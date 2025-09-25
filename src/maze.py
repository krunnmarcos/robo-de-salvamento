
class Maze:
    def __init__(self, filepath):
        self.maze = []
        self.start_pos = None
        self.start_direction = None
        self.human_pos = None
        self._load_maze(filepath)

    def _load_maze(self, filepath):
        with open(filepath, 'r') as f:
            for y, line in enumerate(f):
                row = []
                for x, char in enumerate(line.strip()):
                    row.append(char)
                    if char == 'E':
                        self.start_pos = (x, y)
                    elif char == '@':
                        self.human_pos = (x, y)
                self.maze.append(row)
        
        if self.start_pos[0] == 0:
            self.start_direction = 'E'
        elif self.start_pos[0] == len(self.maze[0]) - 1:
            self.start_direction = 'W'
        elif self.start_pos[1] == 0:
            self.start_direction = 'S'
        else:
            self.start_direction = 'N'


    def get_width(self):
        return len(self.maze[0])

    def get_height(self):
        return len(self.maze)

    def get_cell(self, x, y):
        if 0 <= y < len(self.maze) and 0 <= x < len(self.maze[y]):
            return self.maze[y][x]
        return 'X'  # Treat out of bounds as a wall

