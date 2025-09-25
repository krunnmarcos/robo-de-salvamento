import argparse
import csv
import pygame
from .maze import Maze
from .robot import Robot
from .gui import GUI

def main():
    parser = argparse.ArgumentParser(description='Rescue Robot')
    parser.add_argument('maze_file', help='Path to the maze file')
    args = parser.parse_args()

    maze = Maze(args.maze_file)
    robot = Robot(maze)
    gui = GUI(maze)

    running = True
    exploring = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if exploring:
            robot.explore()
            if robot.carrying_human:
                exploring = False
        else:
            robot.return_to_exit()
            running = False

        gui.draw(robot)
        pygame.time.delay(100)

    # Log generation
    log_file = args.maze_file.replace('.txt', '.csv')
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Comando enviado', 'Leitura do sensor do lado esquerdo do robô após execução do comando', 'Leitura do sensor da frente do robô após execução do comando', 'Leitura do sensor do lado direito do robô após execução do comando', 'Situação do compartimento de carga'])
        writer.writerows(robot.log)

    pygame.quit()

if __name__ == '__main__':
    main()
