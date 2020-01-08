import board
import neopixel

wifiConfig = {
    'ssid' : 'Frontier5216',             # Keep the two '' quotes around the name
    'password' : '3662233257',         # Keep the two '' quotes around password
    'timezone' : "America/New_York",  # http://worldtimeapi.org/timezones
    'aio_username' : 'benczech212',
    'aio_key' : '69d9215300f540ee9c19a24f0642125e',
    }

deviceConfig = [
    {
    "name":"External Light",
    "intensity":1.0,
    "pin":board.D4,
    "ID":"0001",
    "pixels":{
        "range":30,
        "order":neopixel.RGB,
        "min":0,
        "max":29
    },
    "channels":{
        "count":3,
        "toggle": [False,True,True],
        "names": ["Green","Red","Blue"],
        }
    },
    {
    "name":"Status Light",
    "intensity":1.0,
    "pin":board.NEOPIXEL,
    "ID":"0002",
    "pixels":{
        "range":1,
        "order":neopixel.GRB,
        "min":0,
        "max":0
        },
    "channels":{
        "count":3,
        "toggle":[True,True,True],
        "names": ["Green","Red","Blue"],
        }
    },
]

