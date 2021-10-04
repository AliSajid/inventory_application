"""

"""
import os
import boto3
from chalice import Chalice, Response

import uuid
import json
import tempfile

from datetime import datetime

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
            app.log.debug("Item already exists. Updating.")
            self.__update_item(item)
        else:
            app.log.debug("New item. Adding to inventory")
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
            app.log.debug(f"Processing {item}")
            inv.add_or_update_item(Item(**item))
        app.log.debug(f"Inventory: {inv.inventory()}")

        return inv


app = Chalice(app_name="inventory_app")
app.api.cors = True
app.debug = True

s3 = boto3.resource("s3")
s3bucket = s3.Bucket(os.environ.get("INVENTORY_BUCKET_NAME", "inventory.banseljaj.com"))


@app.route("/item", methods=["POST"])
def add_or_update_item():

    """ """

    body = app.current_request.raw_body.decode()
    print(type(body))
    print(body)
    json_body = json.loads(str(body))
    print(json_body)
    item = Item(name=json_body.get("name"), quantity=json_body.get("quantity"))
    dumpfile = tempfile.mktemp()
    item_key = f"{item.name}/{item.id}.json"

    if list(s3bucket.objects.filter(Prefix=item.name)) != []:
        copy_source = {"Bucket": s3bucket.name, "Key": item_key}
        file_object = s3bucket.Object(key=item_key)
        newkey = f"{item.name}/{item.id}_{file_object.last_modified.date().isoformat()}_{file_object.last_modified.time().isoformat()}.json.record"
        s3bucket.copy(copy_source, newkey)

    item.dump(dumpfile)
    s3bucket.upload_file(Filename=dumpfile, Key=item_key)

    out_body = json.dumps(dict(item))

    return Response(status_code=200, body=out_body)


@app.route("/item", methods=["GET"])
def get_item():
    """ """

    item_name = app.current_request.query_params.get("name")

    item_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{item_name}.inventoryapp.work"))

    file_key = f"{item_name}/{item_id}.json"

    dumpfile = tempfile.mktemp()
    current_file = s3bucket.download_file(Key=file_key, Filename=dumpfile)

    with open(dumpfile) as f:
        data = json.load(f)

    return Response(status_code=200, body=json.dumps(data))


@app.on_s3_event(bucket=s3bucket.name, suffix=".json", events=['s3:ObjectCreated:*'])
def update_inventory(event):
    """ """

    app.log.debug("Received event for bucket: %s, key: %s",
                  event.bucket, event.key)
    new_key = event.key

    dumpfile = tempfile.mktemp()

    app.log.debug(f"Dumpfile: {dumpfile}, New Key = {new_key}")

    inventory_bucket = s3.Bucket(name=event.bucket)
    inventory_bucket.download_file(Key=new_key, Filename=dumpfile)

    invdumpfile = tempfile.mktemp()

    invdump_key = "complete.inventory"

    if list(inventory_bucket.objects.filter(Prefix=invdump_key)) == []:
        inv = Inventory()
        tempinvfile = tempfile.mktemp()
        inv.dump(tempinvfile)
        inventory_bucket.upload_file(tempinvfile, invdump_key)

    inventory_bucket.download_file(Key=invdump_key, Filename=invdumpfile)

    inventory = Inventory.load(invdumpfile)
    updated_item = Item.load(dumpfile)
    inventory.add_or_update_item(updated_item)
    inventory.dump(invdumpfile)

    inventory_bucket.upload_file(Filename=invdumpfile, Key=invdump_key)

    return {}


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """ """

    inventory_key = "complete.inventory"
    inventory_file = tempfile.mktemp()

    app.log.debug(f"Inventory Dumpfile: {inventory_file}")

    s3bucket.download_file(Key=inventory_key, Filename=inventory_file)
    with open(inventory_file) as f:
        app.log.debug(f.read())

    inventory = Inventory.load(inventory_file)

    converted = [dict(item) for item in inventory.inventory()]
    out = json.dumps(converted)
    app.log.debug(out)
    return Response(status_code=200, body=out)
