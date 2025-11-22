import itertools
import concurrent.futures
import math

def overlap(a, b):
    """Return the max overlap length where end of a == start of b."""
    for i in range(1, len(a)):
        if a[i:] == b[:len(a)-i]:
            return len(a) - i
    return 0

def build_graph(perms):
    """Compute transition cost matrix (extra characters needed)."""
    n = len(perms)
    cost = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                ov = overlap(perms[i], perms[j])
                cost[i][j] = len(perms[j]) - ov
            else:
                cost[i][j] = float('inf')
    return cost

def build_superperm(perms, order):
    """Construct superpermutation string from the chosen order."""
    s = perms[order[0]]
    for i in range(1, len(order)):
        a, b = perms[order[i-1]], perms[order[i]]
        ov = overlap(a, b)
        s += b[ov:]
    return s

def greedy_tail(cost, start_index, remaining_indices):
    """Greedy search: always pick next permutation with lowest cost."""
    path = [start_index]
    visited = {start_index}
    curr = start_index
    while len(visited) < len(cost):
        best_j, best_c = None, math.inf
        for j in range(len(cost)):
            if j not in visited and cost[curr][j] < best_c:
                best_c = cost[curr][j]
                best_j = j
        path.append(best_j)
        visited.add(best_j)
        curr = best_j
    return path

def explore_branch(start_perm_index, remaining_indices, cost):
    """Worker function for each thread branch."""
    path = greedy_tail(cost, start_perm_index, remaining_indices)
    result = build_superperm(perms, path)
    return (len(result), path, result)

# === Data ===
start_perm = '613425'
remaining_perms = [ '134251', '342516', '425163', '251634', '516342', '163425', '634251', '342513', '425136', '251364', '513642', '136425', '364251', '642513', '425134', '251346', '513462', '134625', '346251', '462513', '625134', '251342', '513426', '134265', '342653', '426531', '265314', '653142', '531426', '314265', '142653', '426534', '265341', '653412', '534123', '341235', '412356', '123564', '235641', '356412', '564123', '641235', '412354', '123546', '235461', '354612', '546123', '461235', '612354', '123541', '235416', '354162', '541623', '416235', '162354', '623541', '235412', '354126', '541263', '412635', '126354', '263542', '635421', '354216', '542163', '421635', '216354', '163542', '635426', '354261', '542613', '426135', '261354', '613542', '135426', '354263', '542631', '426315', '263154', '631542', '315426', '154263', '542635', '426351', '263514', '635142', '351426', '514263', '142635', '426354', '263541', '635412', '354123', '541236', '412365', '123654', '236541', '365412', '654123']

# Combine and build cost matrix
perms = [start_perm] + remaining_perms
cost = build_graph(perms)
start_index = 0

# === Multithreaded Exploration ===
print("Exploring all greedy paths from 20 permutations using multi-threading...")

results = []
remaining_indices = list(range(1, len(perms)))

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    futures = []
    # Try different random orders of remaining perms to explore multiple possibilities
    for order in itertools.islice(itertools.permutations(remaining_indices, 3), 2000):
        # explore each possible 3-step prefix
        start_order = [start_index] + list(order)
        futures.append(executor.submit(explore_branch, start_index, remaining_indices, cost))
    
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

# Get best result
best_len, best_path, best_result = min(results, key=lambda x: x[0])

print("\n✅ Best superpermutation tail found:")
print("Length:", best_len)
print("Order:", [perms[i] for i in best_path])
print("Superpermutation tail:\n", best_result)
