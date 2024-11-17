# order_manager.py
# Ron Company #

import time
from exchange_manager import exchange_manager

def place_order(symbol, side, amount, leverage):
    """Размещает рыночный ордер для указанного символа и стороны (покупка или продажа)."""
    try:
        exchange = exchange_manager.get_exchange()
        # Устанавливаем плечо
        exchange.fapiPrivate_post_leverage({'symbol': symbol.replace('/', ''), 'leverage': leverage})

        # Размещаем рыночный ордер
        order = exchange.create_market_order(symbol, side, amount)
        print(f"Ордер на {side} размещен: {order}")
        return order
    except Exception as e:
        print(f"Ошибка при размещении ордера: {e}")
        return None

def set_stop_loss_take_profit(symbol, side, amount, stop_loss_percent, take_profit_percent):
    """Устанавливает стоп-лосс и тейк-профит для уже размещенного ордера."""
    try:
        exchange = exchange_manager.get_exchange()
        current_price = exchange.fetch_ticker(symbol)['last']

        # Рассчитываем цены стоп-лосса и тейк-профита
        stop_loss_price = current_price * (1 - stop_loss_percent / 100) if side == 'buy' else current_price * (1 + stop_loss_percent / 100)
        take_profit_price = current_price * (1 + take_profit_percent / 100) if side == 'buy' else current_price * (1 - take_profit_percent / 100)

        # Размещаем стоп-лосс
        stop_loss_order = exchange.create_order(
            symbol, 'STOP_MARKET', 'sell' if side == 'buy' else 'buy', amount, None, {'stopPrice': stop_loss_price}
        )
        print(f"Стоп-лосс ордер размещен: {stop_loss_order}")

        # Размещаем тейк-профит
        take_profit_order = exchange.create_order(
            symbol, 'TAKE_PROFIT_MARKET', 'sell' if side == 'buy' else 'buy', amount, None,
            {'stopPrice': take_profit_price}
        )
        print(f"Тейк-профит ордер размещен: {take_profit_order}")

    except Exception as e:
        print(f"Ошибка при установке стоп-лосса/тейк-профита: {e}")

def close_all_positions(symbol):
    """Закрывает все позиции по указанному символу."""
    try:
        exchange = exchange_manager.get_exchange()
        positions = exchange.fetch_positions()
        for position in positions:
            if position['symbol'] == symbol and position['contracts'] > 0:
                side = 'sell' if position['side'] == 'long' else 'buy'
                amount = position['contracts']
                exchange.create_market_order(symbol, side, amount)
                print(f"Позиция по {symbol} закрыта: {amount} контрактов {side}")
    except Exception as e:
        print(f"Ошибка при закрытии позиций: {e}")

def evaluate_and_place_order(symbol, side, amount, leverage, stop_loss_percent, take_profit_percent, min_profit_percent, commission_rate):
    """Оценивает потенциальную прибыль сделки и размещает ордер, если прибыль выше комиссии."""
    try:
        exchange = exchange_manager.get_exchange()
        current_price = exchange.fetch_ticker(symbol)['last']

        # Рассчитываем потенциальную прибыль в процентах
        target_price = current_price * (1 + take_profit_percent / 100) if side == 'buy' else current_price * (1 - take_profit_percent / 100)
        potential_profit_percent = (target_price - current_price) / current_price * 100 if side == 'buy' else (current_price - target_price) / current_price * 100

        # Учитываем комиссию
        total_commission = commission_rate * 2  # комиссия на вход и выход
        net_profit_percent = potential_profit_percent - total_commission

        if net_profit_percent >= min_profit_percent:
            print(f"Потенциальная прибыль: {net_profit_percent:.2f}%, размещение ордера.")
            order = place_order(symbol, side, amount, leverage)
            if order:
                set_stop_loss_take_profit(symbol, side, amount, stop_loss_percent, take_profit_percent)
        else:
            print(f"Потенциальная прибыль: {net_profit_percent:.2f}% меньше минимальной требуемой прибыли. Сделка не будет размещена.")
    except Exception as e:
        print(f"Ошибка при оценке и размещении ордера: {e}")
