import os
import logging
from binance.client import Client
from binance.enums import *

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = self.setup_logger()
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        self.logger.info("Initialized Binance Futures Testnet Client")

    def setup_logger(self):
        logger = logging.getLogger("BinanceBot")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler("bot.log")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == ORDER_TYPE_LIMIT:
                params["price"] = price
                params["timeInForce"] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**params)
            self.logger.info(f"Order placed: {order}")
            print("✅ Order placed successfully!")
            return order

        except Exception as e:
            self.logger.error(f"❌ Error placing order: {e}")
            print(f"Error: {e}")
            return None


def main():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("⚠️ Please set your Binance Testnet API credentials in environment variables.")
        return

    bot = BasicBot(api_key, api_secret)

    print("🔁 Welcome to the Binance Futures Trading Bot")

    while True:
        try:
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            side = input("Buy or Sell: ").strip().upper()
            order_type = input("Market or Limit: ").strip().upper()
            quantity = float(input("Quantity: ").strip())

            price = None
            if order_type == "LIMIT":
                price = float(input("Limit Price: ").strip())

            side_enum = SIDE_BUY if side == "BUY" else SIDE_SELL
            order_type_enum = ORDER_TYPE_MARKET if order_type == "MARKET" else ORDER_TYPE_LIMIT

            bot.place_order(symbol, side_enum, order_type_enum, quantity, price)
        except KeyboardInterrupt:
            print("\n👋 Exiting. Happy trading!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
