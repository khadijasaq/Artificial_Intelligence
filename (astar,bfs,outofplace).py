import heapq
import time

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def enqueue(self, x):
        heapq.heappush(self.elements, x)

    def dequeue(self):
        return heapq.heappop(self.elements)

    def is_empty(self):
        return len(self.elements) == 0

class Node:
    def __init__(self, state, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.g = g  # Cost to reach this node
        self.h = self.heuristic()
        self.f = self.g + self.h  # Total cost for A*

    def __lt__(self, other):
        return self.f < other.f

    def heuristic(self):
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Goal state
        count = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0 and self.state[i][j] != goal[i][j]:
                    count += 1
        return count

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.state])

class PuzzleSolver:
    def __init__(self, start):
        self.start = Node(start)

    def find_space(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)

    def find_moves(self, pos):
        x, y = pos
        moves = []
        if x > 0: moves.append((-1, 0))  # Up
        if x < 2: moves.append((1, 0))   # Down
        if y > 0: moves.append((0, -1))  # Left
        if y < 2: moves.append((0, 1))   # Right
        return moves

    def find_children(self, node):
        space = self.find_space(node.state)
        moves = self.find_moves(space)
        children = []
        for move in moves:
            new_state = self.play_move(node.state, move, space)
            children.append(Node(new_state, parent=node, g=node.g + 1))
        return children

    def play_move(self, state, move, space):
        new_state = [row[:] for row in state]  # Deep copy
        x, y = space
        dx, dy = move
        new_state[x][y], new_state[x+dx][y+dy] = new_state[x+dx][y+dy], new_state[x][y]
        return new_state

    def solve_puzzle(self):
        pq = PriorityQueue()
        pq.enqueue(self.start)
        explored = set()

        while not pq.is_empty():
            node = pq.dequeue()
            explored.add(str(node.state))

            if node.heuristic() == 0:
                return self.print_solution(node)

            for child in self.find_children(node):
                if str(child.state) not in explored:
                    pq.enqueue(child)

        return None

    def print_solution(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

ps = PuzzleSolver([[4, 7, 8], [3, 6, 5], [1, 2, 0]])
#solution = ps.solve_puzzle()
start_time=time.time()
solution = ps.solve_puzzle()
end_time=time.time()

executiontime=end_time-start_time
print("The time taken is ",executiontime,"\n")

if solution:
    for state in solution:
        for row in state:
            print(row)
        print()
else:
    print("No solution found.")
# Write your code here :-)
