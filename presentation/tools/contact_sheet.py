"""Render pages of a PDF as one labelled contact sheet, to look over spacing, overlaps and sizes.

usage (from the presentation folder): python tools/contact_sheet.py [pdf] [pages] [columns] [out.png]
  pdf      default build/main.pdf
  pages    such as 1-8,12; default all
  columns  default 3
  out.png  default build/contact-sheet.png
Requires PyMuPDF and Pillow (pip install pymupdf pillow).
"""
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent


def pages_of(spec: str, count: int) -> list[int]:
    if spec == "all":
        return list(range(1, count + 1))
    pages = []
    for part in spec.split(","):
        first, _, last = part.partition("-")
        pages += range(int(first), int(last or first) + 1)
    return [p for p in pages if 1 <= p <= count]


def main() -> None:
    args = sys.argv[1:] + [None] * 4
    pdf = Path(args[0] or ROOT / "build" / "main.pdf")
    columns = int(args[2] or 3)
    out = Path(args[3] or ROOT / "build" / "contact-sheet.png")
    doc = pymupdf.open(pdf)
    thumbs = []
    for p in pages_of(args[1] or "all", doc.page_count):
        page = doc[p - 1]
        zoom = 640 / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        ImageDraw.Draw(im).text((4, pix.height - 14), f"p{p}", fill=(200, 0, 0))
        thumbs.append(im)
    w, h = thumbs[0].size
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * w + (columns + 1) * 8, rows * h + (rows + 1) * 8), (80, 80, 80))
    for k, im in enumerate(thumbs):
        sheet.paste(im, (8 + (k % columns) * (w + 8), 8 + (k // columns) * (h + 8)))
    sheet.save(out)
    print(out, f"{len(thumbs)} pages")


if __name__ == "__main__":
    main()
