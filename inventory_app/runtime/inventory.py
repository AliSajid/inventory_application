"""

"""

import os
import uuid
import json
import tempfile


class Inventory:
    def __init__(self):
        """ """
        self.__inventory = []

    def __len__(self):
        return len(self.__inventory)

    def add_or_update_item(self, item: Item):
        """

        :param item:
        :return:
        """
        if item in self.__inventory:
            self.__update_item(item)
        else:
            self.__inventory.append(item)

    def __update_item(self, item: Item):
        """

        :param item:
        :return:
        """
        updated = []
        for it in self.__inventory:
            if it == item:
                updated.append(item)
            else:
                updated.append(it)
        self.__inventory = updated

    def inventory(self):
        return self.__inventory

    def dump(self, file):
        converted = [dict(item) for item in self.__inventory]
        with open(file, "w") as f:
            json.dump(converted, f)

    @classmethod
    def load(cls, file):
        with open(file) as f:
            data = json.load(f)
        inv = cls()
        for item in data:
            inv.add_or_update_item(Item(**item))

        return inv
