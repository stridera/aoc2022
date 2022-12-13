import sys
import json
import functools


def log(*args):
    if False:
        print(*args, file=sys.stderr)


def compare(l, r, idx=0) -> int:
    """Compare two lists.  Returns 0 if they are equal, positive if in the right order, neg otherwise."""
    log(f"{'  '*idx}- Comparing {l} vs {r}")

    # Simple case of two ints.  Compare and move on.
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            log(f"{'  '*idx}  - Left side is smaller, so inputs are in the right order")
        elif l > r:
            log(f"{'  '*idx}  - Right side is smaller, so inputs are NOT in the right order")
        return r - l

    # Check for cases where one side is a list but the other is not.
    if isinstance(l, list) and isinstance(r, int):
        log(f"{'  '*idx}  - Mixed types; convert right to [{r}] and retry comparison")
        return compare(l, [r], idx+1)
    elif isinstance(l, int) and isinstance(r, list):
        log(f"{'  '*idx}  - Mixed types; convert left to [{l}] and retry comparison")
        return compare([l], r, idx+1)
    else:
        # Loop over the lists, comparing each item.
        for i in range(max(len(l), len(r))):
            if i >= len(l):
                log(f"{'  '*idx} Left side ran out of items, so inputs are in the right order")
                return idx+1
            elif i >= len(r):
                log(f"{'  '*idx} Right side ran out of items, so inputs are NOT in the right order")
                return -1

            result = compare(l[i], r[i], idx+1)
            if result != 0:
                return result

    return 0


def main(test):

    if test:
        print("Testing")
        filename = "test.txt"
    else:
        filename = "input.txt"

    print("Part 1")
    results = []
    for idx, pairs in enumerate(open(filename).read().split('\n\n')):
        log(f"\n== Pair {idx+1}: ==")
        l, r = pairs.split("\n")
        if compare(json.loads(l), json.loads(r)) > 0:
            results.append(idx+1)

    log("Results:", results)
    if test:
        assert sum(results) == 13, f"Expected 13, got {sum(results)}"
        print("Tests passed")
    print("Final:", sum(results))

    print("Part 2")

    packets = [[[2]], [[6]]]
    for line in open(filename):
        if line.strip():
            packets.append(json.loads(line))

    decoder_keys = []
    for idx, packet in enumerate(sorted(packets, key=functools.cmp_to_key(compare), reverse=True)):
        log(packet)
        if packet == [[6]] or packet == [[2]]:
            decoder_keys.append(idx+1)

    log("Decoder keys:", decoder_keys)
    results = functools.reduce(lambda x, y: x*y, decoder_keys)
    if test:
        assert results == 140, f"Expected 140, got {results}"
        print("Tests passed")
    print("Final:", results)


if __name__ == "__main__":
    main(len(sys.argv) == 2 and sys.argv[1] == "test")
