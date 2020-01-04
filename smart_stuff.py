def atr_calc(bid_price, ask_price, ticks, sub_ranges):
    period = 1000
    avg_price = (bid_price + ask_price) / 2
    ticks.append(avg_price)
    if len(ticks) == period:
        high_index = ticks.index(max(ticks))
        low_index = ticks.index(min(ticks))

        high_period = ticks[high_index-15:high_index+15]
        low_period = ticks[low_index-15:low_index+15]

        print('LOW', ticks.index(min(ticks)), low_period)
        print('HIGH', ticks.index(max(ticks)), high_period)


def STOCHASTIC(bid_price, ask_price, s_ticks):
    avg_price = (bid_price + ask_price) / 2
    s_ticks.append(avg_price)
    if len(s_ticks) > 500:
        high = max(s_ticks)
        low = min(s_ticks)

        s_ticks.pop(0)

        stoch = ((avg_price - low) / (high - low)) * 100
        return stoch
