import os
import json
import socket
import random
from random import randrange
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict

import protocol

from nodes.move_node import compute_gain
from nodes.root_node import RootNode

import display

# Set this call to False to disable graphical debugging
# Better disable it on every push
display.init_debug(False)

host = "localhost"
port = 12000
# HEADERSIZE = 10


"""
set up inspector logging
"""
inspector_logger = logging.getLogger()
inspector_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s :: %(levelname)s :: %(message)s", "%H:%M:%S")
# file
if os.path.exists("./logs/inspector.log"):
    os.remove("./logs/inspector.log")
file_handler = RotatingFileHandler('./logs/inspector.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
inspector_logger.addHandler(file_handler)
# stream
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
inspector_logger.addHandler(stream_handler)


class Player():

    def __init__(self):

        # Update it every round
        self.gamestate = None


        self.questions = {
            "select character": self.predict_round, # Select the character that will play
            "activate+": self.send_use_power, # Use power
            "white character power move +": None, # Asking for a position for each person to displace
            "purple character power": None, # Asking for a character to bring with purple
            "grey character power": self.send_power_target, # Room to put the blackout in
            "blue character power room": None, # Room to set the lock in
            "blue character power exit": None, # Exit from the room
            "select position": self.send_position, # Position to move to
        }

        self.end = False
        # self.old_question = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def predict_round(self, options):
        if display.debugger is not None:
            display.debugger.update(
                self.gamestate,
                compute_gain(self.gamestate),
                "Current state"
            )

        # Adding options to gamestate to pass them on
        self.gamestate['options'] = options

        # Create our tree with available options
        self.tree = RootNode(self.gamestate)

        print(self.tree)
        print("-------------------------------------------")

        if display.debugger is not None:
            display.debugger.update(
                self.gamestate,
                self.tree.get_best_gain(),
                f"Picked {str(self.tree.best)}"
            )

        return self.tree.best.options_index

    def send_position(self, options) -> int:
        index = options.index(self.tree.get_move_target())
        inspector_logger.debug(index)
        return index

    def send_use_power(self, options) -> int:
        return options.index(self.tree.get_use_power())

    def send_power_target(self, options) -> int:
        target = self.tree.get_power_target()
        if (type(target) is list):
            return options.index(target.pop(0))
        return options.index(target)

    def answer(self, question):
        # work
        data = question["data"]
        self.gamestate = question["game state"]
        # log
        inspector_logger.debug("|\n|")
        inspector_logger.debug("inspector answers")
        inspector_logger.debug(f"game state--------- {self.gamestate}")
        inspector_logger.debug(f"question type ----- {question['question type']}")
        inspector_logger.debug(f"data -------------- {data}")
        # inspector_logger.debug(f"response ---------- {data[response_index]}")
        qt = question['question type']
        for qu in self.questions:
            if (qt.startswith(qu)) and self.questions[qu] is not None:
                try:
                    return self.questions[qu](data)
                except ValueError:
                    inspector_logger.warn(
                        f"Couldn't find an answer. random answer")
                    break
        return random.randint(0, len(data)-1)

    def handle_json(self, data):
        data = json.loads(data)
        response = self.answer(data)
        inspector_logger.debug(f"response index ---- {response}")
        # send back to server
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data)

    def connect(self):
        self.socket.connect((host, port))

    def reset(self):
        self.socket.close()

    def run(self):

        self.connect()

        while self.end is not True:
            received_message = protocol.receive_json(self.socket)
            if received_message:
                self.handle_json(received_message)
            else:
                self.end = True
