from BasicBot import BasicBot

def main():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    bot = BasicBot(api_key, api_secret)

    while True:
        try:
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            side = input("Buy or Sell: ").upper()
            order_type = input("Market or Limit: ").upper()
            quantity = float(input("Quantity: "))

            price = None
            if order_type == "LIMIT":
                price = float(input("Limit Price: "))

            side_enum = SIDE_BUY if side == "BUY" else SIDE_SELL
            order_type_enum = ORDER_TYPE_MARKET if order_type == "MARKET" else ORDER_TYPE_LIMIT

            bot.place_order(symbol, side_enum, order_type_enum, quantity, price)
        except KeyboardInterrupt:
            print("\nExiting bot.")
            break
