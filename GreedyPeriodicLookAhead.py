import itertools
import random
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed


# ==============================
# Helper functions
# ==============================

def compute_overlap(a, b):
    """Return overlap length between two permutations."""
    for i in range(1, len(a)):
        if a[i:] == b[:len(a)-i]:
            return len(a) - i
    return 0


def build_min_transition(perms):
    """Build minimum transition table (how many new chars needed)."""
    min_transition = {}
    for a in perms:
        min_transition[a] = {}
        for b in perms:
            if a == b:
                continue
            ov = compute_overlap(a, b)
            min_transition[a][b] = len(b) - ov
    return min_transition


def greedy_walk(start, unused, min_transition, steps=5):
    """Take greedy steps up to 5 moves ahead and return total cost."""
    total_cost = 0
    current = start
    unused_local = set(unused)

    for _ in range(steps):
        if not unused_local:
            break
        min_cost = min(min_transition[current][u] for u in unused_local)
        candidates = [u for u in unused_local if min_transition[current][u] == min_cost]
        next_node = random.choice(candidates)
        total_cost += min_transition[current][next_node]
        current = next_node
        unused_local.remove(next_node)

    return total_cost


def single_start(start, perms, min_transition):
    """Run greedy + branch lookahead from a single starting permutation."""
    unused = set(perms)
    unused.remove(start)
    current = start
    s = start
    step = 1

    while unused:
        # Every 5th edge: branch across all shortest edges, test 5-step lookahead
        if step % 5 == 0:
            min_cost = min(min_transition[current][u] for u in unused)
            candidates = [u for u in unused if min_transition[current][u] == min_cost]

            best_branch_cost = float('inf')
            best_next = None

            for cand in candidates:
                cost = greedy_walk(cand, unused - {cand}, min_transition, steps=5)
                if cost < best_branch_cost:
                    best_branch_cost = cost
                    best_next = cand

            next_cycle = best_next or random.choice(candidates)

        else:
            # Normal greedy step
            min_cost = min(min_transition[current][u] for u in unused)
            candidates = [u for u in unused if min_transition[current][u] == min_cost]
            next_cycle = random.choice(candidates)

        # Add overlap
        ov = compute_overlap(current, next_cycle)
        s += next_cycle[ov:]
        current = next_cycle
        unused.remove(next_cycle)
        step += 1

    return s, len(s)


# ==============================
# Multi-threaded search
# ==============================

def multi_threaded_superperm(perms, min_transition):
    best_string = None
    best_len = float('inf')

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(single_start, start, perms, min_transition) for start in perms]
        for f in as_completed(futures):
            s, l = f.result()
            found = {s[i:i+len(perms[0])] for i in range(len(s) - len(perms[0]) + 1)}
            valid = sum(1 for p in perms if p in found)
            if valid == len(perms) and l < best_len:
                best_len = l
                best_string = s

    return best_string, best_len


# ==============================
# Entry point
# ==============================

if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    n = 6
    perms = [''.join(p) for p in itertools.permutations('123456')]
    print(f"Generated {len(perms)} permutations for n={n}...")

    min_transition = build_min_transition(perms)
    print("Transition table built. Starting search...\n")

    best_string, best_len = multi_threaded_superperm(perms, min_transition)

    print("\n=== FINAL RESULT ===")
    if best_string:
        print(f"Shortest valid superpermutation for n={n}:")
        print(best_string)
        print(f"Length: {best_len}")
    else:
        print("No valid complete superpermutation found.")
