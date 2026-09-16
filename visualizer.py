"""
=============================================================================
PROJECT:  PATHFINDING VISUALIZER MATRIX ENGINE (V1.0.0-PROD)
TARGET:   Python 3.9+ Runtime Environment
PARADIGM: Object-Oriented Programming (OOP) & Graph Traversal Graph Mathematics
=============================================================================
"""

class Node:
    """Represents an individual spatial coordinate cell unit within the 2D grid matrix."""
    def __init__(self, row: int, col: int, width: float, total_rows: int):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.is_obstacle = False
        self.is_start_node = False
        self.is_target_node = False
        self.is_closed_set = False
        self.is_open_set = False
        self.parent_pointer = None
        self.neighbors = []

    def get_coordinate_vector(self) -> tuple[int, int]:
        return self.row, self.col

    def reset_state_matrix(self):
        self.is_obstacle = False
        self.is_closed_set = False
        self.is_open_set = False
        self.parent_pointer = None

    def update_neighbors(self, grid_matrix: list[list['Node']], total_rows: int):
        self.neighbors = []
        if self.row < total_rows - 1 and not grid_matrix[self.row + 1][self.col].is_obstacle:
            self.neighbors.append(grid_matrix[self.row + 1][self.col])
        if self.row > 0 and not grid_matrix[self.row - 1][self.col].is_obstacle:
            self.neighbors.append(grid_matrix[self.row - 1][self.col])
        if self.col < total_rows - 1 and not grid_matrix[self.row][self.col + 1].is_obstacle:
            self.neighbors.append(grid_matrix[self.row][self.col + 1])
        if self.col > 0 and not grid_matrix[self.row][self.col - 1].is_obstacle:
            self.neighbors.append(grid_matrix[self.row][self.col - 1])

def make_grid(rows: int, width: int) -> list[list[Node]]:
    grid_matrix = []
    gap = width // rows
    for i in range(rows):
        grid_matrix.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid_matrix[i].append(node)
    return grid_matrix

def draw_grid_lines(window_surface, rows: int, width: int):
    import pygame
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window_surface, (128, 128, 128), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window_surface, (128, 128, 128), (j * gap, 0), (j * gap, width))

def draw(window_surface, grid_matrix: list[list[Node]], rows: int, width: int):
    import pygame
    window_surface.fill((255, 255, 255))
    for row in grid_matrix:
        for node in row:
            color = (255, 255, 255)
            if node.is_obstacle:
                color = (0, 0, 0)
            elif node.is_start_node:
                color = (255, 165, 0)
            elif node.is_target_node:
                color = (64, 224, 208)
            elif node.is_closed_set:
                color = (255, 192, 203)
            elif node.is_open_set:
                color = (144, 238, 144)
            gap = width // rows
            pygame.draw.rect(window_surface, color, (node.x, node.y, gap, gap))
    draw_grid_lines(window_surface, rows, width)
    pygame.display.update()

def get_clicked_position(pixel_position: tuple[int, int], rows: int, width: int) -> tuple[int, int]:
    gap = width // rows
    y_pixel, x_pixel = pixel_position
    return y_pixel // gap, x_pixel // gap

def run_bfs_algorithm(draw_callback, grid_matrix: list[list[Node]], start_node: Node, target_node: Node) -> bool:
    import pygame
    from collections import deque
    search_queue = deque([start_node])
    visited_set = {start_node}
    while len(search_queue) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        current_node = search_queue.popleft()
        if current_node == target_node:
            path_tracer = target_node.parent_pointer
            while path_tracer and path_tracer != start_node:
                path_tracer.is_closed_set = False
                path_tracer.is_open_set = False
                path_tracer.parent_pointer = path_tracer.parent_pointer
                path_tracer = path_tracer.parent_pointer
            return True
        for neighbor in current_node.neighbors:
            if neighbor not in visited_set and not neighbor.is_obstacle:
                neighbor.parent_pointer = current_node
                visited_set.add(neighbor)
                search_queue.append(neighbor)
                if neighbor != target_node:
                    neighbor.is_open_set = True
        if current_node != start_node:
            current_node.is_closed_set = True
            current_node.is_open_set = False
        draw_callback()
    return False

def main():
    import pygame
    pygame.init()
    WINDOW_WIDTH = 800
    GRID_ROWS = 50
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
    pygame.display.set_caption("Waterloo Portfolio Project: Algorithmic Matrix Engine")
    grid_matrix = make_grid(GRID_ROWS, WINDOW_WIDTH)
    start_node = None
    target_node = None
    is_running = True

    while is_running:
        draw(window_surface, grid_matrix, GRID_ROWS, WINDOW_WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if pygame.mouse.get_pressed()[0]:  # Left Click
                position = pygame.mouse.get_pos()
                row, col = get_clicked_position(position, GRID_ROWS, WINDOW_WIDTH)
                if 0 <= row < GRID_ROWS and 0 <= col < GRID_ROWS:
                    node = grid_matrix[row][col]
                    if not start_node and node != target_node:
                        start_node = node
                        start_node.is_start_node = True
                    elif not target_node and node != start_node:
                        target_node = node
                        target_node.is_target_node = True
                    elif node != start_node and node != target_node:
                        node.is_obstacle = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and target_node:
                    for r in grid_matrix:
                        for n in r:
                            n.update_neighbors(grid_matrix, GRID_ROWS)
                    run_bfs_algorithm(lambda: draw(window_surface, grid_matrix, GRID_ROWS, WINDOW_WIDTH), 
                                      grid_matrix, start_node, target_node)
                if event.key == pygame.K_c:
                    start_node = None
                    target_node = None
                    grid_matrix = make_grid(GRID_ROWS, WINDOW_WIDTH)
    pygame.quit()

if __name__ == "__main__":
    main()
