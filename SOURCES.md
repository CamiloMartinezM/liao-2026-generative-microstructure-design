# Sources and provenance

The talk rests on the article and its code repository. The article is the publisher's version of record, open access under CC BY-NC-ND 4.0; the code repository was read on 4 November 2026 at commit 25f6017 of 6 September 2026. The Supplementary Information, the transparent peer review file and the source data of the article are not used. The groundwork section (slides 5 to 10) rests on the original papers of each method, listed under methods and background.

## The paper and its code

| Source | Used for |
|---|---|
| W. Liao, K. Li, B. Tang, J. Fan, J. Wang, X. Xue, J. Li, R. Yuan, *Generative design of high-fidelity microstructures using physics-aware machine learning*, Nature Communications 17, 11232 (2026), [doi:10.1038/s41467-026-78118-3](https://doi.org/10.1038/s41467-026-78118-3) | The method and the results throughout; Figs. 1 to 5 on slides 3, 13, 16 and 19 to 23 |
| W. Liao, R. Yuan, [nwpuai4msegroup/microstructures_design](https://github.com/nwpuai4msegroup/microstructures_design), commit 25f6017, MIT licence; archived at [doi:10.5281/zenodo.21897025](https://doi.org/10.5281/zenodo.21897025) | `dataset.csv`, copied to `presentation/assets/liao2026/dataset.csv`: the processing route, yield strength and elongation of the 25 variants, on slides 2, 4, 11, 21 and A2 |

## Figures of the paper

The images in `presentation/assets/liao2026/` are the figure images embedded in the article PDF, unchanged. Each is 2000 pixels wide. A slide shows one pixel box of a figure, scaled and unmodified, and draws its labels, braces and captions beside it.

| File | SHA-256 |
|---|---|
| `figure-01.jpg` | `7e52534c9a3d9eedf6b1c7c16645d227b7390334e7e10fda21838f8350e66b35` |
| `figure-02.jpg` | `8a2544b4fad62bc6ba20825263295bc1d4183274a62f3c203815a6e8b2a6da9d` |
| `figure-03.jpg` | `c733231ae60cb22bd567e2a5e7def6d9df970ff5a8b15fcfa4c1142e00834060` |
| `figure-04.jpg` | `d65e36d08bdf9f75d11341bda08abcdad240ed28ad9e277b654d65a59576a9c7` |
| `figure-05.jpg` | `2d5193056ee78086e134cdf219bc263ccbc206d95438023ce1a0f2fd70a882aa` |

| Slide | Figure | Pixel box (x0, y0)–(x1, y1) |
|---|---|---|
| 3 | Fig. 2c, test patches and their reconstructions with the pixel loss | (340, 770)–(1897, 1268) |
| 13 | Fig. 1a, the schematic without the loss equation below it | (0, 0)–(2000, 258) |
| 16 | Fig. 2c, all three rows | (340, 770)–(1897, 1537) |
| 19 | Fig. 3i–n | (0, 700)–(2000, 1883) |
| 20 | Fig. 4b and 4c | (0, 480)–(640, 975) and (640, 480)–(1260, 975) |
| 21 | Fig. 4e | (1280, 480)–(2000, 975) |
| 22 | Fig. 5a–d | (0, 0)–(1300, 965) |
| 23 | Fig. 5e, the map only, and Fig. 5h | (1430, 49)–(1908, 434) and (660, 972)–(2000, 1473) |

Slide 13 labels Fig. 1a with facts from the Results and Methods: patches of 100 × 100 pixels, a code of 128 numbers, three convolutional layers in the encoder and three transposed ones in the decoder, the losses of Eqs. 11 and 15, and the 57,600 training images of the 20 training alloys.

## Values read off the figures

Each value was measured on the figure images: the centre of a mark, or the top of a bar, located in pixels and converted with the pixel positions of the axis ticks. The readings are accurate to about 5 MPa and 0.5 % elongation: read the same way, the 14 marks of measured alloys that stand alone in Fig. 4f agree with `dataset.csv` to within 3 MPa and 0.3 %.

| Slide | Figure | Values |
|---|---|---|
| 4, 21 | Fig. 4f | The five candidates: 556 MPa and 68.8 %; 666 and 67.6; 677 and 65.3, labelled ②; 823 and 48.1, labelled ①; 899 and 46.5 |
| 23 | Fig. 5h | Candidate ①: predicted about 820 MPa and 48 %, simulated about 808 MPa and 44.5 %, measured on the new alloy about 825 MPa and 43.5 % |

## Drawings

| Slide | Drawing | Basis |
|---|---|---|
| Title, 2, 4, 21 | The strength–elongation plane | `dataset.csv`; the front is the staircase that bounds the alloys no other alloy beats in both properties; candidates and candidate ① as read above |
| 5 | Three ways to generate an image | The lecture's contrast of token-based and diffusion-based generation, extended by generation in one pass: a code decoded by a decoder; the illustrative patch cut into 8 × 8 tiles and written in reading order, with the 28th tile outlined; the forward diffusion images of slide 8 in reverse order; `make_assets.py` |
| 6 | Variational Autoencoder | Kingma and Welling (2013): encoder, mean and spread, a sampled code, decoder, reconstruction and KL terms; the code size of 128 from the paper; the latent space is a schematic |
| 7 | Reconstruct, generate, extrapolate | A schematic of the three uses of a generative model and the check each allows |
| 8 | Forward diffusion | The illustrative patch at 100 × 100 pixels, noised as $x_t=\sqrt{\bar\alpha_t}\,x+\sqrt{1-\bar\alpha_t}\,\epsilon$ with the linear schedule of Ho et al. (2020), β from 10⁻⁴ to 0.02 over 1000 steps, one noise image for all t; `make_assets.py`. The step equation is that of Ho et al. (2020) and the paper's Eq. 12, written for one sample. The two rows below, unconditional and conditional generation, reuse these images, with the blurred patch as the guide |
| 9 | One training step | Algorithm 1 of Ho et al. (2020): the patch, the noise image and the patch at t = 150 from the forward diffusion of slide 8, mixed by the paper's Eq. 13; the squared error of the predicted noise as in Ho et al. (2020); the conditioned U-Net of the paper's Eqs. 14 and 15 |
| 10 | Pareto fronts and NSGA-II | The name in three parts after Deb et al. (2002): hand-placed points for dominance (A beats B in both goals; A, C and D form front 1, B front 2) and for crowding (a near-copy dropped, a point with room around it kept); the generation loop as in Holland (1975) |
| 4 | Two fixes | After Fig. 1: the illustrative patch blurred and sharp, its centre enlarged three times in a lens; the latent space as a schematic after Fig. 1c, with random codes among the training codes and codes steered to targets outside them; the plane of slide 2 with the five candidates of Fig. 4f beyond the front |
| 14, 17, 18 | Schematics of the paper's loss, descriptors and search | After Fig. 4a and the Methods (Eqs. 1–16). On slide 17 the shapes come from the Results: 80 patches, a 128 × 80 code matrix, two 128-number descriptors and the first 3 of 24 components of each; the code matrices and strips are shaded at random with fixed seeds. Slide 18 draws the loop of slide 10 with toy fronts of 16 random points (fixed seed), one tree per property, and the way back of slide 17 |
| 15 | Structural similarity | The illustrative patch against copies brightened by 0.25, with the contrast cut to 40 % around the mean, and with its 8 × 8 tiles shuffled (fixed seed); L, C and S of the paper's Eqs. 4 to 6 over the whole patch on grey values, with C1 = 0.01² and C2 = 0.03² as in Wang et al. (2004) and C3 = C2/2; the mean absolute difference and SSIM of the brighter and the blurred patch in the notes; `make_assets.py` |
| 11 | The processing design | `dataset.csv`: hot-rolling reduction across, annealing temperature down, annealing time in each cell, shaded by yield strength |
| 12 | Counts | Results and Methods: 25 maps, a 20/5 split, 80 patches of 100 × 100 pixels per map, six geometric versions and five degraded copies of each; 72,000 = 57,600 + 14,400 |
| Title, 4, 5–9, 11, 12, 14, 15, 17, 18, 22 | Grain maps | Synthetic Voronoi tessellations coloured like Euler maps (red φ1/360°, green Φ/90°, blue φ2/90°), written by `presentation/tools/make_assets.py` with fixed seeds; illustrations, not data from the paper |

## Methods and background

| Source | Used for |
|---|---|
| D. P. Kingma, M. Welling, *Auto-encoding variational Bayes*, arXiv:1312.6114 (2013), ICLR 2014 | The VAE, slides 5, 6 and 13 |
| I. Goodfellow et al., *Generative adversarial nets*, NeurIPS 2014 | GANs on slide 5 |
| J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, S. Ganguli, *Deep unsupervised learning using nonequilibrium thermodynamics*, ICML 2015 | Diffusion models, slide 8 |
| J. Ho, A. Jain, P. Abbeel, *Denoising diffusion probabilistic models*, NeurIPS 2020 | DDPM, its noise schedule, its training by noise prediction and its sampling step, slides 5, 8, 9, 13 and A1 |
| O. Ronneberger, P. Fischer, T. Brox, *U-Net*, MICCAI 2015 | The denoising network, slides 8 and 9 |
| A. Ramesh, M. Pavlov, G. Goh, S. Gray, C. Voss, A. Radford, M. Chen, I. Sutskever, *Zero-shot text-to-image generation*, ICML 2021, PMLR 139, 8821–8831 | DALL-E 1, an image generated token by token from 32 × 32 tokens that a discrete VAE decodes, slide 5 |
| R. Rombach, A. Blattmann, D. Lorenz, P. Esser, B. Ommer, *High-resolution image synthesis with latent diffusion models*, CVPR 2022 | Latent diffusion and Stable Diffusion, slide 5 |
| K. Pandey, A. Mukherjee, P. Rai, A. Kumar, *DiffuseVAE*, TMLR 2022 | A diffusion model guided by a VAE's output, slide 13 |
| A. Singla, *Generative AI*, week 6: multimodal foundation models, lecture slides, Saarland University, winter semester 2024/25 | The contrast of token-by-token and step-by-step generation, with DALL-E 1 against DALL-E 2 and Stable Diffusion (slide 5); the forward and reverse Markov chains of DDPM with fixed $\beta_t$ and the noised sample in closed form (slide 8); training by noise prediction and the U-Net that takes the step as an input (slide 9). Background for the speaker: the slides draw their own figures and do not cite the lecture |
| I. Sobel, G. Feldman, *A 3 × 3 isotropic gradient operator for image processing*, talk at the Stanford Artificial Intelligence Project, 1968 | The Sobel filter, slide 14 |
| Z. Wang, A. C. Bovik, H. R. Sheikh, E. P. Simoncelli, *Image quality assessment: from error visibility to structural similarity*, IEEE TIP 13(4), 600–612, 2004 | SSIM, slides 14, 15 and A1 |
| K. Pearson, *On lines and planes of closest fit to systems of points in space*, Philosophical Magazine 2(11), 559–572, 1901 | PCA, slide 17 |
| V. Pareto, *Manuale di economia politica*, 1906; J. H. Holland, *Adaptation in Natural and Artificial Systems*, 1975; K. Deb, A. Pratap, S. Agarwal, T. Meyarivan, *A fast and elitist multiobjective genetic algorithm: NSGA-II*, IEEE TEVC 6(2), 182–197, 2002 | Pareto fronts, genetic algorithms and NSGA-II, slides 10 and 18 |
| L. Breiman, J. H. Friedman, R. A. Olshen, C. J. Stone, *Classification and Regression Trees*, 1984; J. H. Friedman, *Greedy function approximation: a gradient boosting machine*, Ann. Statist. 29(5), 1189–1232, 2001 | Gradient-boosted trees, slide 20 |
| E. Ma, T. Zhu, *Towards strength–ductility synergy through the design of heterogeneous nanostructures in metals*, Materials Today 20(6), 323–331, 2017 | The mechanism of slide 22, which the paper cites |

Some statements in the notes rest on common practice rather than on the paper: a VAE trained with a pixel loss returns blurry images (slide 6), and diffusion leads image generation today (slide 5).

## Branding

The colours, fonts, theme and logos are those of the Coding Agents 101 talk ([AI-Best-Practices](https://github.com/CamiloMartinezM/AI-Best-Practices)), whose `SOURCES.md` gives their origin: the UdS colours, Latin Modern Sans and FiraCode Nerd Font Mono, the UdS logo from the UdS style guide and the d3M logo from the group's website, unmodified.
