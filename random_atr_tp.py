import trade_2 as trade
import price_2 as price
import threading
import time
import datetime
import random


def interpreter():
    x = 1
    print(datetime.datetime.now())
    for bid_price, ask_price, spread_sum, is_safe, subATR in price.price_subscription():
        global last_bid
        global last_ask
        global safety
        global ATR
        ATR = subATR
        safety = is_safe
        try:
            thread_3.start()
        except RuntimeError:
            pass
        if bid_price != 0:
            last_bid = bid_price
            last_ask = ask_price
            print(ATR)
            x += 1
            if (x % 50) == 0:
                print(x)
                print(datetime.datetime.now())
        else:
            pass
        try:
            if len(spread_sum) >= 7000000:
                thread_2.start()
        except RuntimeError:
            pass


def keep_alive():
    a = 3
    while True:
        price.heartbeat_msg(a)
        a += 1
        time.sleep(20)


n = 1


def keep_alive_2():
    while True:
        global n
        time.sleep(20)
        trade.heartbeat_msg(n)
        n += 1


def calc_stop(side, risk):
    if side == 1:
        stop = (str(last_bid * (1 - risk))).replace('.', '')
    else:
        stop = (str(last_ask * (1 + risk))).replace('.', '')

    if len(stop) > 6:
        x = len(stop) - 6
        stop = stop[:-x]
    elif len(stop) < 6:
        x = 6 - len(stop)
        stop = stop + '0' * x
    else:
        pass

    return stop[:1] + '.' + stop[1:]


def risk():
    risk_factor = (ATR * 13) / ((last_bid + last_ask) / 2)

    if risk_factor > 0.00001:
        while not 0.001 >= risk_factor >= 0.0001:
            risk_factor = risk_factor / 10
    else:
        while not 0.001 >= risk_factor >= 0.0001:
            risk_factor = risk_factor * 10

    if risk_factor > 0.00072:
        risk_factor = risk_factor / 2
    elif risk_factor < 0.00031:
        risk_factor = risk_factor * 2

    risk_factor = risk_factor * 2.3

    return risk_factor


def harvest_cash():
    in_trade = False
    global n
    trade.login(n)
    n += 1
    thread_4.start()
    print('SAFETY', safety)
    while True:
        if in_trade is False and safety is True:

            x = random.getrandbits(1)
            if x == 0:
                side = 1
            elif x == 1:
                side = 2

            risk_factor = 0.0009
            print('RISK', risk_factor)

            trade.market_order(n, side, calc_stop(side, 0))
            n += 1

            if side == 1:
                open_price = last_ask
            else:
                open_price = last_bid

            print('OPEN PRICE', open_price, datetime.datetime.now())

            in_trade = True
            stops_set = False

        elif in_trade is False and safety is False:
            print('MARKET NOT SAFE', datetime.datetime.now())
            time.sleep(600)

        if in_trade is True and safety is True:
            if side == 1:
                if stops_set is False:
                    stop_price = calc_stop(side, (risk_factor / 2))
                    tp_price = calc_stop(2, risk_factor)
                    brkvn_on = (str(open_price + 35))[:1] + '.' + (str(open_price + 35))[1:]
                    brkvn_spot = (str(open_price + 10))[:1] + '.' + (str(open_price + 10))[1:]
                    brkvn = False
                    trail_set = False
                    print('STOP PRICE', stop_price, 'TP', tp_price, 'BRKVN_SPOT', brkvn_spot, 'BRKVN_ON', brkvn_on,
                          datetime.datetime.now())
                    stops_set = True

                if calc_stop(side, 0) >= brkvn_on and brkvn is False:
                    stop_price = brkvn_spot
                    brkvn = True
                    print('BRKVN', stop_price, datetime.datetime.now())

                if calc_stop(side, 0) >= tp_price and trail_set is False:
                    trail_stop = calc_stop(side, risk_factor / 2)
                    print('TRAIL ON', trail_stop, datetime.datetime.now())
                    trail_set = True

                if trail_set is True:
                    new_trail = calc_stop(side, risk_factor / 2)
                    if new_trail > trail_stop:
                        trail_stop = new_trail
                        print('TRAIL UPPPP', trail_stop, datetime.datetime.now())
                    else:
                        pass

                if trail_set is True:
                    if trail_stop >= calc_stop(side, 0):
                        print("LONG WON")
                        trade.market_order(n, 2, calc_stop(side, 0))
                        n += 1
                        in_trade = False
                        trail_set = False
                        brkvn = False
                        time.sleep(random.randint(260, 470))

                if calc_stop(side, 0) <= stop_price:
                    print("LONG LOST", datetime.datetime.now())
                    trade.market_order(n, 2, calc_stop(side, 0))
                    n += 1
                    in_trade = False
                    brkvn = False
                    time.sleep(random.randint(260, 470))

            else:
                if stops_set is False:
                    stop_price = calc_stop(side, (risk_factor / 2))
                    tp_price = calc_stop(1, risk_factor)
                    brkvn_on = (str(open_price - 35))[:1] + '.' + (str(open_price - 35))[1:]
                    brkvn_spot = (str(open_price - 10))[:1] + '.' + (str(open_price - 10))[1:]
                    brkvn = False
                    trail_set = False
                    print('STOP PRICE', stop_price, 'TP', tp_price, 'BRKVN_SPOT', brkvn_spot, 'BRKVN_ON', brkvn_on,
                          datetime.datetime.now())
                    stops_set = True

                if calc_stop(side, 0) <= brkvn_on and brkvn is False:
                    stop_price = brkvn_spot
                    brkvn = True
                    print('BRKVN', stop_price, datetime.datetime.now())

                if calc_stop(side, 0) <= tp_price and trail_set is False:
                    trail_stop = calc_stop(side, risk_factor / 2)
                    print('TRAIL ON', trail_stop, datetime.datetime.now())
                    trail_set = True

                if trail_set is True:
                    new_trail = calc_stop(side, risk_factor / 2)
                    if new_trail < trail_stop:
                        trail_stop = new_trail
                        print('TRAIL DOWNN', trail_stop, datetime.datetime.now())
                    else:
                        pass

                if trail_set is True:
                    if trail_stop <= calc_stop(side, 0):
                        print("SHORT WON")
                        trade.market_order(n, 1, calc_stop(side, 0))
                        n += 1
                        in_trade = False
                        trail_set = False
                        brkvn = False
                        time.sleep(random.randint(260, 470))

                if calc_stop(side, 0) >= stop_price:
                    print("SHORT LOST", datetime.datetime.now())
                    trade.market_order(n, 1, calc_stop(side, 0))
                    n += 1
                    in_trade = False
                    brkvn = False
                    time.sleep(random.randint(260, 470))

                    # return
        elif in_trade is True and safety is False:
            print('NOT SAFE', datetime.datetime.now())
            if side == 1:
                trade.market_order(n, 2, calc_stop(side, 0))
                in_trade = False
                n += 1
                print('MARKET NOT SAFE', datetime.datetime.now())
                time.sleep(600)
            elif side == 2:
                trade.market_order(n, 1, calc_stop(side, 0))
                in_trade = False
                n += 1
                print('MARKET NOT SAFE', datetime.datetime.now())
                time.sleep(600)
        time.sleep(0.1)


thread_1 = threading.Thread(target=interpreter)
thread_2 = threading.Thread(target=harvest_cash)
thread_3 = threading.Thread(target=keep_alive)
thread_4 = threading.Thread(target=keep_alive_2)


thread_1.start()

