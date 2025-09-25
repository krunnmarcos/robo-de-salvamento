from maze import Maze
import heapq

class Robot:
    def __init__(self, maze):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = maze.start_direction
        self.internal_map = {}
        self.path = []
        self.carrying_human = False
        self.log = []
        self.log.append(('LIGAR', *self.get_sensor_readings_for_log(), self.get_carrying_status_for_log()))

    def get_sensor_readings(self):
        readings = {}
        # Sensor directions are relative to the robot's current direction
        if self.direction == 'N':
            sensor_dirs = {'left': 'W', 'front': 'N', 'right': 'E'}
        elif self.direction == 'E':
            sensor_dirs = {'left': 'N', 'front': 'E', 'right': 'S'}
        elif self.direction == 'S':
            sensor_dirs = {'left': 'E', 'front': 'S', 'right': 'W'}
        elif self.direction == 'W':
            sensor_dirs = {'left': 'S', 'front': 'W', 'right': 'N'}

        for sensor, direction in sensor_dirs.items():
            if direction == 'N':
                nx, ny = self.x, self.y - 1
            elif direction == 'E':
                nx, ny = self.x + 1, self.y
            elif direction == 'S':
                nx, ny = self.x, self.y + 1
            elif direction == 'W':
                nx, ny = self.x - 1, self.y
            
            cell = self.maze.get_cell(nx, ny)
            if cell == ' ':
                readings[sensor] = 'VAZIO'
            elif cell == 'X':
                readings[sensor] = 'PAREDE'
            elif cell == '@':
                readings[sensor] = 'HUMANO'
            else:
                readings[sensor] = 'VAZIO'


        return readings

    def get_sensor_readings_for_log(self):
        readings = self.get_sensor_readings()
        return readings['left'], readings['front'], readings['right']

    def get_carrying_status_for_log(self):
        return 'COM HUMANO' if self.carrying_human else 'SEM HUMANO'

    def turn_right(self):
        self.path.append('G')
        if self.direction == 'N':
            self.direction = 'E'
        elif self.direction == 'E':
            self.direction = 'S'
        elif self.direction == 'S':
            self.direction = 'W'
        elif self.direction == 'W':
            self.direction = 'N'
        self.log.append(('G', *self.get_sensor_readings_for_log(), self.get_carrying_status_for_log()))

    def move_forward(self):
        self.path.append('A')
        if self.direction == 'N':
            self.y -= 1
        elif self.direction == 'E':
            self.x += 1
        elif self.direction == 'S':
            self.y += 1
        elif self.direction == 'W':
            self.x -= 1
        self.internal_map[(self.x, self.y)] = self.maze.get_cell(self.x, self.y)
        self.log.append(('A', *self.get_sensor_readings_for_log(), self.get_carrying_status_for_log()))

    def pick_up(self):
        self.path.append('P')
        self.carrying_human = True
        self.log.append(('P', *self.get_sensor_readings_for_log(), self.get_carrying_status_for_log()))

    def eject(self):
        self.path.append('E')
        self.carrying_human = False
        self.log.append(('E', *self.get_sensor_readings_for_log(), self.get_carrying_status_for_log()))

    def explore(self):
        if not self.carrying_human:
            sensors = self.get_sensor_readings()

            if sensors['front'] == 'HUMANO':
                self.move_forward()
                self.pick_up()

            elif sensors['right'] == 'HUMANO':
                self.turn_right()
                self.move_forward()
                self.pick_up()

            elif sensors['left'] == 'HUMANO':
                self.turn_left()
                self.move_forward()
                self.pick_up()

            elif sensors['right'] != 'PAREDE':
                self.turn_right()
                self.move_forward()
            elif sensors['front'] != 'PAREDE':
                self.move_forward()
            else:
                self.turn_left()

    def turn_left(self):
        self.turn_right()
        self.turn_right()
        self.turn_right()

    def return_to_exit(self):
        path = self.a_star((self.x, self.y), self.maze.start_pos)
        if path:
            for next_pos in path:
                dx = next_pos[0] - self.x
                dy = next_pos[1] - self.y

                if dx == 1:
                    target_direction = 'E'
                elif dx == -1:
                    target_direction = 'W'
                elif dy == 1:
                    target_direction = 'S'
                else:
                    target_direction = 'N'

                while self.direction != target_direction:
                    self.turn_right()
                
                self.move_forward()

            self.eject()

    def a_star(self, start, end):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end:
                return self.reconstruct_path(came_from, current)

            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if not self.is_valid_neighbor(neighbor):
                    continue

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def is_valid_neighbor(self, pos):
        # Use the robot's internal map for pathfinding
        if self.internal_map.get(pos, ' ') == 'X':
            return False
        
        # "No three walls" constraint
        wall_count = 0
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            if self.internal_map.get((pos[0] + dx, pos[1] + dy), ' ') == 'X':
                wall_count += 1
        if wall_count >= 3:
            return False

        return True

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[1:][::-1]