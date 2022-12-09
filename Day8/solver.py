"""
30373
25512
65332
33549
35390

With 16 trees visible on the edge and another 5 visible in the interior,
a total of 21 trees are visible in this arrangement.
"""
import sys

def is_visible(trees, x, y):
    # On the edge, visible.
    if x == 0 or x == len(trees) - 1 or y == 0 or y == len(trees[x]) - 1:
        return True
    height = trees[x][y]

    if height > max(trees[x][y+1:]) or height > max(trees[x][:y]):
        return True
    if height > max([row[y] for row in trees[:x]]) or height > max([row[y] for row in trees[x+1:]]):
        return True
    return False

def count_trees_visible(trees, x, y):
   
    # Count trees visible from the right
    count = 0
    for i in range(y+1, len(trees[x])):
        count += 1
        if trees[x][i] >= trees[x][y]:
            break
    product = count

    # Count trees visible from the left
    count = 0
    for i in range(y-1, -1, -1):
        count += 1
        if trees[x][i] >= trees[x][y]:
            break
    product *= count

    # Count trees visible from above
    count = 0
    for i in range(x-1, -1, -1):
        count += 1
        if trees[i][y] >= trees[x][y]:
            break
    product *= count
    
    # Count trees visible from below
    count = 0
    for i in range(x+1, len(trees)):
        count += 1
        if trees[i][y] >= trees[x][y]:
            break
    product *= count
    
    return product

          
def main(filename):
    # Read input
    trees = []
    for line in open(filename):
        trees.append(list(map(int, [*line.strip()])))

    # Part 1
    count = 0
    for x, _ in enumerate(trees):
        for y, _ in enumerate(trees[x]):
            count += 1 if is_visible(trees, x, y) else 0
    print(count)

    # Part 2
    score = [count_trees_visible(trees, x, y) for x, _ in enumerate(trees) for y, _ in enumerate(trees[x])]
    print(max(score))

        

        
            


if __name__ == '__main__':
    main(len(sys.argv) == 2 and sys.argv[1] or "input.txt")