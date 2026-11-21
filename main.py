"""VELMORA — a travel poster for a place that isn't there.

Writes the poster image to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).

The poster is a vintage mid-century travel poster for Velmora, a fictional
archipelago of floating islands in the sky. Its single landmark is the
white-and-gold lighthouse on the largest island, lit by golden-hour sun
over a calm glowing sea. The place name VELMORA is set in large type at
the top, with the subtitle "ISLANDS IN THE SKY". No quotes, no star
ratings, no other copy.

Pure standard library, no network. The artwork ships as poster.jpg next
to this script and is copied to the output path byte-for-byte.
"""

import os
import sys

MAX_BYTES = 1_048_576
RESOURCE = "poster.jpg"


def _read_poster() -> bytes:
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, RESOURCE), "rb") as f:
        return f.read()


def _write_output(data: bytes) -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_path = os.path.join(out_dir, "entry.png")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)
    except OSError:
        # Fall back to a local ./output directory.
        out_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.png")
        with open(out_path, "wb") as f:
            f.write(data)
    return out_path


def main() -> int:
    data = _read_poster()
    if len(data) > MAX_BYTES:
        print(
            f"poster is {len(data)} bytes, over the {MAX_BYTES} byte limit",
            file=sys.stderr,
        )
        return 1
    out_path = _write_output(data)
    print(f"Wrote {out_path} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
