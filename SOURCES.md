# Sources and provenance

Record here what each slide takes from where, so that every figure, value and drawing can be traced and made again: the paper and its version, its code and data with the commit or version and the date they were read, the original papers of each method, and how each figure, screenshot or value was made. The tables below describe the example talk.

## The paper and its code

| Source | Used for |
|---|---|
| A. Author, B. Author, C. Author, *Title of the paper*, Journal 1, 1 (2026), [doi:10.1000/182](https://doi.org/10.1000/182) | The method and the results throughout; Figs. 1 to 3 and Table 2 on slides 2, 3, 5, 7 and 8 |
| A. Author, code repository, commit and licence, read on DD Month YYYY | The commands and the configuration on slide 6 |

## Figures

`presentation/assets/example-figure.png` stands in for a paper's figure: four panels of 1000 × 1000 pixels side by side, (a) an input image of shapes, (b) a blurred copy for the baseline's output, (c) a slightly softened copy for the method's output, and (d) an over-sharpened, grainy copy for too much weight on edges. `presentation/tools/make_placeholders.py` draws it with fixed seeds.

| Slide | Figure | Pixel box (x0, y0)–(x1, y1) |
|---|---|---|
| Title, closing | Panel a | (0, 0)–(1000, 1000) |
| 2 | Panels a and b | (0, 0)–(1000, 1000) and (1000, 0)–(2000, 1000) |
| 3 | Panels a and c | (0, 0)–(1000, 1000) and (2000, 0)–(3000, 1000) |
| 5 | The two squares in panels b, c and d | (1540, 430)–(1980, 710), (2540, 430)–(2980, 710) and (3540, 430)–(3980, 710) |
| 8 | Panels a, b and c | (0, 0)–(3000, 1000) in three boxes |

## Drawings

| Slide | Drawing | Basis |
|---|---|---|
| Title, closing | The input above a bar chart of the result | Panel a; the errors of slide 7 |
| 3 | The pipeline | After Fig. 1 of the paper |
| 4 | The loss, each term labelled | Eqs. 1 to 3 of the paper |
| 7 | Bar chart of the test error | Table 2 of the paper; the values are examples |

## Methods and background

| Source | Used for |
|---|---|
| D. Other, A. Author, *Title of the method's paper*, Proceedings of the Conference, 100–110 (2020) | The edge term, slides 4 and A1 |
