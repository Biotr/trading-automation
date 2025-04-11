from binance.client import Client
from binance.exceptions import BinanceAPIException

import config

client = Client(config.api_key, config.api_secret, testnet=True)


def get_precision(symbol, precision):
    exchange_info = client.futures_exchange_info()
    symbol_info = [info for info in exchange_info["symbols"] if symbol == info["symbol"]]

    return symbol_info[0][precision]


def get_percentage_balance():
    account_balance = client.futures_account_balance()
    for currency in account_balance:
        if currency["asset"] == "USDT":
            entry_usdt = round(float(currency["balance"]) * config.account_percentage / 100, 0)

    return entry_usdt


def delete_active_position(symbol, all_active_positions):
    active_position = [position for position in all_active_positions if position["symbol"] == symbol][0]
    active_position_amount = float(active_position["positionAmt"])

    try:
        if active_position_amount < 0:
            client.futures_create_order(symbol=symbol, type="MARKET", side="BUY", quantity=-active_position_amount, leverage=config.leverage)
        elif active_position_amount > 0:
            client.futures_create_order(symbol=symbol, type="MARKET", side="SELL", quantity=active_position_amount, leverage=config.leverage)
        print(f"Last {symbol} position closed")
    except Exception as err:
        print("\n CHECK YOUR CRYPTO EXCHANGE TO DELETE POSITION \n")
        print(err)


def create_order(symbol, action, price, medium_pairs):

    if symbol not in medium_pairs:
        print("Not in tradingview config")
        return

    active_positions = client.futures_position_information(symbol=symbol)
    if active_positions:
        delete_active_position(symbol, active_positions)

    open_orders = client.futures_get_open_orders(symbol=symbol)
    if open_orders:
        order_id_list = [order["orderId"] for order in open_orders if order["symbol"] == symbol]
        client.futures_cancel_orders(symbol=symbol, orderidlist=order_id_list)

    price_precision = get_precision(symbol, "pricePrecision")
    quantity_precision = get_precision(symbol, "quantityPrecision")

    entry_usdt = get_percentage_balance()
    entry_size = round((entry_usdt / float(price)), quantity_precision) * config.leverage
    entry_price = round(float(price), price_precision)

    try:
        if medium_pairs == config.trading_view_pairs:
            client.futures_create_order(symbol=symbol, type="MARKET", side=action.upper(), quantity=entry_size, leverage=config.leverage)
            print("[TRADINGVIEW]")
            print(symbol, "MARKET", action.upper(), "Coin price:", entry_price, "Quantity:", entry_size)
        else:
            client.futures_create_order(symbol=symbol, type="LIMIT", timeInForce="GTC", price=entry_price, side=action.upper(), quantity=entry_size, leverage=config.leverage)
            print("[DISCORD]")
            print(symbol, "LIMIT", action.upper(), "Coin price:", entry_price, "Quantity:", entry_size)
    except BinanceAPIException as e:
        print("Couldn't create order")

    try:
        opposite_side = "BUY" if action == "sell" else "SELL"

        if config.take_profit_roi != None:
            take_profit_pnl = entry_usdt * config.take_profit_roi / 100
            modifer = 1 if action == "buy" else -1
            take_profit = float(price) + modifer * (take_profit_pnl / entry_size)
            stop_price = round(take_profit, price_precision)
            client.futures_create_order(symbol=symbol, type="TAKE_PROFIT_MARKET", side=opposite_side, stopPrice=stop_price, closePosition=True, workingType="MARK_PRICE", priceProtect=True)
            print("Created TP", stop_price)

        if config.stop_loss_roi != None:
            stop_loss_pnl = entry_usdt * config.stop_loss_roi / 100
            modifer = -1 if action == "buy" else 1
            stop_loss = float(price) + modifer * (stop_loss_pnl / entry_size)
            stop_price = round(stop_loss, price_precision)
            client.futures_create_order(symbol=symbol, type="STOP_MARKET", side=opposite_side, stopPrice=stop_price, closePosition=True, workingType="MARK_PRICE", priceProtect=True)
            print("Created SL", stop_price)
    except BinanceAPIException as e:
        print("Couldn't create stop price orders\n", e)
