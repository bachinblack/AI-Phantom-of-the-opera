import os
import json
import socket
import random
from random import randrange
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict

import protocol
from nodes.nodes import MoveNode, CharacterNode, compute_gain

from nodes import (
    joseph_nodes as jn,
    raoul_nodes as rn,
    christine_nodes as cn,
)

import display

# Comment this out to disable graphic debugging
# Better disable it on every push
# display.init_debug()

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

        # For the given room id, the available passages
        self.passages = [
            (1, 4), (0, 2), (1, 3), (2, 7), (0, 5, 8),
            (4, 6), (5, 7), (3, 6, 9), (4, 9), (7, 8)
        ]

        # Available passages for pink character
        self.pink_passages = [
            (1, 4), (0, 2, 5, 7), (1, 3, 6), (2, 7), (0, 5, 8, 9),
            (4, 6, 1, 8), (5, 7, 2, 9), (3, 6, 9, 1), (4, 9, 5), (7, 8, 4, 6)
        ]

        # Update it every round
        self.gamestate = None

        # The node
        self.predictions = None

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

        # All the implemented powers
        self.characters = {
            "red": rn.RaoulNode,
            "grey": jn.JosephNode,
            "black": cn.ChristineNode,
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
        self.predictions = []
        self.bestnode = None

        for id, ch in enumerate(options):
            color = ch['color']
            # Getting the availables tiles to move to
            routes = self.passages[ch['position']] if color != 'pink' else self.pink_passages[ch['position']]
            # If the lock is in one of the available paths, removing this path from the list
            if ch['position'] in self.gamestate['blocked']:
                # inspector_logger.warn(f"removing lock route {self.gamestate['blocked']}")
                routes = [r for r in routes if r not in self.gamestate['blocked']]
            try:
                # If the character was implemented, picking it
                # (pink doesn't need any implementation, just the pink_paths)
                tmp = self.characters[color](self.gamestate, color, routes)
            except KeyError:
                # Otherwise, using default CharacterNode
                tmp = CharacterNode(self.gamestate, color, routes)
            tmp.id = id
            if self.bestnode is None or abs(tmp.get_best_gain()) < abs(self.bestnode.get_best_gain()):
                self.bestnode = tmp
            self.predictions.append(tmp)

        inspector_logger.debug(self.predictions)
        inspector_logger.warn(self.bestnode)
        if display.debugger is not None:
            display.debugger.update(
                self.gamestate,
                self.bestnode.get_best_gain(),
                f"Picked {str(self.bestnode)}"
            )

        return self.bestnode.id

    def send_position(self, options) -> int:
        index = options.index(self.bestnode.get_move_target())
        inspector_logger.debug(index)
        return index

    def send_use_power(self, options) -> int:
        return options.index(self.bestnode.power)

    def send_power_target(self, options) -> int:
        target = self.bestnode.get_power_target()
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
                print("no message, finished learning")
                self.end = True


p = Player()

p.run()
