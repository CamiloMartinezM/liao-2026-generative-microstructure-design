# Generative design of high-fidelity microstructures using physics-aware machine learning (Liao et al., 2026)

A LaTeX Beamer talk of about 24 minutes for the d3M group on W. Liao et al., "Generative design of high-fidelity microstructures using physics-aware machine learning", *Nature Communications* 17, 11232 (2026), [doi:10.1038/s41467-026-78118-3](https://doi.org/10.1038/s41467-026-78118-3). The talk tells the paper's own story:

- the design problem: the strength–ductility trade-off of 25 Inconel 625 variants, and a pixel loss that blurs grain boundaries in EBSD maps;
- the groundwork, for an audience that has not followed the machine-learning literature: three ways to generate an image (in one pass, token by token, step by step from noise), the variational autoencoder, what reconstructing, generating and extrapolating each need as a check, diffusion models and how they are trained, and Pareto fronts with NSGA-II;
- the method: one EBSD map per alloy, split by alloy before cropping; a variational autoencoder refined by a conditional diffusion model; a loss with Sobel-edge and SSIM terms, and SSIM built up from luminance, contrast and structure; six numbers per alloy; gradient-boosted surrogates and an NSGA-II search;
- the results as the authors report them: reconstruction fidelity, surrogate R², five candidates beyond the measured front, fine grains, crystal plasticity simulation and one experimental alloy.

An appendix holds the loss terms in full, the 25 processing routes and the references.

![Pages of the talk](docs/preview.png)

## Start here

- [Slides](presentation/build/main.pdf): 33 pages, 29 for the talk (title, outline, 22 content slides, four section dividers and the closing slide) and 4 appendix pages.
- [Speaker notes](presentation/build/speaker-notes.pdf): 27 pages, one per slide except the dividers and the references, each with the slide, its notes and its time range; the closing slide's notes hold questions for the discussion, and the backup slides A1 and A2 have notes that start "If asked".
- [Timed outline](OUTLINE.md), [sources and provenance](SOURCES.md), and [third-party notices](THIRD-PARTY-NOTICES.md).

## Files

| Path | Content |
|---|---|
| `presentation/main.tex` | Entry point: title, presenter, date, section files |
| `presentation/beamerthemed3m.sty` | The d3M theme, the same file as in the Coding Agents 101 talk ([AI-Best-Practices](https://github.com/CamiloMartinezM/AI-Best-Practices)) |
| `presentation/slides/macros.tex` | Drawing helpers: parts of the paper's figures, the strength–elongation plane, strips and cards |
| `presentation/slides/*.tex` | One file per section; `00-title.tex` holds the title and outline, `02-groundwork.tex` the groundwork, `06-closing.tex` the thank-you slide, `07-appendix.tex` the appendix |
| `presentation/assets/liao2026/` | Figures 1 to 5 of the paper as published, and `dataset.csv` from the paper's code repository |
| `presentation/assets/drawn/` | Illustrative grain maps, synthetic tessellations coloured like EBSD Euler maps; the forward diffusion of one of them with its noise image; the same patch cut into tiles and written in reading order; and copies of it changed in brightness, contrast and arrangement for SSIM |
| `presentation/assets/generated.tex` | Plot data: the 25 alloys and their front, the processing design, values read off the paper's figures, the table of A2, the toy fronts of the search slide, and the SSIM values of the SSIM slide |
| `presentation/tools/make_assets.py` | Writes `assets/generated.tex` and the images in `assets/drawn/` |
| `presentation/tools/check_notes.py`, `presentation/tools/contact_sheet.py` | Check that every speaker note fits its page; render pages to one image |
| `presentation/assets/uds-logo.pdf`, `presentation/assets/d3m.png` | Logos |
| `presentation/build.ps1`, `presentation/build.sh`, `presentation/.latexmkrc` | Builds: PowerShell, POSIX shell, latexmk (XeLaTeX, three passes) |
| `docs/preview.png` | The pages shown above |

## Build

From the `presentation` folder, in PowerShell:

```powershell
.\build.ps1
.\build.ps1 speaker-notes
```

or in a POSIX shell:

```sh
./build.sh
./build.sh speaker-notes
```

`tools/make_assets.py` redraws the plot data and the grain maps; run it first after changing it or `dataset.csv`, with a Python that has numpy, scipy and Pillow:

```powershell
python -I tools/make_assets.py
```

Requirements: XeLaTeX (tested with MiKTeX 25.12) with beamer, TikZ, tcolorbox, listings and fontawesome5, and FiraCode Nerd Font Mono for code, with Latin Modern Mono as the fallback. Three passes are needed because the title page and the section dividers place their graphics relative to the page. The current build has no layout warnings, and every speaker note fits its page. The check tools need Python 3 with PyMuPDF and Pillow.

## Editing

- **Title, presenter and date:** `\title{}`, `\subtitle{}`, `\paperdoi`, `\author{}` and `\date{}` in `main.tex`, with the PDF's own title in `\hypersetup`. The title slide sets the paper's full title in three lines at 16.5 pt, broken at its phrases by `\\` in `\title{}`, and under the citation the DOI as a link to `https://doi.org/` followed by `\paperdoi`; the speaker notes show the same line without the link, because their thumbnails scale the slide but not its links. The text block is anchored at the presenter's name, which keeps the same distance from the d3M block as in the Coding Agents 101 talk, so a longer or shorter title grows or shrinks upwards.
- **Footer:** `main.tex` replaces the theme's footer with the d3M logo, the frame's citation and the slide number alone.
- **Citations:** a frame's `source=` key fills its footer, in one form on every slide. The paper is `Liao et al.\ (2026), Nat.\ Commun.\ 17, 11232`, followed by the figure, equations or section: a reproduced figure adds `(CC BY-NC-ND 4.0)`, and a drawing made after a figure says `after Fig.\ 4f`. Every other work is author, year and venue, with "et al." for three or more authors and "and" for two: a journal by its abbreviation, volume and first page, a conference by its acronym, a preprint by its arXiv number, a book by its title in italics. Works are joined by ` · `; the full references are on slides A3 and A4.
- **The paper's figures:** `\figpart{x}{y}{figure}{x0}{y0}{x1}{y1}{width}` shows the pixel box (x0, y0)–(x1, y1) of `assets/liao2026/figure-0<figure>.jpg` at the given width in millimetres, with its top-left corner at (x, y). The figures are under CC BY-NC-ND 4.0, which allows parts of them but no adaptations: labels, braces and markers go beside a figure, never over it. After a `\figpart`, `\fpx{px}` and `\fpy{py}` give the slide position of an image pixel, as for the row labels on slides 3 and 16. A dense figure is explained beside it by its own panel letters, as on slides 19 and 22.
- **The strength–elongation plane:** `\planeaxes{xmin}{xmax}{ymin}{ymax}{width}{height}{x ticks}{y ticks}` draws the axes; a scope with the style `plane` then takes (MPa, %) coordinates for `\drawalloys`, `\drawfront[front]` and `\drawcandidates`, as on slides 2 and 21 and in the title panel; slide 4 draws a small copy without ticks.
- **Recurring drawings:** the generation loop of slide 10 returns in the cards of slide 18, the way back of slide 17 returns on slide 18, and the forward diffusion of slide 8 returns on slides 5 and 9; change them together.
- **Values read off the paper's figures:** the five candidates of Fig. 4f and candidate 1 in Fig. 5h are set at the top of `tools/make_assets.py`; [SOURCES.md](SOURCES.md) says how they were read.
- **Strips and cards:** `\warnstrip{y}{text}` draws a red strip for a catch and `\goodstrip{y}{text}` a green one for what holds; `\cardhead{x}{y}{width}{colour}{label}` draws a card's head.
- **Glyphs:** `\descstrip{x}{y}{w}{h}` draws a descriptor of six numbers, `\codematrix{x}{y}{columns}{rows}{cell}` a grid of latent codes, `\minitree{x}{y}` a small regression tree, `\fixarrow{x0}{x1}{y}{label}` the broad arrows of slide 4, and `\cardbullet{text}` a line with the theme's square bullet, as on slide 22.
- **Colours:** blue for the method and its parts, red for what to look at (candidates, a catch), dark for data, grey for the measured alloys and for baselines, green for what holds. Every coloured element also has a text label.
- **Speaker notes:** `\note{\textbf{12:20--13:20}\par First point.\par Second point.}`, the time range first and then one sentence per line; a backup slide's note starts with `\textbf{If asked}` and adds no time. A note that is too long is cut off without a warning, so after every change run `python tools/check_notes.py`, which checks that each note's last words appear in `build/speaker-notes.pdf`.
- **Spacing:** the theme starts every slide's content 4 mm below the title. A slide drawn as a `tikzpicture[x=1mm,y=1mm]` starts its first element at y = 0 and stays within `\useasboundingbox (0,0) rectangle (144,-54)`.

## Before presenting

- Check the occasion and date in `\date{}` of `main.tex`: the title slide reads "Research group talk, 05.11.2026".
- The Supplementary Information of the paper, with the baseline comparison, the latent-space interpolation and the candidates' simulated stress–strain curves, is not covered; the notes say where a slide depends on it.

## Credits

The repository was created from [beamer-talk-template](https://github.com/CamiloMartinezM/beamer-talk-template), whose [slide style](https://github.com/CamiloMartinezM/beamer-talk-template/blob/main/SLIDE-STYLE.md) the slides follow. The theme's plain blocks, footer logo and section dividers follow the [TU Delft presentation](https://www.overleaf.com/latex/templates/tu-delft-presentation/jcxrmnxssdst) template by Novanext (CC BY 4.0), and its navigation Beamer's Frankfurt theme; [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) lists all material by others.
