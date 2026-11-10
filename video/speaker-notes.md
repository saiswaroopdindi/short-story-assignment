# 10–15 minute recording script

Use the PDF deck in `slides/` while recording. Aim for about 60–90 seconds per slide. Replace the bracketed personal introduction with your own words and add one example from your approved-topic spreadsheet.

## Slide 1 — Title

Introduce the topic as a data-mining survey on autoencoder-based deep clustering. State the central question: can a learned low-dimensional representation make unlabeled groups easier to discover? Mention that the presentation is based on the 2025 arXiv survey by Leiber and coauthors.

## Slide 2 — The data-mining problem

Explain why raw high-dimensional features make distance-based grouping difficult. Use images or text as intuitive examples. The point is not that k-Means is bad. The point is that k-Means can only use the geometry it receives.

## Slide 3 — One taxonomy, three training loops

Define sequential, alternating, and simultaneous deep clustering. Explain the direction of information flow in each loop and preview the trade-off between simplicity and task-specific feedback.

## Slide 4 — The autoencoder

Describe the encoder, latent vector, and decoder. Explain that the bottleneck creates a nonlinear dimensionality-reduction space. Mention that architecture should match the data type, such as convolution for images.

## Slide 5 — Loss design

Explain the reconstruction loss and clustering loss in plain language. Emphasize the weight between them. This is the main place where a method can preserve information while also making clusters more compact.

## Slide 6 — Method comparison

Walk through AE + k-Means, N2D, DEC or IDEC, DCEC, and DKM. For each, state one advantage and one caveat. Avoid presenting any method as universally best.

## Slide 7 — Evaluation

Separate external metrics, internal metrics, robustness, and practical deployment behavior. Explain why one score is not enough. Mention new-sample prediction, seeds, and sensitivity to the number of clusters.

## Slide 8 — Open questions

Discuss unknown cluster count, distribution shift, nuisance variation, and consistent evaluation. Add your own view on which question matters most for a real data-mining deployment.

## Slide 9 — Conclusion

Repeat the workflow: raw-feature baseline, AE + k-Means, then clustering feedback if justified. Close with the main message that representation learning changes the space in which similarity is measured.

## Recording checklist

- Record your own narration and keep the final video between 10 and 15 minutes.
- Keep the slide PDF visible throughout the recording.
- Introduce yourself and the course at the beginning.
- Mention the primary paper and distinguish reported findings from your interpretation.
- Export as MP4 and upload the final file to this repository under `video/`.
