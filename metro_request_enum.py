from enum import Enum


class MetroRequest(Enum):
    ADD_LINE = 1
    ADD_STATION = 2
    DELETE_STATION = 3
    LIST_OF_LINE_STATIONS = 4
    LIST_OF_LINES = 5
