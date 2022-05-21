from client.metro_client import MetroClient

metro_client = MetroClient()

metro_client.add_line('Pink')
response = metro_client.get_lines_list()
print(response)
