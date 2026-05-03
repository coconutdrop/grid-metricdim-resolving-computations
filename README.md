# grid-metricdim-resolving-computations
Code and computational results for exhaustive small-grid resolving-polynomial checks.

This repository contains code used to exhaustively test the grid conjecture in the paper
*Probabilistic Fault-Tolerant Metric Dimension*.

For a grid graph \(P_m \square P_n\), the code enumerates all \(k\)-subsets of vertices,
computes the resolving-polynomial coefficient vector

\[
(r_0(S), r_1(S), \ldots, r_k(S)),
\]

and compares it coefficientwise with the canonical long-side set \(C_k\).

## Files

- `src/grid_resolving_polynomials.py`: main functions
- `scripts/run_small_grid_tests.py`: script for reproducing the small-grid computations
- `results/`: computational outputs

## How to run

```bash
python scripts/run_small_grid_tests.py

## Archived release

The archived version of this repository is available on Zenodo:

https://doi.org/10.5281/zenodo.XXXXXXX
