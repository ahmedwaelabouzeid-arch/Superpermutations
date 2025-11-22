import itertools

def overlap(a, b):
    """Return the maximum overlap length between suffix of a and prefix of b."""
    max_olap = 0
    for i in range(1, len(a)):
        if a.endswith(b[:i]):
            max_olap = i
    return max_olap

def greedy_superpermutation(n):
    perms = [''.join(p) for p in itertools.permutations(map(str, range(1, n + 1)))]
    result = perms[0]
    used = {perms[0]}
    
    current = perms[0]
    while len(used) < len(perms):
        best_perm = None
        best_overlap = -1
        for p in perms:
            if p in used:
                continue
            olap = overlap(current, p)
            if olap > best_overlap:
                best_overlap = olap
                best_perm = p
        result += best_perm[best_overlap:]
        used.add(best_perm)
        current = best_perm
    
    return result

if __name__ == "__main__":
    n = 5  # change this to 6 if you want to try n=6
    s = greedy_superpermutation(n)
    print(f"Greedy superpermutation for n={n}:\n{s}")
    print(f"Length = {len(s)}")
    print(f"Contains all {len(set([''.join(p) for p in itertools.permutations(map(str, range(1, n + 1)))))} permutations.")
