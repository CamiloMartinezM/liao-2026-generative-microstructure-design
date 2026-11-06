# Timed outline

About 24 minutes plus discussion: 29 slides including the title, four section dividers and a closing slide. Timings match the speaker notes; "No." is the number in the slide footer. Section 1 makes the problem concrete with one failure case and names the paper's two obstacles. Section 2 introduces the machine-learning methods the paper combines, for an audience that has not followed that literature. Sections 3 and 4 tell the method and the results as the authors report them.

Three threads run through the talk. The failure case of slide 3, real patches blurred by a pixel loss, returns on slide 16 with the new loss. The strength–elongation plane of the 25 measured alloys returns on slide 4 and on slide 21 with the candidates; the title panel shows it too. The three tasks of slide 7 (reconstruct, generate, extrapolate) frame the results on slides 19 and 21.

| No. | Time | Slide | Purpose |
|---|---|---|---|
| — | 0:00 | Title | Topic, paper, presenter; a grain map above the strength–elongation plane with a star beyond the front |
| 1 | 0:20 | Outline | The four sections, each with its question |
| — | 0:50 | Divider 01: The design problem | |
| 2 | 1:00 | Strength/ductility trade-off | The 25 measured alloys and their front, from the repository's `dataset.csv`, with the two ends of the trade-off marked: ductile but weak, strong but brittle; the goal up and to the right |
| 3 | 2:10 | Classic pixelwise loss fails | Fig. 2c, real patches and their reconstructions with a pixel loss only, beside the MAE and MSE: blurred or missing boundaries, mixed orientations |
| 4 | 3:10 | Two fixes | The obstacles in red on the left, the paper's fixes in green on the right: the same patch region enlarged, blurred with a pixel loss and sharp with the edge and structure terms; random codes falling among the training codes in the latent space, against a property-guided search that steers codes to targets outside them, with its candidates beyond the measured front |
| — | 4:10 | Divider 02: Groundwork | |
| 5 | 4:20 | Three ways to generate an image | Three cards: in one pass (a decoder; VAE, GAN), token by token (each tile from the tiles before it; DALL-E 1), step by step from noise (DDPM, Stable Diffusion, DALL-E 2); the paper joins the first and the third |
| 6 | 5:20 | Variational Autoencoder (VAE) | Encoder, mean and spread, a sampled code, decoder; the loss as reconstruction plus KL; a latent space of overlapping codes, where a new code gives a new patch |
| 7 | 6:40 | Reconstruct, generate, extrapolate | Three cards on the same cloud of training codes, each with what can check it: its input, held-out data, an experiment |
| 8 | 7:40 | Diffusion models | The forward process on a 100 × 100 patch at t = 0, 50, 150, 300 and 1000 with its step $x_t=\sqrt{1-\beta_t}\,x_{t-1}+\sqrt{\beta_t}\,\epsilon$, the learned reverse process, and generation with the trained model in two ways: unconditional, from noise alone, and conditional, with a guide image |
| 9 | 8:50 | Training a diffusion model | A patch and a noise image mixed in one go to a random step, the U-Net's predicted noise against the added noise, repeated over many patches; the paper's U-Net also sees the VAE output |
| 10 | 10:00 | Pareto fronts and NSGA-II | The name in three parts: non-dominated sorting (A beats B in both goals; A, C and D form front 1), the genetic algorithm's loop, and crowding distance (a near-copy dropped, a point with room kept); the result, front 1 spread out |
| — | 11:20 | Divider 03: The method | |
| 11 | 11:30 | 25 alloys, one map each | The orthogonal processing design as a grid, shaded by yield strength; one EBSD map and one tensile result per alloy |
| 12 | 12:40 | Alloy split before cropping | Training and test lanes: alloys, patches, flips and rotations, degraded copies, with their counts |
| 13 | 13:30 | A VAE, refined by diffusion | The paper's Fig. 1a, the two models of section 2 joined, labelled with the sizes (patches of 100 × 100 pixels, a code of 128 numbers), both models and their losses, the training data and how a new patch is generated |
| 14 | 14:20 | Optimization Loss | $L = L_{\mathrm{pix}} + L_{\mathrm{edge}} + L_{\mathrm{SSIM}}$, each term over a card that says what it compares; Sobel and Feldman (1968) and Wang et al. (2004) in the footer |
| 15 | 15:30 | Structural Similarity (SSIM) | Luminance, contrast and structure, each with its formula and a copy of the patch that changes only what it measures (brighter, flatter, tiles shuffled); their product with the paper's exponents, Eq. 8, and the loss 1 − SSIM |
| 16 | 16:40 | The same patches, with the new loss | Fig. 2c with its third row: sharp boundaries again |
| 17 | 17:20 | Six numbers per alloy | One alloy's map to 80 codes of 128 numbers, their mean and spread, the first 3 of 24 principal components of each; the table of 25 alloys the descriptors fill, and the way back in red |
| 18 | 18:10 | A genetic search in six numbers | The loop of slide 10 as four cards (population, predict, keep the best, cross over and mutate) around 500 generations, then the way back from the 5 best descriptors to 80 new patches |
| — | 19:00 | Divider 04: The results | |
| 19 | 19:10 | Grain statistics after reconstruction | Fig. 3i–n: per-alloy averages on the line of equality, test alloys too |
| 20 | 20:00 | Property predictions | Fig. 4b, c: R² of 0.96 and 0.92 on five test alloys |
| 21 | 20:40 | Five candidates beyond the front | The plane of slide 2 with the five candidates read off Fig. 4f; Fig. 4e beside it |
| 22 | 21:40 | Fine grains in the generated patches | Fig. 5a–d, explained by its panel letters, and the proposed mechanism on an illustrative bimodal map |
| 23 | 22:40 | Simulation and one experiment | Fig. 5e, the new alloy's map, and Fig. 5h, candidate 1 as predicted, simulated and measured |
| — | 23:40 | Thank you | The thanks and the presenter; the notes hold four questions for the discussion |

## Appendix

A1 the loss terms in full (Sobel kernels, SSIM, the VAE and diffusion losses); A2 the 25 processing routes from `dataset.csv`; A3 and A4 the references. The notes of A1 and A2 start "If asked".
