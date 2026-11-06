"""Check that every speaker note fits its page.

usage (from the presentation folder, after building the speaker notes): python tools/check_notes.py

A note that is too long for its page is cut off without a warning. For each \\note{...} in slides/*.tex,
the last four words of the note must occur in the text of build/speaker-notes.pdf, and no notes page may
have ink in its bottom 2.5 mm. Exits with 1 when a check fails. Requires PyMuPDF (pip install pymupdf).
"""
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "build" / "speaker-notes.pdf"


def norm(text: str) -> str:
    """Lowercase letters and digits only, one space between words."""
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def notes(tex: str):
    """Yield the bodies of \\note{...} and \\note<...>{...}, with balanced braces."""
    for m in re.finditer(r"\\note(?:<[^>]*>)?\{", tex):
        depth, i = 1, m.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(tex[i], 0)
            i += 1
        yield tex[m.end():i - 1]


def plain(body: str) -> str:
    """A note's words as the PDF shows them: no time range, math reduced to its letters, no commands."""
    body = re.sub(r"\\textbf\{[^{}]*\}", " ", body, count=1)
    body = re.sub(r"\$([^$]*)\$", lambda m: re.sub(r"[^A-Za-z0-9]", "", m.group(1)), body)
    body = re.sub(r"\\[a-zA-Z]+\*?", " ", body)
    return body


def main() -> int:
    if not PDF.exists():
        print(f"{PDF.relative_to(ROOT)} is missing: build it first (build.ps1 or build.sh speaker-notes)")
        return 1
    doc = pymupdf.open(PDF)
    text = "\n".join(page.get_text() for page in doc)
    flat = norm(re.sub(r"-[ \t]*\r?\n[ \t]*", "", text))  # join words hyphenated at line ends
    missing, count = [], 0
    for f in sorted((ROOT / "slides").glob("*.tex")):
        for body in notes(f.read_text(encoding="utf-8")):
            count += 1
            tail = " ".join(norm(plain(body)).split()[-4:])
            if tail not in flat:
                missing.append((f.name, tail))
    print(f"{count} notes; {len(missing)} without their last words in the PDF")
    for name, tail in missing:
        print(f"  {name}: ... {tail}")
    low = []
    for k, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=254)  # 10 px per mm
        bottom = pix.samples[-25 * pix.stride:]  # the bottom 2.5 mm
        step = pix.n
        if any(min(bottom[i:i + 3]) < 200 for i in range(0, len(bottom) - 2, step)):
            low.append(k)
    print(f"{doc.page_count} notes pages; ink in the bottom 2.5 mm on: {low or 'none'}")
    return 1 if missing or low else 0


if __name__ == "__main__":
    sys.exit(main())
