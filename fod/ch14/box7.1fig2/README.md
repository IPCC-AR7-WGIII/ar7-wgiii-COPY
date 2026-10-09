# Box 14.7.1, Figure 2 — The net-effect and counterfactual framing

Figure package for the IPCC WGIII AR7 First Order Draft, Chapter 14
(Digitalisation), Section 14.7. `CITATION.cff` carries the citable metadata and
the full caption.

## What the data is

None. This is a conceptual schematic with no underlying dataset and no displayed
numerical values, so there is no data table to archive. `data/README.md` records
that absence, and the folder is kept so every figure package in this section has
the same structure.

The complete rendered wording lives in the script's content constants: the four
effect rows with their detail lines, the counterfactual baseline label, the two
direction labels and the net-effect statement.

## Input data and methods

No input data. The figure reproduces no dataset, table or published figure. Every
arrow, label and statement is authored content: the chapter team's framing of the
emissions consequence of digitalisation as a net balance of direct,
application-level and economy-wide effects, assessed against a counterfactual in
which the technology is absent.

The figure supplies vocabulary rather than quantities. The quantified assessment
of the net emissions balance is conducted in Chapter 9, and the figure points
there rather than asserting a magnitude of its own.

Because nothing is reproduced or adapted, no copyright permission is required.

## What the code does

`code/box14_7_1_fig2.py` draws the framing on a 180 x 100 mm canvas: four effect
arrows either side of a dashed vertical counterfactual baseline, a horizontal
direction axis labelled for effects decreasing and increasing emissions, and the
net-effect statement in a box along the bottom.

The layout is mapped one to one from the notebook original onto mm coordinates.
Micro-nudges of at most 0.9 mm, commented at the geometry constants, keep the
bold effect names clear of the dashed baseline without moving any arrow, row or
wording.

Direction is drawn by arrow geometry and by which side of the baseline an arrow
sits on, reinforced by the two axis labels, so direction never rests on colour
alone. Dashed strokes carry uncertainty of magnitude and direction, and the
bidirectional arrow marks the effect whose sign is unresolved. All four arrows
are the same length and weight, so no effect is given visual precedence over
another. Non-obvious decisions are commented where they apply, including the
white net-effect box fill that replaces a wash sitting below the 15 per cent
print floor.

Before exporting, the script self-checks font resolution, minimum type size, WCAG
AA contrast, canvas containment, in-box fit, vertical gaps, baseline clearance,
line-width floors and greyscale separation across all arrow pairs. It prints each
result, exits non-zero if any check fails, and exports only when all pass.

## How to run it

1. Install the pinned environment, once:
   `pip install -r ../env/requirements_sec14.7.txt`. See
   `../env/README_sec14.7.md`, including the Arial and Arial Narrow system-font
   requirement, which pip cannot satisfy.
2. Run the figure script: `python code/box14_7_1_fig2.py`. It can be run from any
   working directory, because paths resolve relative to the script. There is no
   data step to run first.

On success it writes `figure/FigBox14_2_net_effect.png` at 300 dpi and the
matching `.pdf` as vector with TrueType embedded.

## Licences

The figure is authored content created by the chapter author team; the same
CC BY 4.0 terms as the section's final data apply to it. Code licensed MIT, as
the SPDX headers in `code/` record.
