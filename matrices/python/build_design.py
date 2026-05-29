import numpy as np

def load_exponent_matrix(path):
    """Load an exponent matrix (0..k-1) from a text file."""
    with open(path, "r") as f:
        rows = [list(map(int, line.split())) for line in f]
    return np.array(rows, dtype=int)

def build_associated_design(E, k):
    """
    Build the associated design A_H from exponent matrix E (n x n)
    as defined in Egan–Flannery–Ó Catháin (2015).
    Output is an (n*k) x (n*k) 0–1 matrix.
    """
    n = E.shape[0]
    A = np.zeros((n*k, n*k), dtype=int)

    for i in range(n):
        for j in range(n):
            # exponent e_ij
            e = E[i, j]

            # block position
            row_block = i * k
            col_block = j * k

            # fill the block: a 1 in position (e, 0) shifted mod k
            # This encodes the relation x_j = x_i + e (mod k)
            A[row_block + e, col_block + 0] = 1

    return A

def save_design(A, path):
    """Save A_H as a 0–1 adjacency matrix."""
    np.savetxt(path, A, fmt="%d")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python build_design.py <H.txt> <k> <output.txt>")
        exit(1)

    H_path = sys.argv[1]
    k = int(sys.argv[2])
    out_path = sys.argv[3]

    E = load_exponent_matrix(H_path)
    A = build_associated_design(E, k)
    save_design(A, out_path)
