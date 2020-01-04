from simplefix import FixMessage, FixParser
import price_auth
import socket
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((price_auth.SocketConnectHost, price_auth.SocketConnectPort))

parser = FixParser()


def logon(n):
    message = FixMessage()

    message.append_pair(8, "FIX.4.4")
    message.append_pair(35, "A")
    message.append_pair(34, n)
    message.append_pair(49, price_auth.SenderCompID)
    message.append_utc_timestamp(52)
    message.append_pair(56, price_auth.TargetCompID)
    message.append_pair(98, "0")
    message.append_pair(141, "Y")
    message.append_pair(108, "30")
    message.append_pair(553, price_auth.Username)
    message.append_pair(554, price_auth.Password)

    parser.append_buffer(message.encode())
    sent = parser.get_message()
    print("logon2 request ", sent)

    s.sendall(message.encode())
    response = s.recv(5201)

    parser.append_buffer(response)
    out = parser.get_message()
    print("logon response2", out)


def heartbeat_msg(n):
    heartbeat = FixMessage()

    heartbeat.append_pair(8, "FIX.4.4")
    heartbeat.append_pair(35, "0")
    heartbeat.append_pair(34, n)
    heartbeat.append_pair(49, price_auth.SenderCompID)
    heartbeat.append_utc_timestamp(52)
    heartbeat.append_pair(56, price_auth.TargetCompID)
    heartbeat.append_pair(57, "QUOTE")

    s.sendall(heartbeat.encode())


def data_subscribe(n):
    data = FixMessage()

    data.append_pair(8, "FIX.4.4")
    data.append_pair(35, "V")
    data.append_pair(49, price_auth.SenderCompID)
    data.append_pair(56, price_auth.TargetCompID)
    data.append_pair(34, n)
    data.append_utc_timestamp(52)
    data.append_pair(262, "2")
    data.append_pair(263, "1")
    data.append_pair(264, "1")
    data.append_pair(265, "0") #1
    data.append_pair(146, "1")
    data.append_pair(55, "EURUSD.spa")
    data.append_pair(267, "2")
    data.append_pair(269, "0")
    data.append_pair(269, "1")

    sent = data.encode()
    print("data request ", sent)

    s.sendall(data.encode())
    print(s.recv(price_auth.SocketConnectPort))


def calculate_spread(ask_price, bid_price):
    if ask_price > bid_price:
        return ask_price - bid_price
    elif bid_price > ask_price:
        return bid_price - ask_price
    elif bid_price == ask_price:
        return 0


def safety_first(spread_sum, spread, is_safe):
    if spread >= 0:
        spread_sum.append(spread)
    if len(spread_sum) > 500:
        spread_sum.pop(0)

    if sum(spread_sum[-10:]) > 100:
        #spread_sum.clear()
        is_safe = False
        #print('SPREADS WIDE', sum(spread_sum[-20:]), datetime.datetime.now())
    else:
        is_safe = True

    return spread_sum, is_safe


def price_subscription():
    spread_sum = []
    is_safe = True
    n = 1
    logon(n)
    n += 1
    print("gathering market data...")
    data_subscribe(n)
    n += 1
    ticks = []
    sub_ranges = []
    in_long = False
    in_short = False
    x = 1
    while True:
        out = str(s.recv(price_auth.SocketConnectPort))

        if '35=W' in out:
            bid_index = out.find('269=0')
            bid_price = (((out[bid_index + 13:bid_index + 20]).replace('.', '')).replace('\\', '')).replace('x', '')

            ask_index = out.find('269=1')
            ask_price = (((out[ask_index + 13:ask_index + 20]).replace('.', '')).replace('\\', '')).replace('x', '')

            if len(bid_price) > len(ask_price):
                ask_price = ask_price + ('0' * (len(bid_price) - len(ask_price)))
            elif len(ask_price) > len(bid_price):
                bid_price = bid_price + ('0' * (len(ask_price) - len(bid_price)))

            ask_price = int(float((ask_price.replace(' ', ''))))
            bid_price = int(float((bid_price.replace(' ', ''))))
            spread = calculate_spread(ask_price, bid_price)
            spread_sum, is_safe = safety_first(spread_sum, spread, is_safe)
            #subATR = smart_stuff.atr_calc(bid_price, ask_price, ticks, sub_ranges)
            if x < 122:
                print(x)
                x += 1

            ticks.append((bid_price + ask_price) / 2)

            ma_66 = round(sum(ticks[-66:]) / 66)
            ma_122 = round(sum(ticks[-122:]) / 122)
            side_out = None

            if len(ticks) > 200:
                if ma_66 > ma_122 and in_long is False:
                    print('BUY', datetime.datetime.now())
                    side_out = 1
                    in_long = True
                    in_short = False
                elif ma_66 < ma_122 and in_short is False:
                    print('SELL', datetime.datetime.now())
                    side_out = 2
                    in_short = True
                    in_long = False

            if len(ticks) > 122:
                ticks.pop(0)

            #print("BID:", bid_price, "ASK:", ask_price, 'SPREAD', spread, 'ATR', subATR, subSTOCH, datetime.datetime.now())

            yield bid_price, ask_price, spread_sum, is_safe, side_out


price_subscription()

