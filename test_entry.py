"""Local simulation of the make.fun grader gate for this entry.

Runs main.py exactly as the grader would (python3.13, stdlib only,
$MAKEFUN_OUTPUT_DIR set to a fresh temp dir) and checks the gate:
entry.txt is UTF-8 text of 1-220 characters, not only whitespace,
and holds exactly one sentence.
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import main as entry_main

REPO = Path(__file__).resolve().parent
MAIN = REPO / "main.py"


def run_entry() -> Path:
    """Run main.py with a fresh MAKEFUN_OUTPUT_DIR; return entry.txt path."""
    tmp = Path(tempfile.mkdtemp(prefix="sheetbelt-gate-"))
    out_dir = tmp / "output"
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(out_dir))
    proc = subprocess.run(
        [sys.executable, str(MAIN)],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"main.py exited {proc.returncode}: {proc.stderr}"
    entry = out_dir / "entry.txt"
    assert entry.is_file(), "main.py did not write $MAKEFUN_OUTPUT_DIR/entry.txt"
    return entry


def read_entry() -> str:
    return run_entry().read_text(encoding="utf-8")


class TestGate(unittest.TestCase):
    def test_entry_is_one_sentence_within_220_chars(self):
        text = read_entry()
        self.assertTrue(text.strip(), "entry.txt is empty or whitespace only")
        self.assertGreaterEqual(len(text), 1, "entry.txt is empty")
        self.assertLessEqual(
            len(text), 220, f"entry.txt is {len(text)} chars, over the 220 cap"
        )
        # Exactly one sentence: one terminal period, at the end, and no
        # other sentence-ending punctuation anywhere.
        self.assertTrue(text.endswith("."), "entry must end with a period")
        self.assertEqual(text.count("."), 1, "entry must contain exactly one period")
        self.assertNotIn("!", text)
        self.assertNotIn("?", text)
        self.assertNotIn(";", text)

    def test_entry_names_annoyance_invention_and_mechanism(self):
        text = read_entry()
        lowered = text.lower()
        self.assertIn("sheetbelt", lowered, "entry must name the invention")
        self.assertIn("sheet", lowered, "entry must name the annoyance (fitted sheet)")
        self.assertIn("bouncer", lowered, "entry must name its silly mechanism")

    def test_entry_is_tight_single_line(self):
        text = read_entry()
        self.assertNotIn("\n", text, "entry must be a single line, no newlines")
        self.assertEqual(text, text.strip(), "entry must not start/end with spaces")


class TestLengthGuard(unittest.TestCase):
    def test_rejects_pitch_over_220_chars(self):
        """A pitch over the 220-char gate must fail loudly, not write
        an entry the sealed scorer would score Valid=0."""
        tmp = Path(tempfile.mkdtemp(prefix="sheetbelt-guard-"))
        out_dir = tmp / "output"
        original_pitch = entry_main.PITCH
        original_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
        try:
            entry_main.PITCH = "x" * 221
            os.environ["MAKEFUN_OUTPUT_DIR"] = str(out_dir)
            with self.assertRaises(SystemExit):
                entry_main.main()
        finally:
            entry_main.PITCH = original_pitch
            if original_env is None:
                os.environ.pop("MAKEFUN_OUTPUT_DIR", None)
            else:
                os.environ["MAKEFUN_OUTPUT_DIR"] = original_env
        self.assertFalse(
            (out_dir / "entry.txt").exists(),
            "no entry.txt may be written when the pitch exceeds 220 chars",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
