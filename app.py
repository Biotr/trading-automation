import json, config
from binance.client import Client
from flask import Flask, request
client = Client(config.api_key, config.api_secret,testnet=True)

app = Flask(__name__)

@app.route("/webhook",methods=['GET','POST'])
def webhook():
    json_response = json.loads(request.data.decode('UTF-8'))
    order_price=float(json_response['order_price'])
    order_action=json_response['order_action'].upper()
    #Delete last position
    activePosition=client.futures_position_information(symbol=config.symbol)[0]
    activePositionAmt= float(activePosition['positionAmt'])
    try:
        if activePositionAmt < 0:
            client.futures_create_order(symbol=config.symbol,type="MARKET",side="BUY",quantity=-activePositionAmt,leverage=config.leverage)
        elif activePositionAmt > 0:
            client.futures_create_order(symbol=config.symbol,type="MARKET",side="SELL",quantity=activePositionAmt,leverage=config.leverage)
        print("Position closed")
    except Exception as err:
        print("\n CHECK YOUR CRYPTO EXCHANGE TO DELETE POSITION \n")
        print(err)
        return "<p>Invalid</p>"
    
    account_balance = client.futures_account_balance()
    for checkCoin in account_balance:
        if checkCoin["asset"]=="USDT":
            usdt_balance=round(float(checkCoin["balance"])*config.percent_of_balance/100,0)
    entry_size=(round((usdt_balance/order_price),0)*config.leverage)
    print(f"Balance {usdt_balance}")
    print(f"Entry size {entry_size}")
    #Create position
    try:
        client.futures_create_order(symbol=config.symbol,type="MARKET",side=order_action,quantity=entry_size,leverage=config.leverage)
        print("Order Created")
    except Exception as err:
        print(err)
    
    return "<p>Webhook</p>"