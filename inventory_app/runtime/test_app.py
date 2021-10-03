"""

"""

from chalice.test import Client
from app import app
import json

def test_item_creation():
    """
    """

    with Client(app) as client:
        response = client.http.post(
        "/item",
        headers={'Content-Type':'application/json'},
        body=json.dumps({'name': 'Bread', 'quantity': 10})
        )

    return response


def test_item_retrieval():
    """
    """

    with Client(app) as client:
        response = client.http.get(
        "/item",
        headers={'Content-Type':'application/json'},
        body=json.dumps({'name': 'Bread'})
        )

    return response

if __name__ == '__main__':
    print(test_item_creation().body)
    print(test_item_retrieval().body)
