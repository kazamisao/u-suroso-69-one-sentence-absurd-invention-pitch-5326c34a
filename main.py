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


def main() -> None:
    output_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.txt").write_text(PITCH, encoding="utf-8")


if __name__ == "__main__":
    main()
