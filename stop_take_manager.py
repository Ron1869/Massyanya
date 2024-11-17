# stop_take_manager.py
# Ron Company #

from exchange_manager import get_exchange

class StopTakeManager:
    def __init__(self, symbol):
        self.exchange = get_exchange()
        self.symbol = symbol

    def close_all_positions(self):
        """Закрывает все открытые позиции для указанного символа."""
        try:
            open_positions = self.exchange.fetch_positions()
            for position in open_positions:
                if position['symbol'] == self.symbol and position['contracts'] > 0:
                    side = 'sell' if position['side'] == 'long' else 'buy'
                    amount = position['contracts']
                    self.exchange.create_market_order(self.symbol, side, amount)
                    print(f"Закрыта позиция {side} объемом {amount} для {self.symbol}")
        except Exception as e:
            print(f"Ошибка при закрытии позиций: {e}")

    def set_stop_loss_take_profit(self, side, amount, stop_loss_price, take_profit_price):
        """Устанавливает ордера стоп-лосс и тейк-профит для открытой позиции."""
        try:
            if side == 'buy':
                stop_side = 'sell'
            else:
                stop_side = 'buy'

            # Установка стоп-лосса
            stop_loss_order = self.exchange.create_order(
                self.symbol,
                type='STOP_MARKET',
                side=stop_side,
                amount=amount,
                params={'stopPrice': stop_loss_price}
            )
            print(f"Установлен стоп-лосс: {stop_loss_order}")

            # Установка тейк-профита
            take_profit_order = self.exchange.create_order(
                self.symbol,
                type='TAKE_PROFIT_MARKET',
                side=stop_side,
                amount=amount,
                params={'stopPrice': take_profit_price}
            )
            print(f"Установлен тейк-профит: {take_profit_order}")
        except Exception as e:
            print(f"Ошибка при установке стоп-лосса и тейк-профита: {e}")

    def cancel_all_orders(self):
        """Отменяет все открытые ордера для указанного символа."""
        try:
            orders = self.exchange.fetch_open_orders(self.symbol)
            for order in orders:
                self.exchange.cancel_order(order['id'], self.symbol)
                print(f"Отменен ордер {order['id']} для {self.symbol}")
        except Exception as e:
            print(f"Ошибка при отмене ордеров: {e}")
