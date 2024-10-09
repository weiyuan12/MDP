import socket
import sys
import time
from typing import List

import constants
from commands.go_straight_command import StraightCommand
from commands.scan_obstacle_command import ScanCommand
from connection_to_rpi.rpi_client import RPiClient
from grid.grid import Grid
from grid.obstacle import Obstacle
from misc.direction import Direction
from misc.positioning import Position
from pygame_app import AlgoMinimal
from robot.robot import Robot
from simulation import Simulation

import os


class Main:
    def __init__(self):
        self.client = None
        self.commands = None
        self.count = 0

    def parse_obstacle_data(self, data) -> List[Obstacle]:
        # [[x, y, orient, index], [x, y, orient, index]]
        obs = []
        for obstacle_params in data:
            if len(obstacle_params) < 4:
                continue
            obs.append(
                Obstacle(
                    Position(
                        obstacle_params[0],
                        obstacle_params[1],
                        Direction(obstacle_params[2]),
                    ),
                    obstacle_params[3],
                )
            )
        return obs

    def run_simulator(self):
        # For simulation testing, change this with the obstacles to test.
        obstacles = []
        i = 0
        for x, y, direction in constants.SIMULATOR_OBSTACLES:
            position: Position = Position(x, y, direction)
            obstacle: Obstacle = Obstacle(position, i)
            i += 1
            obstacles.append(obstacle)
        grid = Grid(obstacles)
        bot = Robot(grid)
        sim = Simulation()
        sim.runSimulation(bot)
        # """
        # Fill in obstacle positions with respect to lower bottom left corner.
        # (x-coordinate, y-coordinate, Direction)
        # obstacles = [[15, 75, 0, 0]]
        # obs = parse_obstacle_data(obstacles)
        # """
        # obs = self.parse_obstacle_data([])
        # app = AlgoSimulator(obs)
        # app.init()
        # app.execute()

    def run_minimal(self, also_run_simulator):
        # Create a client to connect to the RPi.

        if self.client is None:
            print(f"Attempting to connect to {constants.RPI_HOST}:{constants.RPI_PORT}")
            self.client = RPiClient(constants.RPI_HOST, constants.RPI_PORT)
            #  Wait to connect to RPi.
            while True:
                try:
                    self.client.connect()
                    break
                except OSError:
                    pass
                except KeyboardInterrupt:
                    self.client.close()
                    sys.exit(1)
            print("Connected to RPi!\n")

        # # # # Wait for message from RPI
        print("Waiting to receive data from RPi...")
        d = self.client.receive_message()
        # d = dummy
        print("Decoding data from RPi:")
        d = d.decode("utf-8")
        #d = 'ALG|2,18,S,0|5,18,S,1|8,18,S,2|11,18,S,3|14,18,S,4;'
        print(f"Received data from RPI: {d}")
        to_return = []
        if d[0:4] == "ALG|":
            d = d[4:]
            d = d.split("|")
            # now split into separate obstacles
            # last will be split into empty string therefore ignore
            for x in range(0, len(d) - 1):
                d_split = d[x].split(",")
                # d_split now holds the 4 values that are needed to create one obstacle
                temp = []
                print(f"d_split: {d_split}")
                for y in range(0, len(d_split)):
                    # means it's x or y coordinate so multiply by 10 to correspond to correct coordinate
                    if y <= 1:
                        temp.append(int(d_split[y]) * 10)
                        #continue
                    elif y == 2:
                        if d_split[y] == "N":
                            temp.append(90)
                        elif d_split[y] == "S":
                            temp.append(-90)
                        elif d_split[y] == "E":
                            temp.append(0)
                        else:
                            temp.append(180)
                    else:
                        temp.append(int(d_split[y]))
                to_return.append(temp)

                print("to_return: ", to_return)
            print("Running here")
            self.decision(self.client, to_return, also_run_simulator)
        else:
            # this would be strings such as NONE, DONE, BULLSEYE
            print("Running here")
            print(f"d = {d}")
            self.decision(self.client, d, also_run_simulator)

    def decision(self, client, data, also_run_simulator):
        def isvalid(img):
            # Obstacle string 11-39
            checklist = [str(i) for i in range(41)]
            if img in checklist:
                return True
            return False

        # Obstacle list
        if isinstance(data[0], list):
            obstacles = self.parse_obstacle_data(data)
            app = AlgoMinimal(obstacles)
            app.init()
            # populates the Hamiltonian object with all the commands necessary to reach the objects
            if also_run_simulator:
                app.simulate()
            else:
                app.execute()
            # app.execute()
            # Send the list of commands over.
            obs_priority = app.robot.hamiltonian.get_simple_hamiltonian()
            # print(obs_priority)
            print("Sending list of commands to RPi...")
            self.commands = app.robot.convert_all_commands()
            print(self.commands)
            if len(self.commands) != 0:
                client.send_message(self.commands)
            else:
                print("ERROR!! NO COMMANDS TO SEND TO RPI")

        elif isinstance(data[0], str):
            # means its None
            print(data)
            try:
                client.send_message(
                    [
                        StraightCommand(-10).convert_to_message(),
                        ScanCommand(0, int(data[1])).convert_to_message(),
                        StraightCommand(10).convert_to_message(),
                    ]
                )
            except IndexError:
                print("Error!")
                print("Index Error!")

        # # String commands from Rpi
        # elif isinstance(data[0], str):
        #     # Check valid image taken
        #     if isvalid(data[0]):
        #         if self.count == 0:
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 print(sent_commands)
        #                 print(self.commands)
        #                 client.send_message(sent_commands)
        #
        #         elif self.count == 1:
        #             self.count = 0
        #             amended_commands = ["STM:w010n\n"]
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 amended_commands = amended_commands + sent_commands
        #                 print("Amended commands: ", amended_commands)
        #                 print(self.commands)
        #                 client.send_message(amended_commands)
        #
        #         elif self.count == 2:
        #             self.count = 0
        #             amended_commands = ["STM:w020n\n"]
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 amended_commands = amended_commands + sent_commands
        #                 print("Amended commands: ", amended_commands)
        #                 print(self.commands)
        #                 client.send_message(amended_commands)
        #
        #     # Start sending algo commands
        #     elif data[0] == "START":
        #         if len(self.commands) != 0:
        #             sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #             self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #             print(sent_commands)
        #             print(self.commands)
        #             client.send_message(sent_commands)
        #             # client.close()
        #
        #     # Not valid data
        #     elif data[0] == "bullseye":
        #         print("Sending list of commands to RPi...")
        #         fixed_commands = ["STM:Ln\n", "STM:w060n\n", "STM:ln\n", "STM:w025n\n", "STM:ln\n", "STM:pn\n"]
        #         print(fixed_commands)
        #         client.send_message(fixed_commands)
        #
        #     # If no image taken
        #     elif data[0] == "-1":
        #         if self.count == 2:
        #             self.count = 0
        #             amended_commands = ["STM:w020n\n"]
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 amended_commands = amended_commands + sent_commands
        #                 print("Amended commands: ", amended_commands)
        #                 print(self.commands)
        #                 client.send_message(amended_commands)
        #
        #         else:
        #             self.count += 1
        #             correction_commands = ["STM:s010n\n", "STM:pn\n"]
        #             print(correction_commands)
        #             client.send_message(correction_commands)

    def run_rpi(self):
        while True:
            # x = 'ALG:10,17,S,0;17,17,W,1;2,16,S,2;16,4,S,3;13,1,W,4;6,6,N,5;9,11,W,6;3,3,E,7;'.encode(
            #     'utf-8')
            a = "ALG:2,17,S,0;16,17,W,1;10,11,S,2;4,6,N,3;9,2,E,4;17,5,W,5;".encode(
                "utf-8"
            )
            b = "ALG:4,18,E,0;18,18,S,1;13,13,E,2;15,1,N,3;9,2,W,4;0,14,E,5;7,7,N,6;".encode(
                "utf-8"
            )
            c = "ALG:2,9,N,0;0,17,E,1;14,15,S,2;6,2,N,3;19,4,W,4;10,5,W,5;17,19,S,6;9,18,W,7;".encode(
                "utf-8"
            )
            d = "ALG:2,18,S,0;5,18,S,1;8,18,S,2;11,18,S,3;14,18,S,4;".encode("utf-8")
            e = "ALG:0,18,E,0;18,19,S,1;18,0,W,2;5,0,E,3;10,10,E,4;9,10,W,5;".encode(
                "utf-8"
            )
            f = "ALG:6,6,N,0;16,4,W,1;9,10,W,2;2,16,S,3;8,17,E,4;17,17,S,5;".encode(
                "utf-8"
            )
            week8 = "ALG:16,1,L,0;8,5,R,1;6,12,N,2;2,18,S,3;15,16,S,4;".encode("utf-8")
            testing = (
                "ALG:6,6,N,0;16,4,W,1;9,11,W,2;2,16,S,3;10,17,S,4;17,17,W,5;".encode(
                    "utf-8"
                )
            )
            g = "ALG:3,11,E,0;7,14,S,1;9,5,N,2;".encode("utf-8")
            h = "ALG:8,2,E,1;8,6,N,2;17,0,N,3;2,16,E,4;11,11,E,5;8,18,S,6;14,18,S,7;17,14,W,8;".encode(
                "utf-8"
            )
            z = "ALG:8,2,E,1;8,6,N,2;19,0,N,3;2,16,E,4;11,11,E,5;".encode("utf-8")

            self.run_minimal(constants.RUN_SIMULATION)
            # break
            time.sleep(5)


def initialize():
    algo = Main()
    algo.run_rpi()


def sim():
    algo = Main()
    algo.run_simulator()


def test():
    print("start test")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("192.168.34.1", 6000))
    print("connected")
    server.send("12345")
    msg = server.recv(1024)
    print(msg.decode("utf-8"))


if __name__ == "__main__":
    # Test connection with RPI
    # test()

    # Run virtual simulator
    # sim()

    # Run on RPI
    initialize()

    pass
