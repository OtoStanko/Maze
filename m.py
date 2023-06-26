import random
import matplotlib.pyplot as plt


class Unit:
    def __init__(self):
        self.visited = False
        self.r = None
        self.l = None
        self.u = None
        self.d = None
        self.dist = 0
        

def getAdjUnvisitedNodes(m, pos):
    k = len(m)
    x, y = pos
    nodes = []
    if x-1 >= 0 and not m[x-1][y].visited:
        nodes.append((x-1, y))
    if x+1 < k and not m[x+1][y].visited:
        nodes.append((x+1, y))
    if y-1 >= 0 and not m[x][y-1].visited:
        nodes.append((x, y-1))
    if y+1 < k and not m[x][y+1].visited:
        nodes.append((x, y+1))
    return nodes

def createPath(u1, u2, pos1, pos2):
    if pos1[0] == pos2[0]:
        if pos1[1] < pos2[1]:
            u1.u = u2
            u2.d = u1
        else:
            u1.d = u2
            u2.u = u1
    else:
        if pos1[0] < pos2[0]:
            u1.r = u2
            u2.l = u1
        else:
            u1.l = u2
            u2.r = u1

def visualize_grid(grid):
    k = len(grid)
    fig, ax = plt.subplots()

    for i in range(k):
        for j in range(k):
            unit = grid[i][j]
            # j 2   i 1 left
            if unit.r is None:
                ax.plot([i+1, i+1], [j, j+1], color='black')
            if unit.l is None:
                ax.plot([i, i], [j, j+1], color='black')
            if unit.d is None:
                ax.plot([i, i+1], [j, j], color='black')
            if unit.u is None:
                ax.plot([i, i+1], [j+1, j+1], color='black')
            if unit.dist % k == 0:
                ax.text(i + 0.5, j + 0.5, str(unit.dist), ha='center', va='center')

    ax.set_xlim([0, k])
    ax.set_ylim([0, k])
    ax.set_aspect('equal', 'box')
    ax.set_xticks(range(k + 1))
    ax.set_yticks(range(k + 1))
    ax.set_xticklabels(range(k + 1))
    ax.set_yticklabels(range(k + 1))
    ax.tick_params(axis='both', which='both', length=0)

    plt.show()

def delete_tuples_after(lst, target_tuple):
    filtered_lst = []
    found_target = False

    for t in lst:
        if t == target_tuple:
            found_target = True

        if not found_target:
            filtered_lst.append(t)

    return filtered_lst

def find_highest(m):
    k = len(m)
    max_x, max_y = (0, 0)
    max_dist = m[max_x][max_y].dist
    for i in range(k):
        for j in range(k):
            x, y, = (i, j)
            if m[x][y].dist > max_dist:
                max_dist = m[x][y].dist
                max_x, max_y = x, y
    return (max_x, max_y), max_dist

def find_highest_on_boarder(m):
    k = len(m)
    max_x, max_y = (0, 0)
    max_dist = m[max_x][max_y].dist
    for i in range(k):
        x, y, = (0, i)
        if m[x][y].dist > max_dist:
            max_dist = m[x][y].dist
            max_x, max_y = x, y
        x, y, = (k-1, i)
        if m[x][y].dist > max_dist:
            max_dist = m[x][y].dist
            max_x, max_y = x, y
        x, y, = (i, 0)
        if m[x][y].dist > max_dist:
            max_dist = m[x][y].dist
            max_x, max_y = x, y
        x, y, = (i, k-1)
        if m[x][y].dist > max_dist:
            max_dist = m[x][y].dist
            max_x, max_y = x, y
    return (max_x, max_y), max_dist

k = 15
m = [[Unit() for j in range(k)] for i in range(k)]

pos = (0, 0)
path = [pos]
i = 0
while True:
    node = m[pos[0]][pos[1]]
    node.visited = True
    node.dist = i
    available = getAdjUnvisitedNodes(m, pos)
    #print('p', path)
    #print('a', available)
    if len(available) == 0:
        for visited in path[::-1]:
            available = getAdjUnvisitedNodes(m, visited)
            if len(available) != 0:
                # delete path that has been traversed
                path = delete_tuples_after(path, visited)
                #print('b', available)
                pos = visited
                node = m[pos[0]][pos[1]]
                i = node.dist
                break
    if len(available) == 0:
        break
    direction = random.randint(0, len(available)-1)
    next_pos = available[direction]
    createPath(node, m[next_pos[0]][next_pos[1]], pos, next_pos)
    pos = next_pos
    i += 1
    path.append(pos)

print(find_highest(m))
print(find_highest_on_boarder(m))
visualize_grid(m)
