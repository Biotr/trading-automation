import json

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

import config
from binance_app import create_order

app = FastAPI()


class OrderData(BaseModel):
    symbol: str
    order_action: str
    order_price: str


@app.post("/webhooks/tradingview")
async def webhook(order_data: OrderData):
    create_order(order_data.symbol, order_data.order_action, order_data.order_price, config.trading_view_pairs)
    return {"Nothgin": "Nothin"}


@app.websocket("/websockets/discord")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        order = json.loads(data)
        create_order(order["symbol"], order["order_action"], order["order_price"], config.discord_pairs)
