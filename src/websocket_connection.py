import os

import websocket
from dotenv import load_dotenv

load_dotenv()
WEBSOCKET_URI = os.environ["WEBSOCKET_URI"]


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("Closed Connection")


def on_open(ws):
    print("Opened Connection")


websocket.enableTrace(True)
ws = websocket.WebSocketApp(
    WEBSOCKET_URI,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
