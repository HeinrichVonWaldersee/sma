!pip install yfinance
!pip install mplfinance
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf


def main():


  # First we call the function "inputs" which returns validated inputs for the 
  # stock ticker, start and end date and short and long moving average:

  stock, start, end, short_sma, long_sma =inputs()
  

  # Then we set up the dataframe (df) to be analysed 
  # with the defined function "dataframe":

  df = dataframe(stock, start, end) 


  # Then we add columns for the moving averages (ma) (short and long) 
  # to the dataframe with the defined function "sma":

  df_sma  = sma(short_sma, long_sma, df)  
  

  # with the defined function "analysis" we assign the dictionaries
  # that contain the dates and prices of trades to the variable "buy_sell"
  # and the statistics of the performance to "stats":

  buy_sell, stats = analysis(df_sma) 


  #Finally we plot the stocks closing price and the SMAs on a chart

  chart = plot(df, short_sma, long_sma, stock)
  return stats, buy_sell, chart


"""

below you find the functions main calls (for more info refer to the ReadMe)

input():allows the user to type in the ticker, dates and SMAs the program calls
        These are validated through while loops and try/except statements
        this function also prints statements that the user can read about the 
        validaton. It also checks if the correct later and earlier dates were 
        assigned in the right Date input and also makes sure that the longer and
        shorter SMAs were assigned to the correct SMA inputs

dataframe(stock, start, end): returns a dataframe of the stock with the ticker 
                              "stock" from dates "start" to "end" by accessing
                              yahoofinance data and pulling the dataframe 

sma(short_sma, long_sma, df): adds columns to the dataframe "df". The 1st column
                              added is "short_sma" the other is "long_sma"

analysis(df): takes a dataframe "df" that contains columns with closing prices 
              for a stock as well as the short and long SMAs and performs a
              simulated trading strategy and returns two dictionaries:
              buy_sell: which includes all the prices and dates at which the
                        strategy would have performed a trade.
              stats:    which includes all the data that can be used to analyse
                        how successful this trading strategy would have been
                        for the stock of this dataframe. Refer to the ReadMe
                        to understand exactly what these stats represent.

plot(df, short_sma, long_sma, stock): uses the library "mplfinance" to plot the 
              stock "stock" over a given amount of time of the dataframe "df"
              as well as plotting the two moving averages "short_sma" and 
              "long_sma". The function returns a plotted chart.


"""

def inputs():
  

  #####
  # First we get the ticker and validate if it can be used:
  #####


  while True:
    stock = input("Stock Ticker: ") #gets the stock ticker
    ticker = yf.Ticker(str(stock))
    info = None
    try:
      if (ticker.info['regularMarketPrice'] == None): #checks if the ticker is in the yahoo database
        raise NameError("This is not a valid Stock try again") #raises an error it cannot be found
      else:
        print("this Ticker is Valid") 
        break #breaks loop and goes on with the program if the ticker is valid
    except NameError:
      print("This Ticker is not valid. Try again") #loops over if ticker can't be found
      continue
  

  #####
  # Second we get the start date and validate the format:
  #####


  while True:
    start = input("Start Time (YYYY-MM-DD):") #asks for the start date
    format = "%Y-%m-%d" #this is the applied format
    try:
      dt.datetime.strptime(start, format) #tries to see if the date can be validated
      print("correct date format") 
      break #breaks loop if we have a valid date
    except ValueError: #if it cannot be validated the loop runs again
      print("wrong date or date format, try again with YYYY-MM-DD")
      continue

  while True:
    end = input("End Time (YYYY-MM-DD):") #asks for the end date
    format = "%Y-%m-%d" #this is the applied format
    try:
      dt.datetime.strptime(end, format) #tries to see if the date can be validated
      print("correct date format")
      break #breaks loop if we have a valid date
    except ValueError: #if it cannot be validated the loop runs again
      print("wrong date or date format, try again with YYYY-MM-DD")
      continue
  

  #####
  # Lastly we get the simple moving averages, validated as integers
  #####


  while True: 
    sma1 = input("Length of first Moving Average (in days):") 
    try:
      sma1 = int(sma1) #if it can be transformed into an INT it's valid
      print("Valid input.")
      break
    except ValueError: #if it cannot be turned into an INT the loop runs again
      print("wrong input. Please write number of days for short sma")
      continue

  while True: 
    sma2 = int(input("Length of Second Moving Average (in days):"))
    try:
      sma2 = int(sma2) #if it can be transformed into an INT it's valid
      print("Valid input.")
      break
    except ValueError: #if it can be transformed into an INT it's valid
      print("wrong input. Please write number of days for short sma")
      continue


  #####
  # Finally we make sure the dates are in the right order
  # and that the SMAs (short and long) are also in the order short and long
  #####

  #date check
  
  format = "%Y-%m-%d"

  #get the date times that correspond to "start" and "end"

  start_date=dt.datetime.strptime(start, format)
  end_date=dt.datetime.strptime(end, format)


  if start_date>end_date: #do the dates need to be switched?

    #create copies to reference for the switch
    copy_start_str = start
    copy_end_str = end

    #perfrom the switch 
    end = copy_start_str
    start = copy_end_str 

  #SMA Check

  SMAs = [sma1, sma2] #a list of both the collected SMAs
  short_sma = min(SMAs) #assigns the shorter moving average to the "short_sma"
  long_sma = max(SMAs)  #assigns the longer moving average to "long_sma"

  return stock, start, end, short_sma, long_sma

def dataframe(stock, start, end):
  df = yf.download(stock,start, end, interval = '1d') #accesses a dataframe from yahoofinance for the given stock with a one day interval and assigns it to df
  return df

def sma(short_sma, long_sma, df):
  SMAs = [short_sma, long_sma]
  name = "short" ##makes sure that the first added column is called "SMA_short"
  for i in SMAs:
    df["SMA_"+name] = df.iloc[:,4].rolling(window = i).mean()  #calculates the rolling mean (sma) over the defined window
    name = "long" ##makes sure that the second added column is called "SMA_long"
  return df

def analysis(df):

  position = 0 # 1 means we have already entered poistion (bought), 0 means not already entered (not bought)
  counter  = 0 #keeps track how often we have run the for loop
  buy_sell   = {} ##empty dict that collects all the buy/sell prices with the date as a key
  percentChange = []   # empty list to collect percent changes 
  

  #####
  # First we run a for loop through the dataframe df:
  #####


  for i in df.index:

      #we define the variables we will use:

      SMA_short = df["SMA_short"]
      SMA_long = df["SMA_long"]
      close = df['Adj Close'][i]
    
      #depending on the difference between the two SMAs we perfrom one of the following

      if(SMA_short[i] > SMA_long[i]): #define uptrend when short_sma is larger than long_sma 
          if(position == 0): #if we don't hold a stock
            buyP = close   #buy price
            position = 1   # turn position
            buy_sell[str(i)] = ("Buy", str(buyP), str(i)) ##adds it to the trends dict
    
      elif(SMA_short[i] <= SMA_long[i]): #define downtrend (also serves as catchall for rare case of parity)
          if(position == 1):   # have a poistion in down trend
            position = 0     # selling position
            sellP = close    # sell price
            buy_sell[str(i)] = ("Sell",str(sellP), str(i)) ##adds it to the trends dict
            perc = (sellP/buyP-1)*100 #how much has the price changed
            percentChange.append(perc) #after a sale we add the percentage "perc" to the list of percent changes


      if(counter == df["Adj Close"].count()-1 and position == 1): #sells on the last close in case we still have an open position
          position = 0 #we have sold the position
          sellP = close #selling price
          buy_sell[str(i)] = ("Sell", str(sellP), str(i)) ##adds it to the trends dict
          perc = (sellP/buyP-1)*100 #how much has the price changed
          percentChange.append(perc) #after a sale we add the percentage "perc" to the list of percent changes
      counter += 1


  #####
  # From here lets calculate some stats on the asset and add them to the dict "stats" 
  # (these calculations are on the percent change of the intial return of 1 (100%))
  #####


  stats = {} # creates an empty dict where will put in all the relevant stats that this analysis brings)

  gains = 0 #corresponds to all the total gains in percent of the strategy
  numGains = 0 #absolute number of Gains overall (counted not summed)
  losses = 0 #corresponds to all the total losses in percent of the strategy
  numLosses = 0 #absolute number of Losses overall (counted not summed) 

  totReturn = 1 #to begin with our totalReturn is 100%

  for i in percentChange: #if i is positive its a gain otherwise its a loss
      if(i>0):
          gains += i
          numGains += 1
      else:
          losses += i
          numLosses += 1

      #we add the loss or gain to "totReturn"    

      totReturn = totReturn*((i/100)+1)


  #we calculate the return of the strategy by subtracting 
  #the intial position of 1 (rounded to two decimals):


  totReturn = round((totReturn-1)*100,2)


  #we can now calculate how many trades the strategy would have followed:


  numTrades = numGains + numLosses
  

  # Then we can estimate what the gains/losses were on average
  # and what the respective maximums were:


  if (numGains>0):
    avgGain = gains/numGains
    maxGain = str(max(percentChange))
  else:
    avgGain = 0
    maxGain = 'unknown'

  if(numLosses>0):
    avgLoss = losses/numLosses
    maxLoss = str(min(percentChange))


    #we can also calculate the riskreward ratio
    #but only if the denominator is not zero:


    ratioRR = str(-avgGain/avgLoss)  # risk-reward ratio
  else:
    avgLoss = 0
    maxLoss = 'unknown'
    ratioRR = 'inf'
  

  # Finally we calculate the batting average which is how often the strategy 
  # "did well" ie how often the many of the total trades were gains 
  # (0-1 scala 1 is great, 0 is bad)

  if(numGains>0 or numLosses>0):
    
    batAvg = numGains/(numGains+numLosses)
  else:
    batAvg = 0


  ######
  #Finally we add all these calculated stats to the "stat" dictionary
  #(for more info on interpretation of the stats consult the ReadMe)
  ######


  stats["Percent Changes"] = percentChange
  stats["Trades"] = numTrades
  stats["Gains"] = gains
  stats["Number of Gains"] = numGains
  stats["Losses"] = losses
  stats["Number of Losses"] = numLosses
  stats["Total Return"] = totReturn
  stats["Average Gain"] = avgGain
  stats["Average Loss"] = avgLoss
  stats["Max Gain"] = maxGain 
  stats["Max Loss"] = maxLoss
  stats["Gain/Loss Ratio"] = ratioRR
  stats["Batting Average"] = batAvg

  return buy_sell, stats


def plot(df, short_sma, long_sma, stock):


  #####
  # The mplfinance library has a function "mpf.plot" that lets us easily 
  # plot the evolution over time of the dataframe of the stock as well as the 
  # SMAs. we assign the plotted chart to the variable "chart" and return it
  #####


  chart = mpf.plot(df, type = 'ohlc', figratio = (16,6), mav = (short_sma,long_sma), 
           volume = True, title = str(stock), style = 'default')
  
  return chart 


main()
