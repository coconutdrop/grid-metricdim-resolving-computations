from itertools import combinations
from math import comb
from functools import lru_cache

def grid_vertices(m, n):
    return [(r, c) for r in range(m) for c in range(n)]

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def canonical_set_indices(m, n, k):
    if m > n:
        raise ValueError("Use m <= n.")

    def idx(r, c):
        return r * n + c

    if k == 2:
        return [idx(0, 0), idx(0, n - 1)]

    if k == 3:
        return [idx(0, 0), idx(0, n - 1), idx(m - 1, 0)]

    cols = [0, n - 1]

    inward = []
    left, right = 1, n - 2
    while left <= right:
        inward.append(left)
        if right != left:
            inward.append(right)
        left += 1
        right -= 1

    paired_cols_needed = k // 2

    for c in inward:
        if len(cols) >= paired_cols_needed:
            break
        cols.append(c)

    S = []
    for c in cols:
        S.append(idx(0, c))
        S.append(idx(m - 1, c))

    if k % 2 == 1:
        for c in inward:
            if c not in cols:
                S.append(idx(0, c))
                break

    return S[:k]

def precompute_landmark_masks(m, n):
    V = grid_vertices(m, n)
    N = len(V)
    pairs = list(combinations(range(N), 2))
    P = len(pairs)

    full_pair_mask = (1 << P) - 1
    landmark_masks = [0] * N

    for w in range(N):
        mask = 0
        for pair_id, (i, j) in enumerate(pairs):
            if dist(V[i], V[w]) != dist(V[j], V[w]):
                mask |= (1 << pair_id)
        landmark_masks[w] = mask

    return landmark_masks, full_pair_mask

def subset_mask(indices):
    mask = 0
    for i in indices:
        mask |= 1 << i
    return mask

def make_resolver(landmark_masks, full_pair_mask):
    @lru_cache(maxsize=None)
    def resolves_cached(vertex_mask):
        combined = 0
        i = 0
        temp = vertex_mask

        while temp:
            if temp & 1:
                combined |= landmark_masks[i]
                if combined == full_pair_mask:
                    return True
            temp >>= 1
            i += 1

        return combined == full_pair_mask

    return resolves_cached

def resolving_polynomial_cached(S_indices, resolves_cached):
    k = len(S_indices)
    coeffs = [0] * (k + 1)

    for t in range(k + 1):
        for T in combinations(S_indices, t):
            T_mask = subset_mask(T)
            if resolves_cached(T_mask):
                coeffs[t] += 1

    return tuple(coeffs)

def test_grid_conjecture(m, n, k_values=None, verbose=True):
    if m > n:
        m, n = n, m

    N = m * n

    if k_values is None:
        k_values = range(2, 2 * n + 1)

    landmark_masks, full_pair_mask = precompute_landmark_masks(m, n)
    resolves_cached = make_resolver(landmark_masks, full_pair_mask)

    results = []

    for k in k_values:
        if k > N:
            continue

        Ck = canonical_set_indices(m, n, k)
        canonical_poly = resolving_polynomial_cached(Ck, resolves_cached)

        max_coeffs = [0] * (k + 1)
        counterexample = None

        checked = 0
        total = comb(N, k)

        for S in combinations(range(N), k):
            checked += 1
            poly = resolving_polynomial_cached(S, resolves_cached)

            for t in range(k + 1):
                if poly[t] > max_coeffs[t]:
                    max_coeffs[t] = poly[t]

                if poly[t] > canonical_poly[t]:
                    counterexample = {
                        "S": S,
                        "poly": poly,
                        "t": t,
                        "canonical_poly": canonical_poly,
                    }
                    break

            if counterexample is not None:
                break

        row = {
            "grid": f"{m}x{n}",
            "k": k,
            "checked": checked,
            "total": total,
            "canonical_poly": canonical_poly,
            "max_coeffs": tuple(max_coeffs),
            "passed": counterexample is None,
            "counterexample": counterexample,
        }

        results.append(row)

        if verbose:
            print(f"Grid {m}x{n}, k={k}")
            print(f"Checked {checked:,} / {total:,} k-sets")
            print("Canonical coefficient vector:", canonical_poly)
            print("Coefficientwise maxima:     ", tuple(max_coeffs))
            print("Passed?", counterexample is None)
            print()

    return results
