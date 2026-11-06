"""Write the placeholder logos and the example figure of the template into presentation/assets/.

usage (from the presentation folder): python tools/make_placeholders.py

  assets/logo-institution.png  wide placeholder for the institution's logo (title and closing slides)
  assets/logo-group.png        square placeholder for the group's logo (title slide and footer)
  assets/example-figure.png    a figure of four 1000 x 1000 px panels, side by side: (a) an input image
                               of shapes, (b) a blurred copy standing for a baseline's output, (c) a
                               slightly softened copy standing for a method's output, and (d) an
                               over-sharpened, noisy copy standing for a method with too much weight on
                               edges

Replace the logos with your own files of the same name (.pdf, .png or .jpg), and the example figure with
your own figures. Requires Pillow 10.1 or later.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "assets"
INK = (24, 36, 51)
GREY = (110, 110, 110)
PALE = (238, 238, 238)


def placeholder(size, lines, path):
    """A pale box with a dashed border and its role in capitals."""
    w, h = size
    im = Image.new("RGB", size, "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, w - 7, h - 7), radius=28, fill=PALE)
    # dashed border
    dash, gap, inset = 34, 22, 6
    for x0 in range(inset + 30, w - inset - 30, dash + gap):
        x1 = min(x0 + dash, w - inset - 30)
        d.line((x0, inset, x1, inset), fill=GREY, width=6)
        d.line((x0, h - inset - 1, x1, h - inset - 1), fill=GREY, width=6)
    for y0 in range(inset + 30, h - inset - 30, dash + gap):
        y1 = min(y0 + dash, h - inset - 30)
        d.line((inset, y0, inset, y1), fill=GREY, width=6)
        d.line((w - inset - 1, y0, w - inset - 1, y1), fill=GREY, width=6)
    font = ImageFont.load_default(size=int(h * 0.16))
    text = "\n".join(lines)
    d.multiline_text((w / 2, h / 2), text, fill=GREY, font=font, anchor="mm", align="center", spacing=12)
    im.save(path, optimize=True)


def shapes_panel():
    """The input panel: shapes on a soft gradient, with two features that a blur destroys."""
    rng = random.Random(7)
    im = Image.new("RGB", (1000, 1000))
    d = ImageDraw.Draw(im)
    for y in range(1000):  # soft vertical gradient
        t = y / 999
        d.line((0, y, 999, y), fill=(int(236 - 18 * t), int(240 - 14 * t), int(246 - 8 * t)))
    colours = [(31, 78, 121), (190, 48, 60), (28, 128, 82), (214, 140, 38), (96, 76, 160), (40, 150, 170)]
    # random shapes, kept away from the two features below
    placed = 0
    while placed < 14:
        cx, cy, r = rng.randint(90, 910), rng.randint(90, 910), rng.randint(45, 110)
        if 380 < cy + r and cy - r < 760 and cx + r > 120:  # the band of the features
            continue
        colour = rng.choice(colours)
        kind = rng.choice(("circle", "square", "triangle"))
        if kind == "circle":
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colour)
        elif kind == "square":
            d.rectangle((cx - r, cy - r, cx + r, cy + r), fill=colour)
        else:
            d.polygon(((cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)), fill=colour)
        placed += 1
    # feature 1: a thin bar, 30 px tall
    d.rectangle((150, 690, 450, 720), fill=INK)
    # feature 2: two squares of different colour that share an edge at x = 760
    d.rectangle((560, 470, 760, 670), fill=colours[1])
    d.rectangle((760, 470, 960, 670), fill=colours[0])
    return im


def over_sharpened(sharp):
    """Halos along edges and grain in flat areas, from a fixed seed."""
    im = sharp.filter(ImageFilter.GaussianBlur(1.6)).filter(ImageFilter.UnsharpMask(radius=9, percent=260))
    rng = random.Random(11)
    noise = Image.new("L", im.size)
    noise.putdata([rng.randint(0, 255) for _ in range(im.size[0] * im.size[1])])
    grain = Image.merge("RGB", (noise, noise, noise)).filter(ImageFilter.GaussianBlur(1.2))
    return Image.blend(im, grain, 0.16)


def example_figure(path):
    sharp = shapes_panel()
    baseline = sharp.filter(ImageFilter.GaussianBlur(18))
    method = sharp.filter(ImageFilter.GaussianBlur(1.6))
    figure = Image.new("RGB", (4000, 1000), "white")
    for k, panel in enumerate((sharp, baseline, method, over_sharpened(sharp))):
        figure.paste(panel, (1000 * k, 0))
    figure.save(path, optimize=True)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    placeholder((1200, 480), ["INSTITUTION", "LOGO"], ASSETS / "logo-institution.png")
    placeholder((480, 480), ["GROUP", "LOGO"], ASSETS / "logo-group.png")
    example_figure(ASSETS / "example-figure.png")
    for name in ("logo-institution.png", "logo-group.png", "example-figure.png"):
        print("wrote", (ASSETS / name).relative_to(ASSETS.parent))
