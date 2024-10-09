import sys
import time
from copy import deepcopy

import pygame
import pygame.freetype

import constants
from commands.go_straight_command import StraightCommand
from commands.scan_obstacle_command import ScanCommand
from commands.turn_command import TurnCommand
from misc.direction import Direction
from misc.type_of_turn import TypeOfTurn


class Simulation:

    def __init__(self):
        pygame.init()
        self.running = True
        self.font = pygame.font.Font("fonts/Formula1-Regular.ttf", 20)
        self.screen = pygame.display.set_mode((800, 650), pygame.RESIZABLE)
        self.clock = None
        pygame.mouse.set_visible(True)
        pygame.display.set_caption("MDP 34 GRAND PRIX SIMULATOR")
        self.screen.fill(constants.DEEP_BLUE)
        self.drawGridBackground()

    def reset(cls, bot):
        cls.screen.fill(constants.DEEP_BLUE)
        cls.drawGridBackground()
        currentPosX = bot.get_current_pos().x
        currentPosY = bot.get_current_pos().y
        direction = bot.get_current_pos().direction
        currentPos = (
            (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - currentPosX) // 10,
            currentPosY // 10,
            direction,
        )
        cls.bot.setCurrentPos(currentPos[0], currentPos[1], currentPos[2])
        cls.bot.hamiltonian.commands.clear()

    def selectObstacles(cls, y, x, cellSize, color):
        newRect = pygame.Rect(y * cellSize, x * cellSize, cellSize, cellSize)
        cls.screen.fill(color, newRect)
        pygame.draw.rect(cls.screen, color, newRect, 2)

    def drawRobot(cls, robotPos, cellSize, directionColor, botColor, botAreaColor):
        for x in range(robotPos[0] - 1, robotPos[0] + 2):
            for y in range(robotPos[1] - 1, robotPos[1] + 2):
                if (
                    0 <= x * cellSize < constants.GRID_LENGTH * constants.SCALING_FACTOR
                ) and (
                    0 <= y * cellSize < constants.GRID_LENGTH * constants.SCALING_FACTOR
                ):
                    if robotPos[0] == x and robotPos[1] == y:
                        cls.selectObstacles(
                            robotPos[1], robotPos[0], cellSize, botColor
                        )
                        if robotPos[2] == Direction.TOP:
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize,
                                robotPos[0] * cellSize,
                                cellSize,
                                5,
                            )
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == Direction.RIGHT:
                            imageSide = pygame.Rect(
                                (robotPos[1] * cellSize) + cellSize - 5,
                                (robotPos[0] * cellSize),
                                5,
                                cellSize,
                            )
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == Direction.BOTTOM:
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize,
                                (robotPos[0] * cellSize) + cellSize - 5,
                                cellSize,
                                5,
                            )
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == Direction.LEFT:
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize,
                                robotPos[0] * cellSize,
                                5,
                                cellSize,
                            )
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(cls.screen, directionColor, imageSide, 5)
                    else:
                        rect = pygame.Rect(
                            y * cellSize, x * cellSize, cellSize, cellSize
                        )
                        cls.screen.fill(botAreaColor, rect)
                        pygame.draw.rect(cls.screen, botAreaColor, rect, 1)

    def drawGridBackground(cls):
        for x in range(
            0,
            constants.GRID_LENGTH * constants.SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
        ):
            for y in range(
                0,
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            ):
                rect = pygame.Rect(
                    y,
                    x,
                    constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                )
                cls.screen.fill(constants.GREY, rect)

    def drawGrid(cls):
        for x in range(
            0,
            constants.GRID_LENGTH * constants.SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
        ):
            for y in range(
                0,
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            ):
                #rect = pygame.Rect(
                #    y,
                #    x,
                #    constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                #    constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                #)
                #cls.screen.fill(constants.WHITE, rect)
                if (
                    x
                    > (constants.GRID_LENGTH - 5 * constants.GRID_CELL_LENGTH)
                    * constants.SCALING_FACTOR
                ) and (y < 4 * constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR):
                    rect = pygame.Rect(
                        y,
                        x,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                    cls.screen.fill(constants.ORANGE, rect)
                    pygame.draw.rect(cls.screen, constants.ORANGE, rect, 2)
                rect = pygame.Rect(
                    y,
                    x,
                    constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                )
                #cls.screen.fill(constants.WHITE, rect)
                pygame.draw.rect(cls.screen, constants.BLACK, rect, 1)

    def drawButtons(cls, xpos, ypos, bgcolor, text, textColor, length, width):
        startButton = pygame.Rect(xpos, ypos, length, width)
        pygame.draw.rect(cls.screen, bgcolor, startButton)
        text = cls.font.render(text, True, textColor)
        cls.screen.blit(
            text,
            text.get_rect(
                center=(startButton.x + (length // 2), startButton.y + (width // 2))
            ),
        )

    def drawImage(cls, image, xpos, ypos, bgcolor, length, width):
        rect = image.get_rect()
        rect.center = (xpos + (length // 2), ypos + (width // 2))
        cls.screen.blit(image, rect)

    def drawObstaclesButton(cls, obstacles, color):
        size = constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR
        for i in obstacles:
            y = (
                constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - i.position.y
            ) // constants.GRID_CELL_LENGTH
            # x = i.position.x // constants.GRID_CELL_LENGTH
            x = i.position.x // constants.GRID_CELL_LENGTH
            direction = i.position.direction
            cls.selectObstacles(
                x,
                y,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                constants.GOLD,
            )

            if direction == Direction.TOP:
                imageSide = pygame.Rect(x * size, y * size, size, 5)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            elif direction == Direction.RIGHT:
                imageSide = pygame.Rect((x * size) + size - 5, (y * size), 5, size)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            elif direction == Direction.BOTTOM:
                imageSide = pygame.Rect(x * size, (y * size) + size - 5, size, 5)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            elif direction == Direction.LEFT:
                imageSide = pygame.Rect(x * size, y * size, 5, size)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)

        img = pygame.image.load("images/MoveForward.png").convert()
        cls.drawImage(img, 685, 110, constants.GREY, size, size)  # Forward N
        img = pygame.image.load("images/MoveBackward.png").convert()
        cls.drawImage(img, 685, 180, constants.GREY, size, size)  # Backward S

        img = pygame.image.load("images/TurnForwardRight.png").convert()
        cls.drawImage(img, 720, 132.5, constants.GREY, size, size)  # Forward E
        img = pygame.image.load("images/TurnForwardLeft.png").convert()
        cls.drawImage(img, 650, 132.5, constants.GREY, size, size)  # Forward W
        img = pygame.image.load("images/TurnReverseRight.png").convert()
        cls.drawImage(img, 720, 160, constants.GREY, size, size)  # Backward E
        img = pygame.image.load("images/TurnReverseLeft.png").convert()
        cls.drawImage(img, 650, 160, constants.GREY, size, size)  # Backward W

        img = pygame.image.load("images/slantForwardRight.png").convert()
        cls.drawImage(img, 720, 107.5, constants.GREY, size, size)  # Slant Forward E
        img = pygame.image.load("images/slantForwardLeft.png").convert()
        cls.drawImage(img, 650, 107.5, constants.GREY, size, size)  # Slant Forward W
        img = pygame.image.load("images/slantBackwardsRight.png").convert()
        cls.drawImage(img, 720, 182.5, constants.GREY, size, size)  # Slant Backward E
        img = pygame.image.load("images/slantBackwardsLeft.png").convert()
        cls.drawImage(img, 650, 182.5, constants.GREY, size, size)  # Slant Backward W

    def moveForward(self, gridSize, cellSize):
        steps = 1
        if self.currentPos[2] == Direction.TOP:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (self.currentPos[0] - steps) * cellSize < gridSize) and (
                0 <= self.currentPos[1] * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0] - steps, self.currentPos[1], self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.RIGHT:
            # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (x == i) and (self.currentPos[1] + 2 == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= self.currentPos[0] * cellSize < gridSize) and (
                0 <= (self.currentPos[1] + steps) * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0], self.currentPos[1] + steps, self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] + 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (self.currentPos[0] + steps) * cellSize < gridSize) and (
                0 <= self.currentPos[1] * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0] + steps, self.currentPos[1], self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.LEFT:
            # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (x == i) and (self.currentPos[1] - 2 == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= self.currentPos[0] * cellSize < gridSize) and (
                0 <= (self.currentPos[1] - steps) * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0], self.currentPos[1] - steps, self.currentPos[2]
                )

    def moveBackward(self, gridSize, cellSize):
        steps = 1
        if self.currentPos[2] == Direction.TOP:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] + 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (self.currentPos[0] + steps) * cellSize < gridSize) and (
                0 <= self.currentPos[1] * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0] + steps, self.currentPos[1], self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.RIGHT:
            # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (x == i) and (self.currentPos[1] - 2 == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= self.currentPos[0] * cellSize < gridSize) and (
                0 <= (self.currentPos[1] - steps) * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0], self.currentPos[1] - steps, self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (self.currentPos[0] - steps) * cellSize < gridSize) and (
                0 <= self.currentPos[1] * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0] - steps, self.currentPos[1], self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.LEFT:
            # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
            #              obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y -
            #              constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (x == i) and (self.currentPos[1] + 2 == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= self.currentPos[0] * cellSize < gridSize) and (
                0 <= (self.currentPos[1] + steps) * cellSize < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0], self.currentPos[1] + steps, self.currentPos[2]
                )

    def turnRight(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (
                    self.currentPos[0] - (constants.TURN_MED_RIGHT_TOP_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (self.currentPos[1] + constants.TURN_MED_RIGHT_TOP_FORWARD[0] // 10)
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                #         if (x > self.currentPos[0] - 3) and (y > self.currentPos[1] + 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_TOP_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_TOP_FORWARD[0] // 10),
                    Direction.RIGHT,
                )
        elif self.currentPos[2] == Direction.RIGHT:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_RIGHT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1] + constants.TURN_MED_RIGHT_RIGHT_FORWARD[0] // 10
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                #         if (x > self.currentPos[0] + 1) and (y < self.currentPos[1] + 3):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 3) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_RIGHT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_RIGHT_FORWARD[0] // 10),
                    Direction.BOTTOM,
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_BOTTOM_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    - (constants.TURN_MED_RIGHT_RIGHT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                #     for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                #         if (x < self.currentPos[0] + 3) and (y < self.currentPos[1] - 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_BOTTOM_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_BOTTOM_FORWARD[0] // 10),
                    Direction.LEFT,
                )
        elif self.currentPos[2] == Direction.LEFT:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_LEFT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_LEFT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                #         if (x < self.currentPos[0] - 1) and (y > self.currentPos[1] - 3):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_LEFT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_LEFT_FORWARD[0] // 10),
                    Direction.TOP,
                )

    def turnLeft(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (self.currentPos[0] - (constants.TURN_MED_LEFT_TOP_FORWARD[1] // 10))
                * cellSize
                < gridSize
            ) and (
                0
                <= (self.currentPos[1] + (constants.TURN_MED_LEFT_TOP_FORWARD[0] // 10))
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                #         if (x > self.currentPos[0] - 3) and (y < self.currentPos[1] - 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0] - (constants.TURN_MED_LEFT_TOP_FORWARD[1] // 10),
                    self.currentPos[1] + (constants.TURN_MED_LEFT_TOP_FORWARD[0] // 10),
                    Direction.LEFT,
                )
        elif self.currentPos[2] == Direction.RIGHT:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_RIGHT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_RIGHT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                #         if (x < self.currentPos[0] - 1) and (y < self.currentPos[1] + 3):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 3) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_RIGHT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_RIGHT_FORWARD[0] // 10),
                    Direction.TOP,
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_BOTTOM_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_BOTTOM_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                #         if (x < self.currentPos[0] + 3) and (y > self.currentPos[1] + 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_BOTTOM_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_BOTTOM_FORWARD[0] // 10),
                    Direction.RIGHT,
                )
        elif self.currentPos[2] == Direction.LEFT:
            if (
                0
                <= (
                    self.currentPos[0] - (constants.TURN_MED_LEFT_LEFT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1] + (constants.TURN_MED_LEFT_LEFT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                #     for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                #         if (x > self.currentPos[0] + 1) and (y > self.currentPos[1] - 3):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 3) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_LEFT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_LEFT_FORWARD[0] // 10),
                    Direction.BOTTOM,
                )

    def reverseTurnRight(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (
                    self.currentPos[0] - (constants.TURN_MED_RIGHT_TOP_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1] + (constants.TURN_MED_RIGHT_TOP_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                #         if (x < self.currentPos[0] + 2) and (y > self.currentPos[1] + 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 3) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_TOP_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_TOP_REVERSE[0] // 10),
                    Direction.LEFT,
                )
        elif self.currentPos[2] == Direction.RIGHT:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_RIGHT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                #     for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                #         if (x > self.currentPos[0] + 1) and (y > self.currentPos[1] - 2):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #         if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #             newRect = pygame.Rect(
                #                 y * cellSize, x * cellSize, cellSize, cellSize)
                #             self.screen.fill(constants.GREEN, newRect)
                #             pygame.draw.rect(
                #                 self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 3) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 4) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_RIGHT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_RIGHT_REVERSE[0] // 10),
                    Direction.TOP,
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_BOTTOM_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                #         if (x > self.currentPos[0] - 2) and (y < self.currentPos[1] - 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 3) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_BOTTOM_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_BOTTOM_REVERSE[0] // 10),
                    Direction.RIGHT,
                )
        elif self.currentPos[2] == Direction.LEFT:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_LEFT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                #         if (x < self.currentPos[0] - 1) and (y < self.currentPos[1] + 2):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 3) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_RIGHT_LEFT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_LEFT_REVERSE[0] // 10),
                    Direction.BOTTOM,
                )

    def reverseTurnLeft(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (self.currentPos[0] - (constants.TURN_MED_LEFT_TOP_REVERSE[1] // 10))
                * cellSize
                < gridSize
            ) and (
                0
                <= (self.currentPos[1] + (constants.TURN_MED_LEFT_TOP_REVERSE[0] // 10))
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                #     for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                #         if (x < self.currentPos[0] + 2) and (y < self.currentPos[1] - 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 3) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0] - (constants.TURN_MED_LEFT_TOP_REVERSE[1] // 10),
                    self.currentPos[1] + (constants.TURN_MED_LEFT_TOP_REVERSE[0] // 10),
                    Direction.RIGHT,
                )
        elif self.currentPos[2] == Direction.RIGHT:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_RIGHT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                #         if (x < self.currentPos[0] - 1) and (y > self.currentPos[1] - 2):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] - 3) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 4) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_RIGHT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_RIGHT_REVERSE[0] // 10),
                    Direction.BOTTOM,
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_BOTTOM_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                #         if (x > self.currentPos[0] - 2) and (y > self.currentPos[1] + 1):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 4) * cellSize < gridSize) and (0 <= (self.currentPos[1] + 3) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_BOTTOM_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_BOTTOM_REVERSE[0] // 10),
                    Direction.LEFT,
                )
        elif self.currentPos[2] == Direction.LEFT:
            if (
                0
                <= (
                    self.currentPos[0] - (constants.TURN_MED_LEFT_LEFT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1] + (constants.TURN_MED_LEFT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                # for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                #     for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                #         if (x > self.currentPos[0] + 1) and (y < self.currentPos[1] + 2):
                #             continue
                #         else:
                #             for obstacle in self.obstacles:
                #                 i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                #                      obstacle.position.x) // constants.GRID_CELL_LENGTH
                #                 j = (
                #                     obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                #                 if (x == i) and (y == j):
                #                     print(f"COLLISION!")
                #                     return
                #             if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                #                 newRect = pygame.Rect(
                #                     y * cellSize, x * cellSize, cellSize, cellSize)
                #                 self.screen.fill(constants.GREEN, newRect)
                #                 pygame.draw.rect(
                #                     self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (self.currentPos[0] + 3) * cellSize < gridSize) and (0 <= (self.currentPos[1] - 4) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{self.currentPos}")
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_MED_LEFT_LEFT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_LEFT_REVERSE[0] // 10),
                    Direction.TOP,
                )

    def moveNorthEast(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[0] // 10),
                    self.currentPos[2],
                )

    def moveNorthWest(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_FORWARD[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_FORWARD[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_FORWARD[0] // 10),
                    self.currentPos[2],
                )

    def moveSouthEast(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[0] // 10),
                    self.currentPos[2],
                )

    def moveSouthWest(self, gridSize, cellSize):
        if self.currentPos[2] == Direction.TOP:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            # for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (self.currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_REVERSE[1] // 10)
                )
                * cellSize
                < gridSize
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridSize
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPos(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_REVERSE[0] // 10),
                    self.currentPos[2],
                )

    def movement(self, x, y, buttonLength, buttonWidth):
        # move North
        if (685 < x < 685 + buttonLength) and (110 < y < 110 + buttonWidth):
            self.moveForward(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move South
        elif (685 < x < 685 + buttonLength) and (180 < y < 180 + buttonWidth):
            self.moveBackward(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move Forward East
        elif (720 < x < 720 + buttonLength) and (132.5 < y < 132.5 + buttonWidth):
            self.turnRight(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move Forward West
        elif (650 < x < 650 + buttonLength) and (132.5 < y < 132.5 + buttonWidth):
            self.turnLeft(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move Backward East
        elif (720 < x < 720 + buttonLength) and (160 < y < 160 + buttonWidth):
            self.reverseTurnRight(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move backward West
        elif (650 < x < 650 + buttonLength) and (160 < y < 160 + buttonWidth):
            self.reverseTurnLeft(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move North East
        elif (720 < x < 720 + buttonLength) and (107.5 < y < 107.5 + buttonWidth):
            self.moveNorthEast(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move North West
        elif (650 < x < 650 + buttonLength) and (107.5 < y < 107.5 + buttonWidth):
            self.moveNorthWest(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move South East
        elif (720 < x < 720 + buttonLength) and (182.5 < y < 182.5 + buttonWidth):
            self.moveSouthEast(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )
        # move South West
        elif (650 < x < 650 + buttonLength) and (182.5 < y < 182.5 + buttonWidth):
            self.moveSouthWest(
                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            )

    def draw(cls, x, y):
        # start button
        cls.drawButtons(
            650,
            500,
            constants.GREEN,
            "START!",
            constants.BLACK,
            constants.BUTTON_LENGTH,
            constants.BUTTON_WIDTH,
        )
        # set obstacles, asking for input from cmd prompt
        # cls.drawButtons(650, 450, constants.GREEN, 'SET', constants.BLACK,
        #                 constants.BUTTON_LENGTH, constants.BUTTON_WIDTH)
        # reset grid button
        cls.drawButtons(
            650,
            400,
            constants.BLACK,
            "RESET",
            constants.WHITE,
            constants.BUTTON_LENGTH,
            constants.BUTTON_WIDTH,
        )
        # Draw shortest path button
        cls.drawButtons(
            650,
            550,
            constants.BLACK,
            "DRAW",
            constants.WHITE,
            constants.BUTTON_LENGTH,
            constants.BUTTON_WIDTH,
        )

        if len(cls.obstacles) != 0:
            cls.drawObstaclesButton(cls.obstacles, constants.RED)
        else:
            cls.drawObstaclesButton([], constants.RED)

    def drawShortestPath(self, bot):
        halfAGridCell = (constants.GRID_CELL_LENGTH // 2) * constants.SCALING_FACTOR
        obstacleList = []
        y = (
            constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - self.currentPos[1]
        ) // constants.GRID_CELL_LENGTH
        x = self.currentPos[0] // constants.GRID_CELL_LENGTH
        obstacleList.append(
            (
                (x * constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                + halfAGridCell,
                (y * constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                + halfAGridCell,
            )
        )
        obstacleInOrder = self.bot.hamiltonian.simple_hamiltonian
        for obstacle in obstacleInOrder:
            print(obstacle)
            y = (
                constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.y
            ) // constants.GRID_CELL_LENGTH
            x = obstacle.position.x // constants.GRID_CELL_LENGTH
            obstacleList.append(
                (
                    (x * constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    + halfAGridCell,
                    (y * constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    + halfAGridCell,
                )
            )
        for i in range(1, len(obstacleList)):
            print(
                (obstacleList[i - 1][0], obstacleList[i - 1][1]),
                (obstacleList[i][0], obstacleList[i][1]),
            )
            self.updatingDisplay()
            pygame.draw.lines(
                self.screen,
                constants.RED,
                True,
                [
                    (obstacleList[i - 1][0], obstacleList[i - 1][1]),
                    (obstacleList[i][0], obstacleList[i][1]),
                ],
                3,
            )
            pygame.display.update()

    def updateTime(self, startTime, currentTime):
        if not startTime:
            return
        rect = pygame.Rect(
            620, 350, constants.BUTTON_LENGTH * 2, constants.BUTTON_WIDTH
        )
        self.screen.fill(constants.DEEP_BLUE, rect)
        pygame.draw.rect(self.screen, constants.DEEP_BLUE, rect, 2)
        self.drawButtons(
            650,
            350,
            constants.DEEP_BLUE,
            f"({(currentTime - startTime):.2f} Seconds)",
            constants.BLACK,
            constants.BUTTON_LENGTH,
            constants.BUTTON_WIDTH,
        )

    def updatingDisplay(self, start=None):
        self.clock.tick(5)  # 10 frames per second apparently
        #self.drawGridBackground()
        self.drawGrid()
        currentPosX = self.bot.get_current_pos().x
        currentPosY = self.bot.get_current_pos().y
        direction = self.bot.get_current_pos().direction
        self.currentPos = (
            (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - currentPosX) // 10,
            currentPosY // 10,
            direction,
        )
        self.drawRobot(
            self.currentPos,
            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
            constants.RED,
            constants.BLUE,
            constants.LIGHT_BLUE,
        )
        self.drawObstaclesButton(self.obstacles, constants.RED)
        pygame.time.delay(250)
        self.updateTime(start, time.time())

    def parseCmd(self, cmd, start):
        if isinstance(cmd, StraightCommand):
            if (cmd.dist // 10) >= 0:
                for i in range(cmd.dist // 10):
                    self.moveForward(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                    self.updatingDisplay(start)
                    pygame.display.update()
            else:
                for i in range(0 - (cmd.dist // 10)):
                    self.moveBackward(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                    self.updatingDisplay(start)
                    pygame.display.update()
        elif isinstance(cmd, TurnCommand):
            self.updatingDisplay(start)
            if cmd.type_of_turn == TypeOfTurn.MEDIUM:
                if cmd.right and not cmd.left and not cmd.reverse:
                    self.turnRight(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                elif cmd.left and not cmd.right and not cmd.reverse:
                    self.turnLeft(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                elif cmd.right and not cmd.left and cmd.reverse:
                    self.reverseTurnRight(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                elif cmd.left and not cmd.right and cmd.reverse:
                    self.reverseTurnLeft(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
            elif cmd.type_of_turn == TypeOfTurn.SMALL:
                if cmd.right and not cmd.left and not cmd.reverse:
                    self.moveNorthEast(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                elif cmd.left and not cmd.right and not cmd.reverse:
                    self.moveNorthWest(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                elif cmd.right and not cmd.left and cmd.reverse:
                    self.moveSouthEast(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
                elif cmd.left and not cmd.right and cmd.reverse:
                    self.moveSouthWest(
                        constants.GRID_LENGTH * constants.SCALING_FACTOR,
                        constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                    )
            pygame.display.update()
            self.updatingDisplay(start)

        elif isinstance(cmd, ScanCommand):
            self.updatingDisplay(start)
            self.drawRobot(
                self.currentPos,
                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                constants.RED,
                constants.ORANGE,
                constants.PINK,
            )
            pygame.display.update()
            self.updatingDisplay(start)
        else:
            print("Error!")
        # self.updatingDisplay(start)

    def runSimulation(self, bot):
        self.bot = deepcopy(bot)
        self.clock = pygame.time.Clock()
        self.obstacles = self.bot.hamiltonian.grid.obstacles
        start = None
        while True:
            self.updatingDisplay()
            x, y = pygame.mouse.get_pos()
            self.draw(x, y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (650 < x < 650 + constants.BUTTON_LENGTH) and (
                        500 < y < 500 + constants.BUTTON_WIDTH
                    ):
                        print(
                            "START BUTTON IS CLICKED!!! I REPEAT, START BUTTON IS CLICKED!!!"
                        )
                        """insert run algo function"""
                        self.bot.hamiltonian.plan_path()
                        start = time.time()
                        self.updateTime(start, start)
                        for cmd in self.bot.hamiltonian.commands:
                            self.parseCmd(cmd, start)
                            pygame.display.update()
                    # elif (650 < x < 650 + constants.BUTTON_LENGTH) and (450 < y < 450 + constants.BUTTON_WIDTH):
                    #     print("*****Drawing obstacles*****")
                    #     self.drawObstaclesButton(self.obstacles, constants.RED)
                    elif (650 < x < 650 + constants.BUTTON_LENGTH) and (
                        400 < y < 400 + constants.BUTTON_WIDTH
                    ):
                        self.reset(bot)
                    elif (
                        650
                        < x
                        < 720 + constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR
                    ) and (
                        115
                        < y
                        < 185 + constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR
                    ):
                        self.movement(
                            x,
                            y,
                            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                            25,
                        )
                    elif (650 < x < 650 + constants.BUTTON_LENGTH) and (
                        550 < y < 560 + constants.BUTTON_WIDTH
                    ):
                        self.drawShortestPath(bot)

                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    # if event.key == pygame.K_UP:
                    if keys[pygame.K_UP]:
                        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                            # if event.key == pygame.K_UP and event.key == pygame.K_RIGHT:
                            self.turnRight(
                                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                            )
                        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                            # elif event.key == pygame.K_UP and event.key == pygame.K_LEFT:
                            self.turnLeft(
                                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                            )
                        else:
                            self.moveForward(
                                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                            )
                    # elif event.key == pygame.K_DOWN:
                    if keys[pygame.K_DOWN]:
                        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                            # if event.key == pygame.K_DOWN and event.key == pygame.K_RIGHT:
                            self.reverseTurnRight(
                                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                            )
                        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                            # elif event.key == pygame.K_DOWN and event.key == pygame.K_LEFT:
                            self.reverseTurnLeft(
                                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                            )
                        else:
                            self.moveBackward(
                                constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                            )
                    elif event.key == pygame.K_e:
                        self.moveNorthEast(
                            constants.GRID_LENGTH * constants.SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                        )
                    elif event.key == pygame.K_q:
                        self.moveNorthWest(
                            constants.GRID_LENGTH * constants.SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                        )
                    elif event.key == pygame.K_d:
                        self.moveSouthEast(
                            constants.GRID_LENGTH * constants.SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                        )
                    elif event.key == pygame.K_a:
                        self.moveSouthWest(
                            constants.GRID_LENGTH * constants.SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                        )
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.screen.fill(constants.DEEP_BLUE)
            pygame.display.update()
