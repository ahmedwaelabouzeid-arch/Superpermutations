import itertools

def overlap(a, b):
    """Return overlap length between end of a and start of b."""
    for i in range(1, len(a)):
        if a[i:] == b[:len(a)-i]:
            return len(a) - i
    return 0

def make_superperm(n):
    perms = [''.join(p) for p in itertools.permutations([str(i) for i in range(1, n+1)])]
    min_length = float('inf')
    best_superperm = None

    # Precompute overlaps to speed up
    overlaps = {}
    for a in perms:
        overlaps[a] = {}
        for b in perms:
            if a != b:
                overlaps[a][b] = overlap(a, b)
            else:
                overlaps[a][b] = 0

    # Try starting from each permutation
    for start in perms:
        unused = set(perms)
        unused.remove(start)
        s = start
        current = start

        while unused:
            # choose next with maximum overlap (min extra chars)
            next_perm = max(unused, key=lambda x: overlaps[current][x])
            ov = overlaps[current][next_perm]
            s += next_perm[ov:]
            current = next_perm
            unused.remove(next_perm)

        if len(s) < min_length:
            min_length = len(s)
            best_superperm = s
            print(f"New best from {start}: length {len(s)}")

    print("\n=== Result ===")
    print(f"Shortest superpermutation found: {min_length}")
    print(f"String: {best_superperm[:200]}...")  # show start only
    print(f"Total length: {len(best_superperm)}")

    # Verify
    count = sum(1 for p in perms if p in best_superperm)
    print(f"Contains {count}/{len(perms)} permutations")
    if count == len(perms):
        print("✅ Contains all permutations!")
    else:
        print("❌ Missing permutations.")

make_superperm(6)  # change to 6 later if it's too slow
