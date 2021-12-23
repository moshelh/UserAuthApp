import requests
from datetime import datetime

LOGGER_URL = "http://logging-server:8080/log/"


def logger(massage: str, name: str, level: str) -> bool:
    print(massage, name, level)
    print("hello")
    now = datetime.now()
    data = {
        "asctime": "date",
        "name": name,
        "levelname": level,
        "massage": massage
    }
    r = requests.post(LOGGER_URL, data=data)
    print(r)
    if r.status_code == 200:
        return True

    return False
