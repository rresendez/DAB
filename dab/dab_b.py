import time
import sys, getopt
import datetime
from poloniex import poloniex

def main(argv):
    period=10
    pair="BTC_ETC"
    prices =[]
    currentMovingAverage =0;
    lengthOfMA =0
    fee = 0.0025
    qt = 0.001
    minT =0.0001

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

    # Aqui va la clave compadre!
    conn = poloniex('','')
    while True:
        # parity one whole object
        eth_btc = conn.api_query("returnOrderBook",{'currencyPair':'BTC_ETH'})
        # parity two whole object
        btc_xcn = conn.api_query("returnOrderBook",{'currencyPair':'BTC_ETC'})
        # parity three whole object
        eth_xcn = conn.api_query("returnOrderBook",{'currencyPair':'ETH_ETC'})
        # last ask parity one
        eth_btc_A =float(eth_btc['asks'][0][0])
        # Quantitu Ethereum
        qe = eth_btc['asks'][0][1]

        print("This is QE: %s" %qe)
        # last ask paraity one minus fee
        eth_btc_AF =float(eth_btc_A)*(1.0-fee)
        # last bid parity two
        btc_xcn_B = float(btc_xcn['bids'][0][0])
        # quantity bitcoin x coin
        qb= btc_xcn['bids'][0][1]
        # last bid parity two plus fee
        btc_xcn_BF =float(btc_xcn_B)*(1.0+fee)
        print("This is QB: %s" %qb)



        # last ask parity three
        eth_xcn_A = float(eth_xcn['asks'][0][0])
        #Quantity xcoin
        qx = eth_xcn['asks'][0][1]
        #print qx
        print("This is QX: %s" %qx)
        # last ask parity three minus fee
        eth_xcn_AF =float(eth_xcn_A)*(1.0-fee)

        snt = float(btc_xcn_BF)/float(eth_btc_AF)
        # quanitity on x coins
        q1 = qe* eth_btc_A
        q2 = qb* btc_xcn_B
        q3 = qx* btc_xcn_B
        print ("Q1 is : %s Q2 is : %s Q3 is : %s \n" %(q1,q2,q3) )


        #print "btc_xcn last bid in btc: %s \n " %btc_xcn['bids'][0][0]
        print "Syntetic price: %s \n :"%snt
        #print "eth_xcn bids: %s\n " %eth_xcn['bids']
        print "Eth / X coin price: %s \n "%str(eth_xcn_AF)


        if(snt < eth_xcn_AF):

            print("There is arbitrage BITCH!!!\n")

            if(qt<q1 and qt<q2 and qt<q3):
                print("Were are using QT: %s\n"%qt)
            elif(q1<q2 and q1<q3 and q1>minT):
                print("Were are using Q1: %s\n"%q1)
            elif(q2<q3 and q2>minT):
                print("Were are using Q2: %s\n"%q2)
            elif(q3>minT):
                print("Were are using Q3: %s\n"%q3)
            else:
                print("Fuck you bitch -Edgar Salinas mintT %s\n"%minT)
        else:
            print("There aint arbitrage BITCH!!!\n")





        #lastPairPrice = currentValues[pair]["last"]
        lastPairPrice =0
        if (len(prices)>0):
            currentMovingAverage =sum(prices)/float(len(prices))

        print "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+" Period: %ss %s %s Moving Average: %s"%(period,pair,lastPairPrice,currentMovingAverage)

        prices.append(float(lastPairPrice))
        price= prices[-lengthOfMA]
        time.sleep(1)

if __name__ =="__main__":
    main(sys.argv[1:])
