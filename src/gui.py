import pygame

class GUI:
    def __init__(self, maze):
        pygame.init()
        self.maze = maze
        self.width = maze.get_width() * 20
        self.height = maze.get_height() * 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Rescue Robot')

    def draw(self, robot):
        self.screen.fill((255, 255, 255))

        for y in range(self.maze.get_height()):
            for x in range(self.maze.get_width()):
                cell = self.maze.get_cell(x, y)
                rect = pygame.Rect(x * 20, y * 20, 20, 20)
                if cell == 'X':
                    pygame.draw.rect(self.screen, (0, 0, 0), rect)
                elif cell == 'E':
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                elif cell == '@':
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)

        # Draw robot
        robot_rect = pygame.Rect(robot.x * 20, robot.y * 20, 20, 20)
        pygame.draw.rect(self.screen, (0, 0, 255), robot_rect)

        pygame.display.flip()
