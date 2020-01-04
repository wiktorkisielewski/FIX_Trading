from simplefix import FixMessage, FixParser
import trade_auth
import socket
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((trade_auth.SocketConnectHost, trade_auth.SocketConnectPort))

parser = FixParser()


def login(n):
    message = FixMessage()

    print('UTC', datetime.datetime.utcnow())
    print('LOCAL', datetime.datetime.now())

    message.append_pair(8, "FIX.4.4")
    message.append_pair(35, "A")
    message.append_pair(34, n)
    message.append_pair(49, trade_auth.SenderCompID)
    message.append_utc_timestamp(52, None)
    message.append_pair(56, trade_auth.TargetCompID)
    message.append_pair(98, "0")
    message.append_pair(108, "30")
    message.append_pair(141, "Y")
    message.append_pair(553, trade_auth.Username)
    message.append_pair(554, trade_auth.Password)

    msg = message.encode()
    print("logon msg", msg)

    s.sendall(msg)
    print("logon response", s.recv(7550))


def market_order(n, side, price):
    order = FixMessage()

    order.append_pair(8, "FIX.4.4")
    order.append_pair(35, "D")
    order.append_pair(34, n)
    order.append_pair(49, trade_auth.SenderCompID)
    order.append_utc_timestamp(52)
    order.append_pair(56, trade_auth.TargetCompID)
    order.append_pair(55, "EURUSD.spa")
    order.append_pair(54, side)
    order.append_pair(59, "3")
    order.append_utc_timestamp(60)
    order.append_pair(40, "1")
    order.append_pair(44, price)
    order.append_pair(38, "10000")
    order.append_utc_timestamp(11)

    order_msg = order.encode()
    print("sent order", order_msg)

    s.sendall(order_msg)
    print(str(s.recv(trade_auth.SocketConnectPort)).replace('\\x01', '|'))


def heartbeat_msg(n):
    heartbeat = FixMessage()

    heartbeat.append_pair(8, "FIX.4.4")
    heartbeat.append_pair(35, "0")
    heartbeat.append_pair(34, n)
    heartbeat.append_pair(49, trade_auth.SenderCompID)
    heartbeat.append_utc_timestamp(52)
    heartbeat.append_pair(56, trade_auth.TargetCompID)
    heartbeat.append_pair(57, "TRADES")

    parser.append_buffer(heartbeat.encode())
    s.sendall(heartbeat.encode())
