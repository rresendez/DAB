import time
import sys, getopt
import datetime
from poloniex import poloniex

def main(argv):
    period=10
    pair="BTC_XRP"
    prices =[]
    currentMovingAverage =0;
    lengthOfMA =0
    fee = 0.0025

    try:
        opts,args =getopt.getopt(argv,"hp:c:n:",["peroid=","currency=","points"])
    except getopt.GetoptError:
        print 'trading-bot.py -p <period length -c <currency pair> -n <period of moving avarage>'
        sys.exit(2)

    for opt,arg in opts:
        if opt == '-h':
            print 'trading-bot.py -p <period length -c <currency pair> -n <period of moving avarage>'
            sys.exit()
        elif opt in ("-p", "--period"):
            if(int(arg) in [300,900,1800,7200,14400,86400]):
                period = arg
            else:
                print 'Poloniex requires perdios bla bal bla'
                sys.exit(2)
        elif opt in ("-c", "--currency"):
                pair = args
        elif opt in ("-n", "--points"):
                lengthOfMA = int(arg)


    conn = poloniex('QNJX0IAV-XPVQQNBK-3WLERMOA-HNVY4PVL','35562d33daecb1e2d50dc662abaa42ae2edf4cf9b86b9ca93e00f2ab124657394fb96f7b8a8c0c2f46ca958314bb5d24a3ed4044cab227e4f9f2fa6c89f76316')
    while True:
        eth_btc = conn.api_query("returnOrderBook",{'currencyPair':'BTC_ETH'})
        btc_xcn = conn.api_query("returnOrderBook",{'currencyPair':'BTC_ETC'})
        eth_xcn = conn.api_query("returnOrderBook",{'currencyPair':'ETH_ETC'})
        eth_btc_A = eth_btc['asks'][0][0]
        eth_btc_A =float(eth_btc_A)*(1.0+fee)
        btc_xcn_B = btc_xcn['bids'][0][0]
        btc_xcn_B =float(btc_xcn_B)*(1.0-fee)
        eth_xcn_A = eth_xcn['asks'][0][0]
        eth_xcn_A =float(eth_xcn_A)*(1.0-fee)
        snt = float(btc_xcn_B)/float(eth_btc_A)
        #print "eth_btc ask: %s\n " %eth_btc['asks']
        print "eth_btc last ask in btc: %s\n " %eth_btc['asks'][0][0]
        #print "btc_xcn bids: %s\n " %btc_xcn['bids']
        #print "btc_xcn last bid in btc: %s \n " %btc_xcn['bids'][0][0]
        print "Syntetic price: %s \n :"%snt
        #print "eth_xcn bids: %s\n " %eth_xcn['bids']
        print "Eth / X coin price: %s \n "%str(eth_xcn_A)

        #lastPairPrice = currentValues[pair]["last"]
        lastPairPrice =0
        if (len(prices)>0):
            currentMovingAverage =sum(prices)/float(len(prices))

        print "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+" Period: %ss %s %s Moving Average: %s"%(period,pair,lastPairPrice,currentMovingAverage)

        prices.append(float(lastPairPrice))
        price= prices[-lengthOfMA]
        time.sleep(10)

if __name__ =="__main__":
    main(sys.argv[1:])
