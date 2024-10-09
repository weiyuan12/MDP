import constants
from grid.grid import Grid
from grid.obstacle import Obstacle
from misc.direction import Direction
from misc.positioning import Position
from robot.robot import Robot
from TaskTwoSimulation import Simulation

obstacleX = 70
obstacleY = constants.TASK2_LENGTH - constants.GRID_CELL_LENGTH - 20
distance1 = constants.DISTANCE1
distance2 = constants.DISTANCE2

world1 = [
    [70, distance1, Direction.BOTTOM],
    [70, distance1 + distance2 + constants.GRID_CELL_LENGTH, Direction.BOTTOM],
]
obstacles = []
i = 0
for x, y, direction in world1:
    position: Position = Position(x, y, direction)
    obstacle: Obstacle = Obstacle(position, i)
    i += 1
    obstacles.append(obstacle)
grid = Grid(obstacles)
bot = Robot(grid)
direction = bot.get_current_pos().direction
currentPos = (obstacleY // 10, obstacleX // 10, direction)
print(f"CURRENT POS: {currentPos}")
bot.setCurrentPosTask2(currentPos[0], currentPos[1], bot.get_current_pos().direction)
direction = []

obstacle1 = constants.OBSTACLE1
direction.append(obstacle1)

obstacle2 = constants.OBSTACLE2
direction.append(obstacle2)

sim = Simulation(direction)
sim.runTask2Simulation(bot)
