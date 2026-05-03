import csv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from grid_resolving_polynomials import test_grid_conjecture

grids = [
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 3),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (4, 4),
    (4, 5),
]

all_results = []

for m, n in grids:
    results = test_grid_conjecture(m, n, verbose=True)
    all_results.extend(results)

output_dir = Path(__file__).resolve().parents[1] / "results"
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "small_grid_coefficient_vectors.csv"

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "grid",
        "k",
        "checked",
        "total",
        "canonical_coefficient_vector",
        "coefficientwise_maximum_vector",
        "passed",
    ])

    for row in all_results:
        writer.writerow([
            row["grid"],
            row["k"],
            row["checked"],
            row["total"],
            row["canonical_poly"],
            row["max_coeffs"],
            row["passed"],
        ])

print(f"Saved results to {output_file}")
