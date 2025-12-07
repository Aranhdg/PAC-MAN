import pygame
import sys
from collections import deque

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with Search Algorithms")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREY = (50, 50, 50)
RED = (255, 0, 0)

# Game settings
FPS = 5
GRID_SIZE = 40
PACMAN_SIZE = GRID_SIZE - 10

# Complex maze layout (1: Wall, 0: Path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Search algorithms
def dfs(start, goal, maze):
    stack = [(start, [start])]
    visited = set()

    while stack:
        (vertex, path) = stack.pop()
        if vertex == goal:
            return path

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = vertex[0] + direction[0], vertex[1] + direction[1]

            if (0 <= x < len(maze)) and (0 <= y < len(maze[0])) and maze[x][y] == 0:
                next_pos = (x, y)
                if next_pos not in visited:
                    visited.add(next_pos)
                    stack.append((next_pos, path + [next_pos]))

    return []

def bfs(start, goal, maze):
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        vertex, path = queue.popleft()
        if vertex == goal:
            return path

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = vertex[0] + direction[0], vertex[1] + direction[1]

            if (0 <= x < len(maze)) and (0 <= y < len(maze[0])) and maze[x][y] == 0:
                next_pos = (x, y)
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

    return []

def ids(start, goal, maze):
    def dls(node, goal, depth):
        if depth == 0 and node == goal:
            return [node]
        if depth > 0:
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x, y = node[0] + direction[0], node[1] + direction[1]
                if (0 <= x < len(maze)) and (0 <= y < len(maze[0])) and maze[x][y] == 0:
                    if (x, y) not in visited:
                        visited.add((x, y))
                        path = dls((x, y), goal, depth - 1)
                        if path:
                            return [node] + path
        return None

    for depth in range(len(maze) * len(maze[0])):
        visited = set()
        visited.add(start)
        path = dls(start, goal, depth)
        if path:
            return path

    return []

# Initial positions
pacman_start = (1, 1)
goal_pos = (9, 18)

# Choose an algorithm: 'dfs', 'bfs', 'ids'
algorithm = 'dfs'
if algorithm == 'dfs':
    path = dfs(pacman_start, goal_pos, maze)
elif algorithm == 'bfs':
    path = bfs(pacman_start, goal_pos, maze)
elif algorithm == 'ids':
    path = ids(pacman_start, goal_pos, maze)

def draw_grid():
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = GREY if maze[y][x] == 1 else BLUE
            pygame.draw.rect(WIN, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            if maze[y][x] == 0:
                pygame.draw.circle(WIN, WHITE, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 3)

def draw_pacman(pos):
    pygame.draw.circle(WIN, YELLOW, (pos[1] * GRID_SIZE + GRID_SIZE // 2, pos[0] * GRID_SIZE + GRID_SIZE // 2), PACMAN_SIZE // 2)

def draw_goal(pos):
    pygame.draw.circle(WIN, RED, (pos[1] * GRID_SIZE + GRID_SIZE // 2, pos[0] * GRID_SIZE + GRID_SIZE // 2), PACMAN_SIZE // 2 - 5)

def main():
    clock = pygame.time.Clock()
    current_step = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WIN.fill(BLACK)
        draw_grid()
        draw_goal(goal_pos)

        if current_step < len(path):
            current_pos = path[current_step]
            draw_pacman(current_pos)
            current_step += 1

        pygame.display.update()
        clock.tick(FPS)
print(len(maze))
if __name__ == "__main__":
    main()
print(len(maze))