# Kinetics-400 Label Explorer

Take-home for the Labellerr Software Development Intern role. It reads the label file of a public video dataset and shows it as a searchable table, either in the terminal or in a small web page.

## Summary Card

| Section | What I did | Confidence | Files |
|---|---|---|---|
| Dataset | Used the official Kinetics-400 validation labels (action label, YouTube ID, start/end time) | 4/5 | [data/kinetics400_val_sample.csv](data/kinetics400_val_sample.csv) |
| Ingest + summary | Parser that reads the CSV and adds a duration and YouTube link per clip | 4/5 | [src/loader.py](src/loader.py) |
| Search + filter | Keyword search, exact category, min/max duration. Works in CLI and in the web page | 4/5 | [src/cli.py](src/cli.py), [web/index.html](web/index.html) |
| Tests | 8 small unit tests for parsing and filters | 4/5 | [tests/test_loader.py](tests/test_loader.py) |
| Bonus deploy | Not done | - | - |

## Dataset

I used **Kinetics-400** (DeepMind), a video dataset where each clip is labelled with one human action like "archery" or "arm wrestling". I took the validation split annotations from the official file:

`https://s3.amazonaws.com/kinetics/400/annotations/val.csv`

Each row looks like `label, youtube_id, time_start, time_end, split, is_cc`. So a row says: the 10 second part of that YouTube video between start and end shows this action. The labels are already there, I did not label anything myself.

The full file has around 19,900 rows and 400 classes. To keep the repo small I committed the **first 498 rows unchanged (10 classes, abseiling to auctioning)**. The code does not depend on the subset. Replacing the CSV with the full `val.csv` should work as is.

**What I tried first:** my first search found a Hugging Face mirror of the annotations, but it only had video paths and a number for the class (no class name, no timestamps), so I could not build a useful summary from it. The official CSV had everything in one file, so I switched to it.

## How to run

You only need Python 3. There is nothing to install.

```bash
./setup.sh     # just checks that python3 exists
./run.sh       # builds web/data.json and serves the page at http://localhost:8000
```

Terminal only:

```bash
./run.sh --cli
./run.sh --cli --search archery
./run.sh --cli --label "air drumming" --min-duration 8
./run.sh --cli --list-labels
./run.sh --cli --search cream --export-json out.json
```

Tests:

```bash
python3 -m unittest discover -s tests -v
```

On Windows the `.sh` files need Git Bash or WSL. Without them:

```powershell
python -m src.build_web_data
cd web
python -m http.server 8000
```

## Assumptions and things to know

- "Search and filter" is a simple in-memory filter. No Elasticsearch or Firestore.
- The web page is plain HTML/JS and reads `web/data.json`. That file is generated from the CSV by `src/build_web_data.py` (`run.sh` does it), so it is in `.gitignore`.
- Duration is `time_end - time_start`. Every clip in my subset is exactly 10 seconds, because Kinetics uses fixed 10s clips. So the duration filter works but is not very interesting on this data.
- `is_cc` is kept in the data but I did not make a filter for it.
- I did not deploy the page anywhere.
- I used an AI assistant (Claude) while working on this, as the brief allows. I ran and checked everything myself.

## Time spent

- Finding the dataset: ~30 min
- Parser (`loader.py`): ~25 min
- CLI: ~25 min
- Web page (search + filter): ~45 min
- Tests: ~15 min
- `setup.sh` / `run.sh` and a clean-machine check: ~15 min
- README and the two questions: ~25 min

Total: about 3 hours.

## Two questions

**What would I improve with two more hours?**
I would use the full 19,900 row file instead of the 10 class subset, since the code already supports it. Then I would add pagination to the table, a small chart of clips per category, and deploy the `web/` folder as a static site so there is a live link.

**Something I did not know how to do, and how I figured it out**
I had never worked with the Kinetics annotation format. My first source turned out to have only numeric class IDs and no timestamps. I searched again, found the official CSV, and checked its columns against how torchvision reads the same file before writing the parser.
