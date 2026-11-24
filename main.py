"""One-Sentence Absurd Invention Pitch: Sheetbelt.

Writes a single sentence pitching Sheetbelt -- four tiny mattress
bouncers hired to keep a fitted sheet from escaping overnight -- to
$MAKEFUN_OUTPUT_DIR/entry.txt. Python 3.13, standard library only.
"""

import os
from pathlib import Path

PITCH = (
    "Sheetbelt hires four tiny mattress bouncers who spend all night "
    "shoving your fitted sheet's escaped elastic back onto the bed "
    "before it can run away."
)

# Sealed-scorer gate (RULES.txt): entry.txt must be 1-220 characters.
# Fail loudly here instead of writing an entry the scorer would mark
# Valid=0 with no rate and no prize.
MAX_PITCH_CHARS = 220


def main() -> None:
    if len(PITCH) > MAX_PITCH_CHARS:
        raise SystemExit(
            f"PITCH is {len(PITCH)} characters, over the competition's "
            f"{MAX_PITCH_CHARS}-character gate; shorten it before submitting."
        )
    output_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.txt").write_text(PITCH, encoding="utf-8")


if __name__ == "__main__":
    main()
