# FIX_Trading
A sandbox made in python allowing anyone to trade through FIX protocol (Financial Information Exchange).

# Basic utilities
price.py and trade.py are made to create and send basic FIX messages throught web socket. They both need auth.py file that should look like this:

SessionQualifier = '######'
SenderCompID = '#####'
TargetCompID = '#####'
Username = '#####'
Password = '#####'
SocketConnectHost = '#####'
SocketConnectPort = ###

price.py file is responsible for updating quotes (prices), they should be gathered from broker or exchange server.
trade.py is made for sending orders and reciving execution reports.
They both have similar heartbeat messages which should be sent in a loop to keep connection alive.

# Example trading algo
random_atr_tp.py is an example bot which executes trades on its own. 
It may have open only one possition at a given time and only when market conditions are safe (low spreads, high liquidity).
Every trade is opened in a random direction (it either profits from rise or fall of the underlying asset price).
After a trade is executed it monitors the market in order to lower possible risk. 
A stop (cut out) point is always set, it may move the stop point higher after a small favorable move in order to pay for the commisions in case of failed trade.
If the conditions are very good it may close a possition while trying to make the biggest gain possible.
