import sqlite3
import random
import os

from termcolor import cprint, colored

from amity.database.database_file import Database
from amity.Person import Fellow, Staff
from amity.Room import Living_Space, Office


class Amity(object):
    all_persons = []
    all_allocations = {
        'office': {},
        'living_space': {}
        }
    all_unallocated = []
    all_rooms = []

    def create_room(self, room_type, room_name):
        """

        Create a list of rooms depending on the user's input

        """
        if room_type == 'O':
            if (item for item in all_rooms if item["name"] == "Pam"):
