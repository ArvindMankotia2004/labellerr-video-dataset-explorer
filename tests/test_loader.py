"""
Basic tests for src/loader.py. Run with:
    python3 -m unittest discover -s tests -v
(No pytest / external dependency required.)
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import loader  # noqa: E402


class TestLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clips = loader.load_clips()

    def test_loads_rows(self):
        self.assertGreater(len(self.clips), 0)

    def test_expected_columns_present(self):
        clip = self.clips[0]
        for key in ("label", "youtube_id", "youtube_url", "time_start",
                    "time_end", "duration_seconds", "split", "clip_id"):
            self.assertIn(key, clip)

    def test_duration_is_end_minus_start(self):
        for clip in self.clips[:20]:
            self.assertEqual(
                clip["duration_seconds"],
                clip["time_end"] - clip["time_start"],
            )

    def test_unique_labels(self):
        labels = loader.unique_labels(self.clips)
        self.assertEqual(labels, sorted(set(labels)))
        self.assertGreater(len(labels), 1)

    def test_filter_by_keyword(self):
        result = loader.filter_clips(self.clips, keyword="archery")
        self.assertTrue(len(result) > 0)
        self.assertTrue(all("archery" in c["label"].lower() for c in result))

    def test_filter_by_exact_label(self):
        label = loader.unique_labels(self.clips)[0]
        result = loader.filter_clips(self.clips, label=label)
        self.assertTrue(all(c["label"] == label for c in result))

    def test_filter_by_duration_range(self):
        result = loader.filter_clips(self.clips, min_duration=10, max_duration=10)
        self.assertTrue(all(c["duration_seconds"] == 10 for c in result))

    def test_filter_no_match_returns_empty(self):
        result = loader.filter_clips(self.clips, keyword="zzz_not_a_real_label_zzz")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
