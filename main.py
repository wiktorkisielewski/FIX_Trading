import trade
import price
import threading
import time
from random import getrandbits


def coin_flip():
    return getrandbits(1)


def interpreter():
    print("wait...")
    for bid_price, ask_price, spread, spread_sum, is_safe in price.price_subscription():
        global last_bid
        global last_ask
        global safety
        safety = is_safe
        last_bid = bid_price
        last_ask = ask_price
        try:
            if len(spread_sum) >= 10:
                p_2.start()
        except RuntimeError:
            pass


def calc_stop(side, risk):
    if side == 1:
        stop = (str(last_bid * (1 - risk))).replace('.', '')
    else:
        stop = (str(last_bid * (1 + risk))).replace('.', '')

    if len(stop) > 6:
        n = len(stop) - 6
        stop = stop[:-n]
    elif len(stop) < 6:
        n = 6 - len(stop)
        stop = stop + '0' * n
    else:
        pass

    return stop[:1] + '.' + stop[1:]


def trail(side, open_price, stop_price):
    trail_stop = stop_price
    in_trade = True
    while True:
        if in_trade is True:
            if side == 1:
                if open_price < last_ask:
                    new_trail = calc_stop(side, 0.0001)
                    if new_trail >= trail_stop:
                        trail_stop = new_trail
                    else:
                        pass
                else:
                    pass
                print("up", trail_stop, "VS", calc_stop(side, 0))
                if trail_stop >= calc_stop(side, 0):
                    print("LONG LOST")
                    #trade.market_sell(n)
                    in_trade = False
            else:
                if open_price > last_bid:
                    new_trail = calc_stop(side, 0.0001)
                    if new_trail <= trail_stop:
                        trail_stop = new_trail
                    else:
                        pass
                print("down", trail_stop, "VS", calc_stop(side, 0))
                if trail_stop <= calc_stop(side, 0):
                    print("SHORT LOST")
                    #trade.market_buy(n)
                    in_trade = False
            time.sleep(1)
        else:
            print("FINITO")
            return





def main_loop():
    print("hot af")
    global n
    n = 1
    trade.login(n)
    n += 1
    print("SAFETY:", safety)
    if safety is True:
        side = coin_flip()
        print("SIDE", side)
        if side == 1:
            stop_price = calc_stop(1, 0.0001)
            trade.market_buy(n)
            open_price = last_bid
            p_3 = threading.Thread(target=trail, args=(side, open_price, stop_price))
            n += 1
            trade.long_stop(n, stop_price)
            n += 1
            p_3.start()
        elif side == 0:
            stop_price = calc_stop(0, 0.0001)
            trade.market_sell(n)
            open_price = last_ask
            p_3 = threading.Thread(target=trail, args=(side, open_price, stop_price))
            n += 1
            trade.short_stop(n, stop_price)
            n += 1
            p_3.start()
    elif safety is False:
        print("volatility kills")
    else:
        pass


p_1 = threading.Thread(target=interpreter, args=())
p_2 = threading.Thread(target=main_loop, args=())


p_1.start()
