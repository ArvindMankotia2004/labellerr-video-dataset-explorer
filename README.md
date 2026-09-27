# Kinetics-400 (val) Label Explorer

A small tool that ingests a real, publicly labeled video dataset and turns it
into a clean, readable, searchable summary — built for the Labellerr
Software Development Intern take-home assignment.

## Summary Card

| Section | What I did | Confidence (1-5) | Files |
|---|---|---|---|
| 1. Find a labeled dataset | Used the **official Kinetics-400 validation split** annotations (real, publicly hosted action-recognition labels: label, YouTube ID, start/end timestamp, split) | 5 | [`data/kinetics400_val_sample.csv`](data/kinetics400_val_sample.csv) |
| 2. Ingest + clean summary | Python stdlib parser that turns raw rows into clip records with a computed duration and YouTube link | 5 | [`src/loader.py`](src/loader.py) |
| 3. Search & filter | CLI table view **and** a static browser UI, both supporting keyword search, exact-category filter, and duration range | 5 | [`src/cli.py`](src/cli.py), [`web/index.html`](web/index.html) |
| 4. README + assumptions | This file | 5 | `README.md` |
| Bonus: tests | 8 unit tests covering parsing, duration math, and every filter combination | 4 | [`tests/test_loader.py`](tests/test_loader.py) |
| Bonus: deploy | Not deployed to a public host (see "Optional bonus" below for why, and what I'd do instead) | — | — |

## The dataset

**[Kinetics-400](https://www.deepmind.com/open-source/kinetics)**, DeepMind's
widely-used human action recognition video dataset — specifically the
official **validation split** label file
(`https://s3.amazonaws.com/kinetics/400/annotations/val.csv`), which every
paper/codebase using Kinetics-400 downloads from directly. It is video,
comes with real, human-annotated labels already attached (not something I
labeled myself), and each row includes genuine metadata beyond just the
label: a YouTube source ID, a start/end timestamp in the source video
(which gives a clip duration), and the dataset split.

Each row means: *"the 10-second clip from `youtube.com/watch?v=<id>`
between `time_start`s and `time_end`s is an example of the action
`<label>`."*

**Why this one:** it's the standard, most-recognized dataset for exactly
this kind of "labeled clip with metadata" task, it's small and text-only to
work with (no need to actually download video), and the label format
(`label, youtube_id, time_start, time_end, split, is_cc`) maps directly onto
the assignment's example fields (category → `label`; duration →
`time_end - time_start`).

**What I tried first (documenting per the ground rules):** I initially
looked for a ready-made "path,label" style mirror on GitHub/Hugging Face,
since those looked easiest to fetch. I found one (a `vCLIMB`-format mirror)
but it only encoded the label as a bare numeric class ID with no duration
field — not a clean enough summary source. Going back to the *official*
Kinetics annotation CSV (still well within the 30-minute search budget) got
me a real `label` name and real start/end timestamps in one file, which is
a much better fit for the assignment's "labels + metadata" ask.

**Sampling:** the full validation file has ~19,900 clips across all 400
action classes. To keep the repo small and the tool fast to run/review, I
committed a **real, unmodified 498-row subset covering 10 full categories**
(`abseiling` → `auctioning`, alphabetically first), taken directly from the
official file. The loader and both UIs work unmodified against the full
19,900-row file too — just replace `data/kinetics400_val_sample.csv` with
the full `val.csv` and everything (search, filter, duration math) scales
the same way, since nothing is hardcoded to the 10-category subset.

## How to run

```bash
./setup.sh   # verifies Python 3 is available (stdlib only — nothing to install)
./run.sh     # builds web/data.json and starts a local web UI at http://localhost:8000
```

Terminal-only mode (no browser, no server):

```bash
./run.sh --cli                                        # first 40 rows
./run.sh --cli --search archery                        # keyword search on the label
./run.sh --cli --label "air drumming" --min-duration 8  # exact category + duration filter
./run.sh --cli --list-labels                            # every unique category
./run.sh --cli --search cream --export-json out.json    # also write filtered results as JSON
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Assumptions

- **"Search and filter" was interpreted broadly on purpose**: keyword
  search on the label (substring match), an exact-category dropdown/flag,
  and a min/max clip-duration range — all combinable, all in-memory (no
  Elasticsearch/Firestore, per the assignment's "simple in-memory filter is
  fine").
- The web UI is a **static page** (`web/index.html` + a generated
  `data.json`), served with Python's built-in `http.server` — no Flask/
  Express/build step, so it needs nothing beyond Python 3 on a clean
  machine, per the ground rules.
- `web/data.json` is a **generated file** (via `src/build_web_data.py`,
  which `run.sh` calls automatically) and is gitignored rather than
  committed, since it's fully derived from the CSV.
- Every clip in the committed 498-row subset happens to be **exactly 10
  seconds long** — that's a real property of Kinetics-400 (clips are
  standardized to 10s), not a bug in the duration calculation. It does mean
  the duration filter is less visually interesting on this subset than it
  would be on a dataset with more varied clip lengths; I call this out
  explicitly rather than hiding it. The duration field and filter still
  work correctly and would show more spread on the small number of
  Kinetics-400 clips that run shorter than 10s near the end of a source
  video (visible in the full `val.csv`).
- `is_cc` (whether the source video was Creative-Commons licensed) is
  parsed but not surfaced as its own filter — kept as-is in the exported
  JSON in case it's useful, but out of scope for the two required
  filter types.

## Time spent

- Finding and vetting a real dataset with genuine labels + metadata: ~25 min
- Writing the parser + clip model (`loader.py`): ~15 min
- CLI tool with search/filter (`cli.py`): ~20 min
- Static web UI with search/filter (`web/index.html`, `build_web_data.py`): ~35 min
- Tests: ~15 min
- `setup.sh` / `run.sh` + verifying on a clean shell: ~15 min
- README (including this section and the reflection below): ~20 min

## Optional bonus: deployment

I did not deploy this to a public host. The tool has zero dependencies and
runs anywhere Python 3 is installed via `./run.sh`, but wiring up a free-tier
host (Render/Railway/PythonAnywhere) needs an account and credentials I
don't have on hand for this environment. If I were doing that next: since
`web/` is a fully static site (HTML + a generated JSON file), the fastest
path would be a static host like GitHub Pages or Netlify — no server
process needed at all, just `data.json` committed once at deploy time.

## Reflection

**What would I improve about this submission if I had two more hours?**
I'd swap in the full ~19,900-row validation file (or an even larger,
multi-split sample) instead of the 10-category subset, since the tool
already handles that without changes — it would make the duration filter
and the category dropdown much more interesting to actually use. I'd also
add pagination or virtual scrolling to the web table so it stays snappy at
that scale, add a couple of chart-style summary stats (clip count per
category, duration histogram), and actually follow through on the static
deploy described above so there's a live link rather than just
instructions for one.

**What's one thing about this task I didn't already know how to do, and
how did you figure it out?**
I hadn't worked with the Kinetics-400 label file format before and wasn't
sure where a trustworthy, still-live copy of it was hosted — my first
search turned up a GitHub/Hugging Face mirror that turned out to encode
labels as bare numeric class IDs with no duration info, which wasn't
usable for a "clean summary" tool. I used web search (an AI assistant,
per the ground rules' "use any tools you'd normally use on the job") to
track down the *official* DeepMind-hosted annotation CSV instead, confirmed
its column format (`label, youtube_id, time_start, time_end, split, is_cc`)
against Kinetics-loading code from `torchvision`/`huggingface datasets` to
make sure I was reading it correctly, and built the parser around that.
