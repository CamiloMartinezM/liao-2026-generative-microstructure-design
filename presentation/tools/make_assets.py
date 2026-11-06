"""Make the drawn assets of the talk.

Writes assets/generated.tex, the plot data of the slides: the 25 measured alloys from assets/liao2026/dataset.csv
(the table in the code repository of Liao et al. 2026), their front, the processing design, and values read off
the paper's figures. Also writes the illustrative grain maps in assets/drawn/: synthetic Voronoi tessellations
coloured the way EBSD Euler maps are (the three Euler angles as red, green and blue), not data from the paper.

Run from the presentation folder with a Python that has numpy, scipy and Pillow:

    python -I tools/make_assets.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DRAWN = ASSETS / "drawn"

# Read off the paper's figures by locating each mark against the axis ticks in the figure images
# (assets/liao2026/figure-04.jpg and figure-05.jpg); accurate to about 5 MPa and 0.5 % elongation.
# Fig. 4f, the five optimized candidates: yield strength (MPa), elongation (%), label (0: none).
CANDIDATES = [(556, 68.8, 0), (666, 67.6, 0), (677, 65.3, 2), (823, 48.1, 1), (899, 46.5, 0)]
# Fig. 5h, candidate 1: simulated by CPFE and measured on the processed alloy (the prediction is the 4f point).
SIMULATED = (808, 44.5)
MEASURED = (825, 43.5)


def read_alloys() -> list[dict]:
    with open(ASSETS / "liao2026" / "dataset.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    alloys = []
    for row in rows[1:]:
        ident, temperature, hours, reduction, strength, elongation = row
        alloys.append(
            dict(id=int(ident), temperature=int(temperature), hours=int(hours), reduction=int(reduction),
                 strength=float(strength), elongation=float(elongation))
        )
    assert len(alloys) == 25
    return alloys


def front_path(alloys: list[dict]) -> list[tuple[float, float]]:
    """The staircase that bounds the alloys no other alloy beats in both strength and elongation."""
    ordered = sorted(alloys, key=lambda a: -a["strength"])
    front, best = [], -1.0
    for a in ordered:
        if a["elongation"] > best:
            front.append((a["strength"], a["elongation"]))
            best = a["elongation"]
    front.reverse()  # by increasing strength
    path = [front[0]]
    for (x0, y0), (x1, y1) in zip(front, front[1:]):
        path += [(x0, y1), (x1, y1)]
    return path


def number(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def euler_rgb(phi1, big_phi, phi2) -> np.ndarray:
    """Euler angles (degrees) as red, green and blue, each scaled by its range."""
    return np.stack([np.asarray(phi1) / 360.0, np.asarray(big_phi) / 90.0, np.asarray(phi2) / 90.0], axis=-1)


def euler_angles(rng: np.random.Generator, n: int) -> np.ndarray:
    """Random orientations; Phi stays below 55 degrees, as in the paper's maps of a cubic alloy (Fig. 3g)."""
    return np.column_stack([rng.uniform(0, 360, n), rng.uniform(0, 55, n), rng.uniform(0, 90, n)])


def seeds(rng: np.random.Generator, n: int, size: tuple[int, int], min_dist: float, centre=None, radius=None):
    """Points at least min_dist apart, in the image or within radius of centre."""
    points, tries = [], 0
    while len(points) < n and tries < 50000:
        tries += 1
        if centre is None:
            p = rng.uniform((0, 0), size)
        else:
            a, r = rng.uniform(0, 2 * np.pi), radius * np.sqrt(rng.uniform())
            p = np.asarray(centre) + r * np.array([np.cos(a), np.sin(a)])
        if all(np.hypot(*(p - q)) >= min_dist for q in points):
            points.append(p)
    return np.array(points)


def labels(width: int, height: int, points: np.ndarray) -> np.ndarray:
    yy, xx = np.mgrid[0:height, 0:width] + 0.5
    _, lab = cKDTree(points).query(np.column_stack([xx.ravel(), yy.ravel()]))
    return lab.reshape(height, width)


def boundary_mask(lab: np.ndarray, width: int) -> np.ndarray:
    edge = np.zeros(lab.shape, bool)
    edge[:, :-1] |= lab[:, :-1] != lab[:, 1:]
    edge[:-1, :] |= lab[:-1, :] != lab[1:, :]
    return ndimage.binary_dilation(edge, iterations=width) if width else edge


def render(lab, angles, rng=None, line=1) -> np.ndarray:
    rgb = euler_rgb(*angles.T)[lab]
    if rng is not None:  # a slight orientation spread inside the grains, as EBSD maps show
        noise = ndimage.gaussian_filter(rng.normal(0, 1, rgb.shape), sigma=(14, 14, 0))
        rgb = rgb + 0.6 * noise / max(noise.std(), 1e-9) * 0.03
    rgb = 0.85 * rgb + 0.15 * 0.5
    rgb[boundary_mask(lab, line)] = 0.08
    return np.clip(rgb, 0, 1)


def save(rgb: np.ndarray, name: str) -> None:
    Image.fromarray((np.clip(rgb, 0, 1) * 255).round().astype(np.uint8)).save(DRAWN / name, optimize=True)
    print("wrote", (DRAWN / name).relative_to(ROOT))


def sobel_edges(rgb: np.ndarray) -> np.ndarray:
    """|S_x * x| + |S_y * x| on the grey values, drawn in the talk's blue on white."""
    grey = rgb.mean(axis=2)
    mag = np.abs(ndimage.sobel(grey, axis=1)) + np.abs(ndimage.sobel(grey, axis=0))
    mag = ndimage.maximum_filter(mag, size=3)  # lines thick enough to see at icon size
    mag = np.clip(mag / np.percentile(mag, 97), 0, 1)[..., None]
    blue = np.array([0, 73, 118]) / 255
    return 1 - mag * (1 - blue)


def drawn_maps() -> dict[str, tuple[int, int, int]]:
    DRAWN.mkdir(exist_ok=True)
    rng = np.random.default_rng(625)
    # a square patch: sharp, as a pixel loss blurs it, and its Sobel edges
    pts = seeds(rng, 34, (400, 400), 46)
    lab = labels(400, 400, pts)
    ang = euler_angles(rng, len(pts))
    texture = np.random.default_rng(7)
    sharp = render(lab, ang, texture, line=2)
    save(sharp, "grain-map.png")
    save(ndimage.gaussian_filter(sharp, sigma=(5, 5, 0)), "grain-map-blurred.png")
    # the edges of the coloured grains, without the drawn boundary lines, so that each boundary is one line
    save(sobel_edges(render(lab, ang, np.random.default_rng(7), line=0)), "grain-map-edges.png")
    # a whole map, 1000 x 800 pixels in shape
    pts = seeds(rng, 150, (500, 400), 24)
    save(render(labels(500, 400, pts), euler_angles(rng, len(pts)), rng, line=1), "grain-map-wide.png")
    # coarse grains, with round clusters of fine grains cut into them
    coarse = seeds(rng, 11, (400, 400), 105)
    lab = labels(400, 400, coarse)
    yy, xx = np.mgrid[0:400, 0:400] + 0.5
    count = len(coarse)
    for centre, radius in (((100, 115), 58), ((300, 295), 64), ((300, 75), 44)):
        fine = seeds(rng, 60, (400, 400), 13, centre=centre, radius=radius)
        inside = np.hypot(xx - centre[0], yy - centre[1]) < radius
        lab[inside] = count + labels(400, 400, fine)[inside]
        count += len(fine)
    save(render(lab, euler_angles(rng, count), rng, line=1), "grain-map-bimodal.png")
    # a small map, the same map rotated by 90 degrees with its colours kept, and the rotated sample's map,
    # whose first Euler angle turns with the sample
    pts = seeds(rng, 9, (200, 200), 52)
    lab = labels(200, 200, pts)
    ang = euler_angles(rng, len(pts))
    save(render(lab, ang, line=1), "rotation-map.png")
    turned = np.rot90(lab, k=-1)
    save(render(turned, ang, line=1), "rotation-colours-kept.png")
    shifted = ang.copy()
    shifted[:, 0] = (shifted[:, 0] + 90) % 360
    save(render(turned, shifted, line=1), "rotation-sample-turned.png")
    # a second patch, for codes that decode to a new microstructure
    other = np.random.default_rng(2026)
    pts = seeds(other, 30, (400, 400), 48)
    save(render(labels(400, 400, pts), euler_angles(other, len(pts)), other, line=2), "grain-map-new.png")
    diffusion_steps()
    token_order()
    # swatches of nearly equal orientations far apart in colour, without the maps' grey blend
    swatch = lambda a, b, c: tuple(int(round(255 * v)) for v in np.clip(euler_rgb(a, b, c), 0, 1))
    return {
        "wrapA": swatch(2, 30, 45), "wrapB": swatch(358, 30, 45),
        "symA": swatch(120, 30, 1), "symB": swatch(120, 30, 89),
    }


DIFFUSION_STEPS = (0, 50, 150, 300, 1000)


def diffusion_steps() -> None:
    """The forward process of a DDPM on the illustrative patch at 100 x 100 pixels, the paper's patch size:
    x_t = sqrt(abar_t) x + sqrt(1 - abar_t) eps, with the linear schedule of Ho et al. (2020), beta from 1e-4 to
    0.02 over T = 1000 steps, and one noise image for all t. Saved four times enlarged, so each pixel shows."""
    patch = np.asarray(Image.open(DRAWN / "grain-map.png").convert("RGB").resize((100, 100), Image.BOX)) / 255
    x = 2 * patch - 1
    abar = np.cumprod(1 - np.linspace(1e-4, 0.02, 1000))
    eps = np.random.default_rng(2020).normal(size=x.shape)
    save(np.kron((np.clip(eps, -1, 1) + 1) / 2, np.ones((4, 4, 1))), "diffusion-noise.png")
    for t in DIFFUSION_STEPS:
        xt = x if t == 0 else np.sqrt(abar[t - 1]) * x + np.sqrt(1 - abar[t - 1]) * eps
        big = np.kron((np.clip(xt, -1, 1) + 1) / 2, np.ones((4, 4, 1)))
        save(big, f"diffusion-t{t}.png")


TOKENS_SHOWN = 27  # of the 8 x 8 tiles; the slide outlines the next one


def token_order() -> None:
    """The illustrative patch cut into 8 x 8 tiles and written in reading order up to TOKENS_SHOWN tiles; the
    tiles still to come are white, as in a model that generates an image token by token."""
    patch = np.asarray(Image.open(DRAWN / "grain-map.png").convert("RGB"), dtype=float) / 255
    tile = patch.shape[0] // 8
    for k in range(TOKENS_SHOWN, 64):
        row, col = divmod(k, 8)
        patch[row * tile:(row + 1) * tile, col * tile:(col + 1) * tile] = 1
    save(patch, "tokens-partial.png")


def pareto_toy() -> list[str]:
    """Non-dominated sorting of 16 random trade-off points (both objectives maximised), for the groundwork slide:
    each point with its rank, the staircases of fronts 1 and 2, and the crowding box of the middle point of
    front 1, spanned by its two neighbours on the front."""
    rng = np.random.default_rng(1906)
    u = rng.uniform(0.06, 0.94, 16)
    v = np.clip(0.92 - 0.78 * u + rng.normal(0, 0.13, 16), 0.05, 0.95)
    pts = list(zip(u, v))
    rank, left, r = {}, set(range(len(pts))), 1
    while left:
        front = {i for i in left if not any(pts[j][0] >= pts[i][0] and pts[j][1] >= pts[i][1] and pts[j] != pts[i]
                                            for j in left)}
        for i in front:
            rank[i] = r
        left -= front
        r += 1

    def staircase(k):
        f = sorted((pts[i] for i in rank if rank[i] == k))
        path = [f[0]]
        for (x0, y0), (x1, y1) in zip(f, f[1:]):
            path += [(x0, y1), (x1, y1)]
        return " -- ".join(f"({a:.3f},{b:.3f})" for a, b in path), f

    one, f1 = staircase(1)
    two, _ = staircase(2)
    m = len(f1) // 2
    (xa, ya), (xm, ym), (xb, yb) = f1[m - 1], f1[m], f1[m + 1]
    return [
        "% Non-dominated sorting of a toy trade-off (pareto_toy): points x/y/rank in the unit square, both",
        "% objectives maximised; staircases of fronts 1 and 2; the crowding box of the middle point of front 1.",
        "\\def\\paretopoints{" + ",".join(f"{a:.3f}/{b:.3f}/{rank[i]}" for i, (a, b) in enumerate(pts)) + "}",
        "\\newcommand\\drawfrontone[1][]{\\draw[#1] " + one + ";}",
        "\\newcommand\\drawfronttwo[1][]{\\draw[#1] " + two + ";}",
        f"\\newcommand\\drawcrowdbox[1][]{{\\draw[#1] ({xa:.3f},{yb:.3f}) rectangle ({xb:.3f},{ya:.3f});}}",
    ]


SSIM_C1, SSIM_C2 = 0.01 ** 2, 0.03 ** 2  # K1 = 0.01 and K2 = 0.03 for values in [0, 1], as in Wang et al. (2004)


def ssim_parts(a: np.ndarray, b: np.ndarray) -> tuple[float, ...]:
    """Luminance, contrast and structure of the paper's Eqs. 4 to 6 over a whole patch, on grey values in [0, 1],
    with C3 = C2 / 2; their product; and the mean absolute difference of the grey values."""
    a, b = a.mean(axis=2), b.mean(axis=2)
    ma, mb, sa, sb = a.mean(), b.mean(), a.std(), b.std()
    cov = ((a - ma) * (b - mb)).mean()
    c3 = SSIM_C2 / 2
    lum = (2 * ma * mb + SSIM_C1) / (ma ** 2 + mb ** 2 + SSIM_C1)
    con = (2 * sa * sb + SSIM_C2) / (sa ** 2 + sb ** 2 + SSIM_C2)
    struct = (cov + c3) / (sa * sb + c3)
    return lum, con, struct, lum * con * struct, float(np.abs(a - b).mean())


def ssim_examples() -> list[str]:
    """Copies of the illustrative patch that each change one SSIM component (brighter, flatter, its 8 x 8 tiles
    shuffled), and the blurred patch; saves the copies and returns their values as TeX macros."""
    x = np.asarray(Image.open(DRAWN / "grain-map.png").convert("RGB"), dtype=float) / 255
    blurred = np.asarray(Image.open(DRAWN / "grain-map-blurred.png").convert("RGB"), dtype=float) / 255
    mu = x.mean(axis=(0, 1), keepdims=True)
    tile = x.shape[0] // 8
    tiles = [x[i:i + tile, j:j + tile] for i in range(0, 8 * tile, tile) for j in range(0, 8 * tile, tile)]
    order = np.random.default_rng(4).permutation(len(tiles))
    shuffled = np.concatenate([np.concatenate([tiles[order[r * 8 + c]] for c in range(8)], axis=1) for r in range(8)])
    cases = {"Bright": np.clip(x + 0.25, 0, 1), "Flat": mu + 0.4 * (x - mu), "Shuffled": shuffled, "Blurred": blurred}
    lines = ["% SSIM of the illustrative patch against changed copies (ssim_examples): \\ssim<copy><L, C, S, Q for",
             "% their product, M for the mean absolute difference>, over the whole patch on grey values"]
    for name, y in cases.items():
        if name != "Blurred":
            save(y, f"ssim-{name.lower()}.png")
        for key, value in zip("LCSQM", ssim_parts(x, y)):
            lines.append(f"\\newcommand\\ssim{name}{key}{{{value:.2f}}}")
    return lines


def write_tex(alloys: list[dict], colours: dict[str, tuple[int, int, int]]) -> None:
    low, high = min(a["strength"] for a in alloys), max(a["strength"] for a in alloys)
    shade = lambda s: round(8 + 62 * (s - low) / (high - low))
    lines = [
        "% Written by tools/make_assets.py; edit the script, not this file.",
        "% The 25 measured alloys (assets/liao2026/dataset.csv): yield strength (MPa)/elongation (%)/ID.",
        "\\def\\alloydata{" + ",".join(
            f"{number(a['strength'])}/{number(a['elongation'])}/{a['id']}" for a in alloys) + "}",
        "% Their front: \\drawfront[options] draws its staircase in (MPa,%) coordinates.",
        "\\newcommand\\drawfront[1][]{\\draw[#1] "
        + " -- ".join(f"({number(x)},{number(y)})" for x, y in front_path(alloys)) + ";}",
        "% The processing design: hot-rolling reduction (%)/annealing temperature (C)/annealing time (h)/"
        "yield strength (MPa)/shade of blue (%).",
        "\\def\\alloygrid{" + ",".join(
            f"{a['reduction']}/{a['temperature']}/{a['hours']}/{round(a['strength'])}/{shade(a['strength'])}"
            for a in alloys) + "}",
        "% Read off the paper's figures: the five candidates of Fig. 4f, yield strength/elongation/label (0: none),",
        "% and candidate 1 in Fig. 5h as simulated and as measured on the processed alloy.",
        "\\def\\candidatedata{" + ",".join(f"{number(x)}/{number(y)}/{l}" for x, y, l in CANDIDATES) + "}",
        "\\def\\predictedpoint{" + "{},{}".format(*[number(v) for v in CANDIDATES[3][:2]]) + "}",
        "\\def\\simulatedpoint{" + "{},{}".format(*[number(v) for v in SIMULATED]) + "}",
        "\\def\\measuredpoint{" + "{},{}".format(*[number(v) for v in MEASURED]) + "}",
        "% Euler colours of nearly equal orientations: phi1 = 2 and 358 degrees (Phi 30, phi2 45), and",
        "% phi2 = 1 and 89 degrees (phi1 120, Phi 30), which a 90-degree cubic symmetry relates.",
    ]
    lines += [f"\\definecolor{{{k}}}{{RGB}}{{{r},{g},{b}}}" for k, (r, g, b) in colours.items()]
    # the table of the appendix, in two halves: ID, annealing (C, h), hot-rolling reduction (%), yield strength
    # (MPa), elongation (%)
    row = lambda a: (f"{a['id']} & {a['temperature']} & {a['hours']} & {a['reduction']} & "
                     f"{a['strength']:.0f} & {a['elongation']:.1f}\\\\")
    lines += [
        "% The 25 processing routes, rows 1-13 and 14-25: ID & C & h & % & MPa & %.",
        "\\def\\alloytableA{" + "".join(row(a) for a in alloys[:13]) + "}",
        "\\def\\alloytableB{" + "".join(row(a) for a in alloys[13:]) + "}",
    ]
    lines += pareto_toy() + ssim_examples()
    (ASSETS / "generated.tex").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote", (ASSETS / "generated.tex").relative_to(ROOT))


if __name__ == "__main__":
    write_tex(read_alloys(), drawn_maps())
