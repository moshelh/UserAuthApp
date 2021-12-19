import requests
from datetime import datetime


LOGGER_URL = "http://logging-server:8080/log/"


def logger(massage : str, name: str, level: str) -> bool:
    now = datetime.now()
    data = {
        "asctime": now.strftime("%d/%m/%Y %H:%M:%S"),
        "name": name,
        "levelname": level,
        "massage": massage
    }
    r = requests.post(LOGGER_URL, data=data)
    if r.status_code == 200:
        return True

    return False
