from client.metro_client import MetroClient
from metro_request_enum import MetroRequest

metro_client = MetroClient()

response = metro_client.call([MetroRequest.LIST_OF_LINES.value, []])
print(response)
