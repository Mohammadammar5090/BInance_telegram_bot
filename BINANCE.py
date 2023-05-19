from decouple import config
from binance.client import Client
from datetime import datetime
import time
import pandas as pd 
from binance.helpers import round_step_size
from binance.enums import *
from win32com import client as cle


# API Key and Secret Key get fron env file 
client = Client(config('Pkey'), config('Skey'))

# Get the time from milliseconds to normal time
def get_time(milli_seconds):
    timestamp = milli_seconds/1000
    # Convert timestamp to datetime object
    time = datetime.fromtimestamp(timestamp)
    # Extract hour and minute
    day= time.day
    hour = time.hour
    minute = time.minute
    second = time.second
    return f'{hour}:{minute}:{second}'


######################################################################################################################################
######################################################## INFO ########################################################################
######################################################################################################################################
   

# Get binance server time
def get_binance_time():
    time_res = client.get_server_time()
    time = datetime.fromtimestamp(time_res["serverTime"]/1000)
    # Extract hour , minute and second
    day= time.day
    hour = time.hour
    minute = time.minute
    second = time.second
    print(f'Day:{day} Time--> {hour}:{minute}:{second}')

# Get binance "status 0: normal 1:system maintenance / msg 'normal' or 'System maintenance'
def sys_status():
    status = client.get_system_status()["status"]
    msg = client.get_system_status()["msg"]
    
    if (status==0 )and (msg=="normal"):
        return True
    else:
        return False

# GET all coin USDT/BUSD that is (available for deposit and withdraw) for user
def get_all_coin_info():
    c=0
    info = client.get_all_tickers()
    for coin in info:
        for i in coin:
            i=coin[i]
            if (i[-4:] =="BUSD") or (i[-4:0] =="USDT"):
                print(coin)
                c+=1
    print(c)

# Get daily account snapshot of 'SPOT'
def get_snapshot():
    info = client.get_account_snapshot(type='SPOT')
    for i in info:
        print(i)

# Get the Order Book for the market return: (type parameter)'lastUpdateId' , 'bids : the buy order in market' , 'asks: the sell order in market'
# This function will always work in the background to notify the user of the entry or exit of a large amount
# must the (coin parameter) be all the coin in market as list or func (from get_all_coin_info)
def get_marke_depth(coin,type):
    depth = client.get_order_book(symbol=coin,limit=1)
    for i in depth[type]:
        print(i)
    
 # Get recent trades  
 # This function will always work in the background to notify the user of the entry or exit of a large amount      
def get_market_recent_trades(coin):
    trades = client.get_recent_trades(symbol=coin,limit=1)
    for i in trades:
        print(f'[price:{i["price"]},qty:{i["qty"]},quoteQty:{i["quoteQty"]}]')

# Get the older trades that already done
# must the (coin parameter) be all the coin in market as list or func (from get_all_coin_info)
def get_historical_market_trades(coin):
    trades = client.get_historical_trades(symbol=coin,limit=1)
    for i in trades:
        print(f'[price:{i["price"]},qty:{i["qty"]},quoteQty:{i["quoteQty"]}]')

# Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.
# We will look into it later***********
def get_aggregate(coin):
    trades = client.get_aggregate_trades(symbol=coin,limit=1)
    for i in trades:
        print(i)

# Get the candle that are happening now according to different times of the candle :(KLINE_INTERVAL_1MINUTE,KLINE_INTERVAL_30MINUTE,KLINE_INTERVAL_1WEEK )
# candl_time  parametr will be called later
# limit : gets you a list of all operations that have taken place since this candle appeared
def get_candlesticks_now(coin,candl_time=0):
    candles = client.get_klines(symbol=coin, interval=Client.KLINE_INTERVAL_30MINUTE,limit=1)
    for one_candle in candles:
        one_candle[0]="Open time : "+str(get_time(one_candle[0])) #
        one_candle[1]="Open : "+str(one_candle[1])
        one_candle[2]="High : "+str(one_candle[2])
        one_candle[3]="Low : "+str(one_candle[3])
        one_candle[4]="Close : "+str(one_candle[4])
        one_candle[5]="Volume : "+str(one_candle[5])
        one_candle[6]="Close time : "+str(one_candle[6])
        one_candle[7]="Quote asset volume : "+str(one_candle[7])
        one_candle[8]="Number of trades : "+str(one_candle[8])
        one_candle[9]="Taker buy base asset volume : "+str(one_candle[9])
        one_candle[10]="Taker buy quote asset volume : "+str(one_candle[10])
        one_candle[11]="Can be ignored : "+str(one_candle[11])
        for i in one_candle:
            print(i)
        print("#################################")

 #Get the historical candle that according to different times of the candle 
def get_Historical_candlesticks(coin):
    # fetch 30 minute klines for the last day up until now
    klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC")
    for one_candle in klines:
        one_candle[0]="Open time : "+str(get_time(one_candle[0])) #
        one_candle[1]="Open : "+str(one_candle[1])
        one_candle[2]="High : "+str(one_candle[2])
        one_candle[3]="Low : "+str(one_candle[3])
        one_candle[4]="Close : "+str(one_candle[4])
        one_candle[5]="Volume : "+str(one_candle[5])
        one_candle[6]="Close time : "+str(one_candle[6])
        one_candle[7]="Quote asset volume : "+str(one_candle[7])
        one_candle[8]="Number of trades : "+str(one_candle[8])
        one_candle[9]="Taker buy base asset volume : "+str(one_candle[9])
        one_candle[10]="Taker buy quote asset volume : "+str(one_candle[10])
        one_candle[11]="Can be ignored : "+str(one_candle[11])
        for i in one_candle:
            print(i)
        print("#################################")

# Current average price for a symbol.
def get_average_price(coin):
    avg_price = client.get_avg_price(symbol=coin)
    print(f'{coin} : {avg_price["price"]}')

# Get 24 hour price change statistics.
def get_24hr_Ticker(coin):
    tickers = client.get_ticker(symbol=coin)
    for i in tickers:
        print(i," : ",tickers[i])

# Latest price for all symbols.
def get_all_prices():
    prices = client.get_all_tickers()
    for i in prices:
        print(i)
    print(len(prices))

# Get first bid and ask entry in the order book for all markets,'bid : the buy order in market that will happen' , 'ask: the sell order in market that will happen'
def get_orderbook_coins():
    tickers = client.get_orderbook_tickers()
    for i in tickers:
        print(i)

# Get the exact current price of the currency
def get_current_price(coin):
    trades = client.get_aggregate_trades(symbol=coin,limit=1)[0]["p"]
    return float(trades)

######################################################################################################################################
######################################################## Orders ######################################################################
######################################################################################################################################

#########################################################################################################

# Get the minimum qty for the coin (formated W.R.T binance) that binance accepts 
def qty_ticker_info(coin):
    info=client.get_symbol_info(coin)
    min_qty2=pd.to_numeric(info["filters"][1]["minQty"])
    return min_qty2 # return as tuple

# Get the minimum price for the coin (formated W.R.T binance) that binance accepts 
def price_ticer_info(coin): 
    info = client.get_symbol_info(coin)
    minPrice = pd.to_numeric(info['filters'][0]['minPrice'])  #  0 to isolate  price precision   #  2 to isloate qty 
    return minPrice # return as tuple


# Get the formated value of coin W.R.T free BUSD/USDT that binance will accepts it
def format_value(valuetoformatx,fractionfactorx):

    value = valuetoformatx
    fractionfactor = fractionfactorx
    Precision = abs(int(f'{fractionfactor:e}'.split('e')[-1]))
    FormattedValue = float('{:0.0{}f}'.format(value, Precision))
    return FormattedValue
#######################################################################################################

#  Enter the information that the 3 function above need 
def make_order(coin):
    free=float(client.get_asset_balance(asset=coin[-4:])["free"])
    price = client.get_avg_price(symbol = coin)
    price_of_coin = float(price['price'])
    Quantity = free/price_of_coin

    minQty = qty_ticker_info(coin)
    
    return format_value(Quantity,minQty)

# Get all orders that related to the account (must be converted into an excel file )********
def get_all_oreders(coin):
    orders = client.get_all_orders(symbol=coin, limit=2)
    for one_order in orders:
        for i in one_order:
            print(i,":",one_order[i])
        print("##################################################")

# Make limit buy order
def make_limit_buy_order(coin,qty,lpb): # lpb : limit price to buy (type : str)
    order = client.order_limit_buy(
        symbol=str(coin),
            quantity=qty,
                price=str(lpb))
    
# Make limit sell order
def make_limit_sell_order(coin,qty,lps): # lps : limit price to sell (type : str)
    order = client.order_limit_sell(
        symbol=str(coin),
            quantity=qty,
                price=str(lps))

# Make market sell order
def make_market_buy_order(coin,qty):
    order = client.order_market_buy(
        symbol=coin,
                quantity=qty) 

# Make market sell order
def make_market_sell_order(coin,qty):
    order = client.order_market_sell(
        symbol=coin,
                quantity=qty)

# Make oco order(buy/sell)
def make_oco_order(coin,side,qty,stop,price):
    order = client.create_oco_order(
        symbol=str(coin),
        side=side,
        stopLimitTimeInForce=TIME_IN_FORCE_GTC,
        quantity=qty,
        stopPrice=str(stop),
        price=str(price))

# Check an order’s status. Either orderId or origClientOrderId must be sent.
def check_order_status(coin,id):
    order = client.get_order(
    symbol=str(coin),
    orderId=str(id))

# Cancel an active order. Either orderId or origClientOrderId must be sent.
def cancel_order(coin,id):
    result = client.cancel_order(
    symbol=str(coin),
    orderId=str(id))

# Get all open orders on a symbol.
def get_open_order(coin):
    orders = client.get_open_orders(symbol=coin)
    print(orders)


##############################################################################################################
#####################################################Test#####################################################
##############################################################################################################

# Go to excal file to user
def get_account_info():
    asset=[]
    free=[]
    locked=[]
    info = client.get_account()
    info=info["balances"]
    for one_asset in info:
        if float(one_asset["free"])>0:
            asset.append(one_asset["asset"])
            free.append(float(one_asset["free"]))
            locked.append(float(one_asset["locked"]))
           
    info={
         "asset":asset,
         "free":free,
         "locked":locked
    }

    df=pd.DataFrame(info)
    df.to_excel("Account_asset_info.xlsx",index=False)
        # Open Microsoft Excel
    excel = cle.Dispatch("Excel.Application")
    # path='C:\Users\omara\OneDrive\Desktop\BOT Binance\Account asset info.xlsx'
    # Read Excel File
    sheets = excel.Workbooks.Open(r"C:\Users\omara\OneDrive\Desktop\BOT Binance\Account_asset_info.xlsx")
    work_sheets = sheets.Worksheets[0]
    
    # Convert into PDF File
    work_sheets.ExportAsFixedFormat(0, r"C:\Users\omara\OneDrive\Desktop\BOT Binance\Account_asset_info.xlsx")
    sheets.Close()
    excel.Quit()
   


