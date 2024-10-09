import sys
from copy import deepcopy

import pygame

import constants
from misc.direction import Direction


class Simulation:
    def __init__(self, direction):
        pygame.init()
        self.running = True
        self.direction = direction
        self.font = pygame.font.SysFont("Arial", 25)
        self.screen = pygame.display.set_mode((900, 700), pygame.RESIZABLE)
        self.clock = None
        pygame.mouse.set_visible(1)
        pygame.display.set_caption("Vroom Vroom Simulation")
        self.screen.fill(constants.BLACK)

    def reset(cls, bot):
        cls.screen.fill(constants.BLACK)
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
                    0
                    <= x * cellSize
                    < constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR
                ) and (
                    0
                    <= y * cellSize
                    < constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR
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

    def drawGrid2(cls, bot):
        for x in range(
            0,
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        ):
            for y in range(
                0,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            ):
                rect = pygame.Rect(
                    y,
                    x,
                    constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
                    constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
                )
                pygame.draw.rect(cls.screen, constants.WHITE, rect, 2)

    """ How to add texts?? """

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

    def drawWalls(cls, x, y, xLength, yLength, size, color):
        imageSide = pygame.Rect(
            x * size, (y * size) + size, xLength * size, yLength * size
        )
        cls.screen.fill(color, imageSide)
        pygame.draw.rect(cls.screen, color, imageSide, 1)

    def drawObstacles(cls, obstacles, color):
        size = constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR

        """Draw obstacle 1"""
        y = (
            constants.TASK2_LENGTH
            - (constants.GRID_CELL_LENGTH * 5 + obstacles[0].position.y)
        ) // constants.GRID_CELL_LENGTH
        # x = i.position.x // constants.GRID_CELL_LENGTH
        x = obstacles[0].position.x // constants.GRID_CELL_LENGTH

        cls.selectObstacles(
            x,
            y,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.YELLOW,
        )
        imageSide = pygame.Rect(x * size, (y * size) + size - 5, size, 5)
        cls.screen.fill(color, imageSide)
        pygame.draw.rect(cls.screen, color, imageSide, 5)

        """Draw obstacle 2"""
        size = constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR
        y = (
            constants.TASK2_LENGTH
            - (constants.GRID_CELL_LENGTH * 5 + obstacles[1].position.y)
        ) // constants.GRID_CELL_LENGTH
        # x = i.position.x // constants.GRID_CELL_LENGTH
        x = obstacles[1].position.x // constants.GRID_CELL_LENGTH

        cls.selectObstacles(
            x,
            y,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.YELLOW,
        )
        imageSide = pygame.Rect(x * size, (y * size) + size - 5, size, 5)
        cls.screen.fill(color, imageSide)
        pygame.draw.rect(cls.screen, color, imageSide, 5)

        """Draw walls"""
        cls.drawWalls(x - 2.5, y - 1, 2.5, 1, size, constants.YELLOW)
        cls.drawWalls(x + 1, y - 1, 2.5, 1, size, constants.YELLOW)
        cls.drawWalls(
            5,
            (constants.TASK2_LENGTH - 5 * constants.GRID_CELL_LENGTH) // 10,
            1,
            4,
            size,
            constants.YELLOW,
        )
        cls.drawWalls(
            9,
            (constants.TASK2_LENGTH - 5 * constants.GRID_CELL_LENGTH) // 10,
            1,
            4,
            size,
            constants.YELLOW,
        )
        cls.drawWalls(
            5,
            (constants.TASK2_LENGTH - 2 * constants.GRID_CELL_LENGTH) // 10,
            5,
            1,
            size,
            constants.YELLOW,
        )

    """ self.currentPos[0] == y, self.currentPos[1] == x for some reason dk why, dont plan to change this """

    def moveForward(self, gridLength, gridWidth, cellSize):
        steps = 1
        if self.currentPos[2] == Direction.TOP:
            for x in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (self.currentPos[0] - 2 == j) and (x == i):
                        print(f"COLLISION!")
                        return -1
            # if (0 <= (self.currentPos[0] - steps) * cellSize < gridLength) and (0 <= self.currentPos[1] * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0] - steps, self.currentPos[1], self.currentPos[2]
            )
        elif self.currentPos[2] == Direction.RIGHT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (x == j) and (self.currentPos[1] + 2 == i):
                        print(f"COLLISION!")
                        return -1
            # if (0 <= self.currentPos[0] * cellSize < gridLength) and (0 <= (self.currentPos[1] + steps) * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0], self.currentPos[1] + steps, self.currentPos[2]
            )
        elif self.currentPos[2] == Direction.BOTTOM:
            for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (self.currentPos[0] + 2 == j) and (y == i):
                        print(f"COLLISION!")
                        return -1
            # if (0 <= (self.currentPos[0] + steps) * cellSize < gridLength) and (0 <= self.currentPos[1] * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0] + steps, self.currentPos[1], self.currentPos[2]
            )
        elif self.currentPos[2] == Direction.LEFT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (x == j) and (self.currentPos[1] - 2 == i):
                        print(f"COLLISION!")
                        return -1
            # if (0 <= self.currentPos[0] * cellSize < gridLength) and (0 <= (self.currentPos[1] - steps) * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0], self.currentPos[1] - steps, self.currentPos[2]
            )
        return 1

    def moveBackward(self, gridLength, gridWidth, cellSize):
        steps = 1
        if self.currentPos[2] == Direction.TOP:
            for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (self.currentPos[0] + 2 == j) and (y == i):
                        print(f"COLLISION!")
                        return -1
            if (0 <= (self.currentPos[0] + steps) * cellSize < gridLength) and (
                0 <= self.currentPos[1] * cellSize < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0] + steps, self.currentPos[1], self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.RIGHT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (x == j) and (self.currentPos[1] - 2 == i):
                        print(f"COLLISION!")
                        return -1
            if (0 <= self.currentPos[0] * cellSize < gridLength) and (
                0 <= (self.currentPos[1] - steps) * cellSize < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0], self.currentPos[1] - steps, self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            for y in range(self.currentPos[1] - 1, self.currentPos[1] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (self.currentPos[0] - 2 == j) and (y == i):
                        print(f"COLLISION!")
                        return -1
            if (0 <= (self.currentPos[0] - steps) * cellSize < gridLength) and (
                0 <= self.currentPos[1] * cellSize < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0] - steps, self.currentPos[1], self.currentPos[2]
                )
        elif self.currentPos[2] == Direction.LEFT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 2):
                for obstacle in self.obstacles:
                    j = (
                        constants.TASK2_LENGTH
                        - constants.GRID_CELL_LENGTH * 5
                        - obstacle.position.y
                    ) // constants.GRID_CELL_LENGTH
                    i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                    if (x == j) and (self.currentPos[1] + 2 == i):
                        print(f"COLLISION!")
                        return -1
            if (0 <= self.currentPos[0] * cellSize < gridLength) and (
                0 <= (self.currentPos[1] + steps) * cellSize < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0], self.currentPos[1] + steps, self.currentPos[2]
                )
        return 1

    def turnRight(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (
                    self.currentPos[0] - (constants.TURN_MED_RIGHT_TOP_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (self.currentPos[1] + constants.TURN_MED_RIGHT_TOP_FORWARD[0] // 10)
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                    for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                        if (x > self.currentPos[0] + 1) and (y >= self.currentPos[1]):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_TOP_FORWARD[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_TOP_FORWARD[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_TOP_FORWARD[1] // 10),
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_TOP_FORWARD[0] // 10),
                        Direction.RIGHT,
                    )
        elif self.currentPos[2] == Direction.RIGHT:
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_RIGHT_RIGHT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + constants.TURN_MED_RIGHT_RIGHT_FORWARD[0] // 10) * cellSize < gridWidth):
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                    if (x > self.currentPos[0] + 1) and (y < self.currentPos[1] + 1):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                        #     newRect = pygame.Rect(
                        #         y * cellSize, x * cellSize, cellSize, cellSize)
                        #     self.screen.fill(constants.GREEN, newRect)
                        #     pygame.draw.rect(
                        #         self.screen, constants.GREEN, newRect, 2)
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_RIGHT_RIGHT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + (constants.TURN_MED_RIGHT_RIGHT_FORWARD[0] // 10)) * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0] - (constants.TURN_MED_RIGHT_RIGHT_FORWARD[1] // 10),
                self.currentPos[1] + (constants.TURN_MED_RIGHT_RIGHT_FORWARD[0] // 10),
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    - (constants.TURN_MED_RIGHT_RIGHT_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                    for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                        if (x < self.currentPos[0] + 1) and (
                            y < self.currentPos[1] - 1
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_BOTTOM_FORWARD[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_BOTTOM_FORWARD[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_BOTTOM_FORWARD[1] // 10),
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_BOTTOM_FORWARD[0] // 10),
                        Direction.LEFT,
                    )
        elif self.currentPos[2] == Direction.LEFT:
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_RIGHT_LEFT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + (constants.TURN_MED_RIGHT_LEFT_FORWARD[0] // 10)) * cellSize < gridWidth):
            for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                    if (x < self.currentPos[0] - 1) and (y > self.currentPos[1] - 1):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                        #     newRect = pygame.Rect(
                        #         y * cellSize, x * cellSize, cellSize, cellSize)
                        #     self.screen.fill(constants.GREEN, newRect)
                        #     pygame.draw.rect(
                        #         self.screen, constants.GREEN, newRect, 2)
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_RIGHT_LEFT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + (constants.TURN_MED_RIGHT_LEFT_FORWARD[0] // 10)) * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0] - (constants.TURN_MED_RIGHT_LEFT_FORWARD[1] // 10),
                self.currentPos[1] + (constants.TURN_MED_RIGHT_LEFT_FORWARD[0] // 10),
                Direction.TOP,
            )
        return 1

    def turnLeft(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (self.currentPos[0] - (constants.TURN_MED_LEFT_TOP_FORWARD[1] // 10))
                * cellSize
                < gridLength
            ) and (
                0
                <= (self.currentPos[1] + (constants.TURN_MED_LEFT_TOP_FORWARD[0] // 10))
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                    for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                        if (x > self.currentPos[0] - 1) and (
                            y < self.currentPos[1] - 1
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_TOP_FORWARD[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_TOP_FORWARD[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_TOP_FORWARD[1] // 10),
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_TOP_FORWARD[0] // 10),
                        Direction.LEFT,
                    )
        elif self.currentPos[2] == Direction.RIGHT:
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_LEFT_RIGHT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + (constants.TURN_MED_LEFT_RIGHT_FORWARD[0] // 10)) * cellSize < gridWidth):
            for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                    if (x < self.currentPos[0] - 1) and (y < self.currentPos[1] + 1):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                        #     newRect = pygame.Rect(
                        #         y * cellSize, x * cellSize, cellSize, cellSize)
                        #     self.screen.fill(constants.GREEN, newRect)
                        #     pygame.draw.rect(
                        #         self.screen, constants.GREEN, newRect, 2)
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_LEFT_RIGHT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + (constants.TURN_MED_LEFT_RIGHT_FORWARD[0] // 10)) * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0] - (constants.TURN_MED_LEFT_RIGHT_FORWARD[1] // 10),
                self.currentPos[1] + (constants.TURN_MED_LEFT_RIGHT_FORWARD[0] // 10),
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_BOTTOM_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                    for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                        if (x < self.currentPos[0] + 1) and (
                            y > self.currentPos[1] + 1
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_BOTTOM_FORWARD[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_BOTTOM_FORWARD[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_BOTTOM_FORWARD[1] // 10),
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_BOTTOM_FORWARD[0] // 10),
                        Direction.RIGHT,
                    )
        elif self.currentPos[2] == Direction.LEFT:
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_LEFT_LEFT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + (constants.TURN_MED_LEFT_LEFT_FORWARD[0] // 10)) * cellSize < gridWidth):
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                    if (x > self.currentPos[0] + 1) and (y > self.currentPos[1] - 1):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                        #     newRect = pygame.Rect(
                        #         y * cellSize, x * cellSize, cellSize, cellSize)
                        #     self.screen.fill(constants.GREEN, newRect)
                        #     pygame.draw.rect(
                        #         self.screen, constants.GREEN, newRect, 2)
            # if (0 <= (self.currentPos[0] - (constants.TURN_MED_LEFT_LEFT_FORWARD[1] // 10)) * cellSize < gridLength) and (0 <= (self.currentPos[1] + (constants.TURN_MED_LEFT_LEFT_FORWARD[0] // 10)) * cellSize < gridWidth):
            self.drawRobot(
                self.currentPos,
                cellSize,
                constants.GREEN,
                constants.GREEN,
                constants.GREEN,
            )
            self.bot.setCurrentPosTask2(
                self.currentPos[0] - (constants.TURN_MED_LEFT_LEFT_FORWARD[1] // 10),
                self.currentPos[1] + (constants.TURN_MED_LEFT_LEFT_FORWARD[0] // 10),
                Direction.BOTTOM,
            )
        return 1

    def reverseTurnRight(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (
                    self.currentPos[0] - (constants.TURN_MED_RIGHT_TOP_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1] + (constants.TURN_MED_RIGHT_TOP_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                    for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                        if (x < self.currentPos[0] + 2) and (
                            y > self.currentPos[1] + 1
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_TOP_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_TOP_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                    for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                        if (x > self.currentPos[0] + 1) and (
                            y > self.currentPos[1] - 2
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_RIGHT_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_RIGHT_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                    for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                        if (x > self.currentPos[0] - 2) and (
                            y < self.currentPos[1] - 1
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_BOTTOM_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_BOTTOM_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_RIGHT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                    for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                        if (x < self.currentPos[0] - 1) and (
                            y < self.currentPos[1] + 2
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_LEFT_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_LEFT_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
                        self.currentPos[0]
                        - (constants.TURN_MED_RIGHT_LEFT_REVERSE[1] // 10),
                        self.currentPos[1]
                        + (constants.TURN_MED_RIGHT_LEFT_REVERSE[0] // 10),
                        Direction.BOTTOM,
                    )
        return 1

    def reverseTurnLeft(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            if (
                0
                <= (self.currentPos[0] - (constants.TURN_MED_LEFT_TOP_REVERSE[1] // 10))
                * cellSize
                < gridLength
            ) and (
                0
                <= (self.currentPos[1] + (constants.TURN_MED_LEFT_TOP_REVERSE[0] // 10))
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 1, self.currentPos[0] + 5):
                    for y in range(self.currentPos[1] - 3, self.currentPos[1] + 2):
                        if (x < self.currentPos[0] + 2) and (
                            y < self.currentPos[1] - 1
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_TOP_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_TOP_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_TOP_REVERSE[1] // 10),
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_TOP_REVERSE[0] // 10),
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 3, self.currentPos[0] + 2):
                    for y in range(self.currentPos[1] - 4, self.currentPos[1] + 2):
                        if (x < self.currentPos[0] - 1) and (
                            y > self.currentPos[1] - 2
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_RIGHT_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_RIGHT_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_MED_LEFT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 4, self.currentPos[0] + 2):
                    for y in range(self.currentPos[1] - 1, self.currentPos[1] + 4):
                        if (x > self.currentPos[0] - 2) and (
                            y > self.currentPos[1] + 1
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_BOTTOM_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_BOTTOM_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
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
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1] + (constants.TURN_MED_LEFT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                for x in range(self.currentPos[0] - 1, self.currentPos[0] + 4):
                    for y in range(self.currentPos[1] - 1, self.currentPos[1] + 5):
                        if (x > self.currentPos[0] + 1) and (
                            y < self.currentPos[1] + 2
                        ):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                j = (
                                    constants.TASK2_LENGTH
                                    - constants.GRID_CELL_LENGTH * 5
                                    - obstacle.position.y
                                ) // constants.GRID_CELL_LENGTH
                                i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                                if (x == j) and (y == i):
                                    print(f"COLLISION!")
                                    return -1
                            # if (0 <= x * cellSize < gridLength) and (0 <= y * cellSize < gridWidth):
                            #     newRect = pygame.Rect(
                            #         y * cellSize, x * cellSize, cellSize, cellSize)
                            #     self.screen.fill(constants.GREEN, newRect)
                            #     pygame.draw.rect(
                            #         self.screen, constants.GREEN, newRect, 2)
                if (
                    0
                    <= (
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_LEFT_REVERSE[1] // 10)
                    )
                    * cellSize
                    < gridLength
                ) and (
                    0
                    <= (
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_LEFT_REVERSE[0] // 10)
                    )
                    * cellSize
                    < gridWidth
                ):
                    self.drawRobot(
                        self.currentPos,
                        cellSize,
                        constants.GREEN,
                        constants.GREEN,
                        constants.GREEN,
                    )
                    self.bot.setCurrentPosTask2(
                        self.currentPos[0]
                        - (constants.TURN_MED_LEFT_LEFT_REVERSE[1] // 10),
                        self.currentPos[1]
                        + (constants.TURN_MED_LEFT_LEFT_REVERSE[0] // 10),
                        Direction.TOP,
                    )
        return 1

    def moveNorthEast(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            for x in range(self.currentPos[0] - 5, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 3):
                    if (x > self.currentPos[0] - 1) and (y > self.currentPos[1] + 1):
                        continue
                    elif (x < self.currentPos[0] - 3) and (y < self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 3):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 6):
                    if (x > self.currentPos[0] + 1) and (y < self.currentPos[1] + 1):
                        continue
                    elif (x < self.currentPos[0]) and (y > self.currentPos[1] + 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 6):
                for y in range(self.currentPos[1] - 2, self.currentPos[1] + 2):
                    if (x < self.currentPos[0] + 1) and (y < self.currentPos[1] - 1):
                        continue
                    elif (x > self.currentPos[0] + 3) and (y > self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            for x in range(self.currentPos[0] - 2, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 5, self.currentPos[1] + 2):
                    if (x < self.currentPos[0] - 1) and (y > self.currentPos[1] - 1):
                        continue
                    elif (x > self.currentPos[0]) and (y < self.currentPos[1] - 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        return 1

    def moveNorthWest(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            for x in range(self.currentPos[0] - 5, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 2, self.currentPos[1] + 2):
                    if (x > self.currentPos[0] - 1) and (y < self.currentPos[1] - 1):
                        continue
                    elif (x < self.currentPos[0] - 3) and (y > self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            for x in range(self.currentPos[0] - 2, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 6):
                    if (x < self.currentPos[0] - 1) and (y < self.currentPos[1] + 1):
                        continue
                    elif (x > self.currentPos[0]) and (y > self.currentPos[1] + 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 6):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 3):
                    if (x < self.currentPos[0] + 1) and (y > self.currentPos[1] + 1):
                        continue
                    elif (x > self.currentPos[0] + 3) and (y < self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 3):
                for y in range(self.currentPos[1] - 5, self.currentPos[1] + 2):
                    if (x > self.currentPos[0] + 1) and (y > self.currentPos[1] - 1):
                        continue
                    elif (x < self.currentPos[0]) and (y < self.currentPos[1] - 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_FORWARD[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_FORWARD[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_FORWARD[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_FORWARD[0] // 10),
                    self.currentPos[2],
                )
        return 1

    def moveSouthEast(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 6):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 3):
                    if (x < self.currentPos[0] + 1) and (y > self.currentPos[1] + 1):
                        continue
                    elif (x > self.currentPos[0] + 3) and (y < self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)

            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_TOP_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_TOP_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 3):
                for y in range(self.currentPos[1] - 5, self.currentPos[1] + 2):
                    if (x > self.currentPos[0] + 1) and (y > self.currentPos[1] - 1):
                        continue
                    elif (x < self.currentPos[0]) and (y < self.currentPos[1] - 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_RIGHT_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            for x in range(self.currentPos[0] - 5, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 2, self.currentPos[1] + 2):
                    if (x > self.currentPos[0] - 1) and (y < self.currentPos[1] - 1):
                        continue
                    elif (x < self.currentPos[0] - 3) and (y > self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_BOTTOM_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            for x in range(self.currentPos[0] - 2, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 6):
                    if (x < self.currentPos[0] - 1) and (y < self.currentPos[1] + 1):
                        continue
                    elif (x > self.currentPos[0]) and (y > self.currentPos[1] + 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_RIGHT_LEFT_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        return 1

    def moveSouthWest(self, gridLength, gridWidth, cellSize):
        if self.currentPos[2] == Direction.TOP:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 6):
                for y in range(self.currentPos[1] - 2, self.currentPos[1] + 2):
                    if (x < self.currentPos[0] + 1) and (y < self.currentPos[1] - 1):
                        continue
                    elif (x > self.currentPos[0] + 3) and (y > self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_TOP_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_TOP_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.RIGHT:
            for x in range(self.currentPos[0] - 2, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 5, self.currentPos[1] + 2):
                    if (x < self.currentPos[0] - 1) and (y > self.currentPos[1] - 1):
                        continue
                    elif (x > self.currentPos[0]) and (y < self.currentPos[1] - 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_RIGHT_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.BOTTOM:
            for x in range(self.currentPos[0] - 5, self.currentPos[0] + 2):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 3):
                    if (x > self.currentPos[0] - 1) and (y > self.currentPos[1] + 1):
                        continue
                    elif (x < self.currentPos[0] - 3) and (y < self.currentPos[1]):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_BOTTOM_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        elif self.currentPos[2] == Direction.LEFT:
            for x in range(self.currentPos[0] - 1, self.currentPos[0] + 3):
                for y in range(self.currentPos[1] - 1, self.currentPos[1] + 6):
                    if (x > self.currentPos[0] + 1) and (y < self.currentPos[1] + 1):
                        continue
                    elif (x < self.currentPos[0]) and (y > self.currentPos[1] + 3):
                        continue
                    else:
                        for obstacle in self.obstacles:
                            j = (
                                constants.TASK2_LENGTH
                                - constants.GRID_CELL_LENGTH * 5
                                - obstacle.position.y
                            ) // constants.GRID_CELL_LENGTH
                            i = (obstacle.position.x) // constants.GRID_CELL_LENGTH
                            if (x == j) and (y == i):
                                print(f"COLLISION!")
                                return -1
                        if (0 <= x * cellSize < gridLength) and (
                            0 <= y * cellSize < gridWidth
                        ):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize
                            )
                            self.screen.fill(constants.PINK, newRect)
                            pygame.draw.rect(self.screen, constants.PINK, newRect, 2)
            if (
                0
                <= (
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_REVERSE[1] // 10)
                )
                * cellSize
                < gridLength
            ) and (
                0
                <= (
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_REVERSE[0] // 10)
                )
                * cellSize
                < gridWidth
            ):
                self.drawRobot(
                    self.currentPos,
                    cellSize,
                    constants.GREEN,
                    constants.GREEN,
                    constants.GREEN,
                )
                self.bot.setCurrentPosTask2(
                    self.currentPos[0]
                    - (constants.TURN_SMALL_LEFT_LEFT_REVERSE[1] // 10),
                    self.currentPos[1]
                    + (constants.TURN_SMALL_LEFT_LEFT_REVERSE[0] // 10),
                    self.currentPos[2],
                )
        return 1

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
        # current cursor coordinates, change to robot
        cls.drawButtons(
            650,
            550,
            constants.BLACK,
            f"({x}, {y})",
            constants.WHITE,
            constants.BUTTON_LENGTH,
            constants.BUTTON_WIDTH,
        )
        # reset grid button
        cls.drawButtons(
            650,
            450,
            constants.GREY,
            "RESET",
            constants.BLACK,
            constants.BUTTON_LENGTH,
            constants.BUTTON_WIDTH,
        )
        # Draw shortest path button
        if len(cls.obstacles) != 0:
            cls.drawObstacles(cls.obstacles, constants.RED)
        else:
            cls.drawObstacles([], constants.RED)

    def updatingTask2Display(self):
        self.clock.tick(100)
        self.drawGrid2(self.bot)
        currentPosX = self.bot.get_current_pos().x
        currentPosY = self.bot.get_current_pos().y
        direction = self.bot.get_current_pos().direction
        self.currentPos = (
            (constants.TASK2_LENGTH - constants.GRID_CELL_LENGTH - currentPosX) // 10,
            currentPosY // 10,
            direction,
        )
        self.drawRobot(
            self.currentPos,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.RED,
            constants.BLUE,
            constants.LIGHT_BLUE,
        )
        self.drawObstacles(self.obstacles, constants.RED)
        pygame.time.delay(100)

    def left(self, movement):
        for i in range(3):
            self.moveBackward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            movement["forward"] -= 1
            self.updatingTask2Display()
            pygame.display.update()
        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()
        movement["forward"] += 10

    def right(self, movement):
        for i in range(3):
            self.moveBackward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            movement["forward"] -= 1
            self.updatingTask2Display()
            pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()
        movement["forward"] += 10

    def secondleft(self, movement):
        for i in range(2):
            self.moveBackward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            movement["forward"] -= 1
            self.updatingTask2Display()
            pygame.display.update()

        movement["forward"] -= 1
        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        for i in range(5):
            self.moveForward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            # movement['forward'] -= 1
            self.updatingTask2Display()
            pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        for i in range(movement["forward"]):
            self.moveForward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            self.updatingTask2Display()
            pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

    def secondright(self, movement):
        for i in range(2):
            self.moveBackward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            movement["forward"] -= 1
            self.updatingTask2Display()
            pygame.display.update()

        movement["forward"] -= 1
        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        for i in range(5):
            self.moveForward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            # movement['forward'] -= 1
            self.updatingTask2Display()
            pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        for i in range(movement["forward"]):
            self.moveForward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            # movement['forward'] -= 1
            self.updatingTask2Display()
            pygame.display.update()

        self.turnLeft(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

        self.turnRight(
            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
        )
        self.updatingTask2Display()
        pygame.display.update()

    def task2Algo(self, direction):
        movement = {}
        movement["forward"] = 0

        while True:  # while ultrasonic dont detect wall
            temp = self.moveForward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            if temp == 1:  # if not wall
                movement["forward"] += 1
                self.updatingTask2Display()
                pygame.display.update()
            elif temp == -1:  # if wall
                break

        # get arrow direction
        obstacle1 = direction[0]
        if obstacle1 == "L":
            self.left(movement)
        elif obstacle1 == "R":
            self.right(movement)

        # robot routes around the first obstacle

        while True:  # while not wall move forward
            temp = self.moveForward(
                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
            )
            if temp == 1:  # if not wall
                movement["forward"] += 1
                self.updatingTask2Display()
                pygame.display.update()
            elif temp == -1:  # if wall
                break

        # get second direction
        obstacle2 = direction[1]

        if obstacle2 == "L":
            self.secondleft(movement)
        elif obstacle2 == "R":
            self.secondright(movement)

    def runTask2Simulation(self, bot):
        self.bot = deepcopy(bot)
        self.clock = pygame.time.Clock()
        self.obstacles = self.bot.hamiltonian.grid.obstacles
        while True:
            self.updatingTask2Display()
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

                        self.task2Algo(self.direction)
                    elif (650 < x < 650 + constants.BUTTON_LENGTH) and (
                        450 < y < 450 + constants.BUTTON_WIDTH
                    ):
                        self.reset(bot)

                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                            self.turnRight(
                                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH
                                * constants.TASK2_SCALING_FACTOR,
                            )
                        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                            self.turnLeft(
                                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH
                                * constants.TASK2_SCALING_FACTOR,
                            )
                        else:
                            self.moveForward(
                                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH
                                * constants.TASK2_SCALING_FACTOR,
                            )
                    if keys[pygame.K_DOWN]:
                        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                            self.reverseTurnRight(
                                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH
                                * constants.TASK2_SCALING_FACTOR,
                            )
                        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                            self.reverseTurnLeft(
                                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH
                                * constants.TASK2_SCALING_FACTOR,
                            )
                        else:
                            self.moveBackward(
                                constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                                constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                                constants.GRID_CELL_LENGTH
                                * constants.TASK2_SCALING_FACTOR,
                            )
                    elif event.key == pygame.K_e:
                        self.moveNorthEast(
                            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
                        )
                    elif event.key == pygame.K_q:
                        self.moveNorthWest(
                            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
                        )
                    elif event.key == pygame.K_d:
                        self.moveSouthEast(
                            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
                        )
                    elif event.key == pygame.K_a:
                        self.moveSouthWest(
                            constants.TASK2_LENGTH * constants.TASK2_SCALING_FACTOR,
                            constants.TASK2_WIDTH * constants.TASK2_SCALING_FACTOR,
                            constants.GRID_CELL_LENGTH * constants.TASK2_SCALING_FACTOR,
                        )
            pygame.display.update()
