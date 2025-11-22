import itertools
import heapq

def overlap(a, b):
    """Return the largest suffix of a that matches a prefix of b."""
    for i in range(len(a)):
        if b.startswith(a[i:]):
            return len(a) - i
    return 0

def build_graph(perms):
    n = len(perms[0])
    graph = {p: [] for p in perms}
    for a in perms:
        for b in perms:
            if a != b:
                ov = overlap(a, b)
                cost = n - ov
                graph[a].append((cost, b))
    return graph

def dijkstra_superperm(n):
    perms = [''.join(p) for p in itertools.permutations(map(str, range(1, n+1)))]
    graph = build_graph(perms)

    # Dijkstra-style state: (total_length, current_perm, visited_mask, current_string)
    start = perms[0]
    heap = [(len(start), start, 1 << 0, start)]
    seen = {}

    while heap:
        length, node, mask, seq = heapq.heappop(heap)
        if mask == (1 << len(perms)) - 1:
            return seq  # Found full coverage
        if (node, mask) in seen and seen[(node, mask)] <= length:
            continue
        seen[(node, mask)] = length

        for cost, nxt in graph[node]:
            idx = perms.index(nxt)
            new_mask = mask | (1 << idx)
            ov = overlap(node, nxt)
            new_seq = seq + nxt[ov:]
            heapq.heappush(heap, (len(new_seq), nxt, new_mask, new_seq))

def check_superperm(s, n):
    perms = [''.join(p) for p in itertools.permutations(map(str, range(1, n+1)))]
    missing = [p for p in perms if p not in s]
    print(f"n={n} | Length={len(s)}")
    print("Contains all permutations:", len(missing) == 0)
    if missing:
        print("Missing:", missing)

# Run the algorithm
n = 4  # Try 3 or 4 first
result = dijkstra_superperm(n)
check_superperm(result, n)
print("Shortest superpermutation:", result)
