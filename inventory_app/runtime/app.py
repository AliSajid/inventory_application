import os
import boto3
from chalice import Chalice, Response

from inventory import Inventory
from item import Item

app = Chalice(app_name="inventory_app")
s3 = boto3.resource("s3")
s3bucket = s3.Bucket(os.environ.get("INVENTORY_BUCKET_NAME", "test.banseljaj.com"))


@app.route("/item", methods=["POST"])
def add_or_update_item():

    """ """

    body = app.current_request.json_body
    item = Item(name=body.get("name"), quantity=body.get("quantity"))
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

    return Respone(status_code=200, body=out_body)


@app.route("/item", methods=["GET"])
def get_item():
    """ """

    body = app.current_request.json_body

    item_name = body.get("name", "")

    item_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{body['name']}.inventoryapp.work"))

    file_key = f"{item_name}/{item_id}.json"

    dumpfile = tempfile.mktemp()
    current_file = s3bucket.download_file(Key=file_key, Filename=dumpfile)

    with open(dumpfile) as f:
        data = json.load(f)

    return Response(status_code=200, body=json.dumps(data))


@app.on_s3_event(bucket=s3bucket.name, suffix=".json")
def update_inventory(event):
    """ """

    new_key = event.key

    dumpfile = tempfile.mktemp()

    s3bucket.download_file(Key=new_key, Filename=dumpfile)

    invdumpfile = tempfile.mktemp()

    invdump_key = "complete.inventory"

    if list(s3bucket.objects.filter(prefix=invdump_key)) == []:
        inv = Inventory()
        tempinvfile = tempfile.mktemp()
        inv.dump(tempfile)
        s3bucket.upload_file(tempinvfile, invdump_key)

    s3bucket.download_file(Key=invdump_key, Filename=invdumpfile)

    inventory = Inventory.load(invdumpfile)
    updated_item = Item.load(dumpfile)
    inventory.add_or_update_item(updated_item)
    inventory.dump(invdumpfile)

    s3bucket.upload_file(Filename=invdumpfile, Key=invdump_key)

    return {}


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """ """

    inventory_key = "complete.inventory"
    inventory_file = tempfile.mktemp()

    s3bucket.download_file(Key=inventory_key, Filename=inventory_file)

    inventory = Inventory.load(inventory_file)

    return Response(status_code=200, body=inventory.inventory)
