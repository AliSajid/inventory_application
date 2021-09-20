import os
import uuid
import json
import tempfile

from datetime import datetime

import boto3
import botocore.exceptions


class Item:
    """
    A class for storing data for an item
    """

    def __init__(self, name, quantity, date=None, time=None, id=None):
        """

        :param name:
        :param quantity:
        """
        self.name = name
        self.quantity = quantity
        if date is None:
            self.date = datetime.utcnow().date().isoformat()
        else:
            self.date = date
        if time is None:
            self.time = datetime.utcnow().time().isoformat()
        else:
            self.time = time
        if id is None:
            self.id = str(
                uuid.uuid5(uuid.NAMESPACE_DNS, f"{self.name}.inventoryapp.work")
            )
        else:
            self.id = id

    def __repr__(self):
        return f"<Item: {self.name}, Quantity:{self.quantity}>"

    def __eq__(self, other):
        return self.id == other.id

    def __iter__(self):
        """

        :return:
        """
        yield "id", self.id
        yield "name", self.name
        yield "quantity", self.quantity
        yield "date", self.date
        yield "time", self.time

    def dump(self, file):
        """

        :return:
        """
        with open(file, "w") as f:
            json.dump(dict(self), f)

    @classmethod
    def load(cls, filename):
        """

        :return:
        """
        with open(filename, "r") as f:
            data = json.load(f)

        return cls(**data)
