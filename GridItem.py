from enum import Enum


class Type(Enum):
    SWITCH = 'SWITCH'
    DIMMER = 'DIMMER'
    TEMP = 'TEMP'
    DOOR = 'DOOR'
    HUMIDITY = 'HUMIDITY'


class GridItem:
    def __init__(self, name, label, ztype, key):
        self.name = name
        self.label = label
        self.ztype = ztype
        self.key = key

