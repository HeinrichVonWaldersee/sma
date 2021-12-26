# SMA Project

This code was written by the Python group consisting of 

Master Students: Heinrich von Waldersee (16-620-502), Antonios Chrysolouris (21-600-036)

Bachelor Students: Christian Salis (21-605-225), Jovin Müntener (19-619-196)

In case there are any issues with the GitHub, please access the source code on the google collab notebook under the following link:

https://colab.research.google.com/drive/1jSPL-K3OKY_9LIk7738NnYdFe2i96ISo?usp=sharing

.

.

***IMPORTANT DISCLAIMER:***

The interface of CodingXCamp website did not allow us all to sign up together, because some members of the group are MAster Students and some Members are Bachelor Students.

However, this was not mentioned to be an issue when we formed the groups at the group forming event. Furthermore, we tried to contact the Professor both by email and by Slack (as early as the 15th of December) and we never recieved an answer. Therefore, we have have formed two groups to hand this project (one group wiht the Bachelor Students, One Group with the Master Students) **All of the above have mentioned students have collaborated on this project!!!**

For more information please contact: heinrich.vonwaldersee@student.unisg.ch

### About

Goal of the program: Simulate a trading strategy for a given stock over a past timeframe to validate the strategies historical performance. The trading strategy followed is a Simple Moving Average strategy and the program returns the strategies performance based on a long an shorter Simple Moving Average. The program should return a chart for the stocks performance and the moving averages as well as detailed statistics and KPIs that give us insights into the performance of the strategy in a given timeframe for the given stock.

inputs: stock ticker (to search yahoo finance),
        start date (YYYY-MM-DD), 
        end date (YYYY-MM-DD), 
        short Simple Moving Average (in days),
        long Simple Moving Average (in days).
        
Sample inputs: Stock: GOOG, Start Date: 2018-01-01, End Date: 2021-12-01, Short SMA: 20, Long SMA: 50        
        
Outputs: Chart that visulaises Stock closing price in defined time period and the Long and short Simple Moving Averages,
         dictionary of performance statistics of the trading strategy, 
         dictionary of the trades the strategy performed.

The program was adapted from **Ryan Mardani**, who wrote the fundamentals of many of the functions that we use. However, his code was very rigid and was thus adapted by us to applicable to any stock over any timeframe and with any SMAs. We added validated inputs and structured the program into functions a put them into a main function to have the program be runnable. Finally we also added thorough comments and documentation and changed a few calculations and outputs to better address how we expect the code to function. 
The Documentation of Mardani’s code can be found on their blog here: 
https://towardsdatascience.com/data-science-in-finance-56a4d99279f7 
and on their GitHub here: https://github.com/mardani72/Finance_Moving_Ave_Strategy

In our group project, we tried to enhance an investment strategy, by tracking the historical performance over a given time period of a Simple Moving Average (SMA) Strategy. An SMA is calculated by averaging the closing stock prices of a chosen stock over a predetermined timeframe.
The SMA Strategy consists in calculating two separate SMAs: one with a shorter timeframe than the other, longer, timeframe. Thereafter, we compare the short SMA with the long one. If the short one is larger than the longer one, and we do not yet hold a position in this stock, then we may proceed to buying this stock. If, however, the long SMA is larger  than the shorter SMA, and we hold a position in this stock, then the strategy suggests selling the stock.
As described above, the SMA is a trend-following indicator, calculated as the arithmetic mean of a concrete set of values. In our case, it will be the arithmetic mean of the past closing prices of a stock of our choice. Our code asks the user to define the time horizon of both SMAs. For example, if we set the length of the short SMA to be 30 and the length of the long one to be 60, then the code will calculate the arithmetic mean of the last 30 and the last 60 closing prices of the stock. 

### Functions

**main()**: the main function receives calls the input function to receive that values it needs (Stock, start/end dates and short/long SMAs) and applies them to the other below defined functions to return a chart that tracks the performance as well as the two dictionaries “buy_sell” containing dates and prices at which positions would have been bought or sold and the dictionary “stats” that contains all the statistical analysis we can can get on the performance of this strategy. 

**input()**: we ask for the following inputs and validates if they can be used.
  _Stock_: a stock ticker that can be found in the yahoo finance database. If the stock ticker cannot be found the program raises a “NameError” and the user can try with a different ticker.
  _Start:_ the date at which we wish to start our analysis. This is validated if it has the proper format.
  _End_: the date at which we wish to end our analysis This is also validated if it has the proper format.
  _Short SMA_: the shorter moving average (in days), validated to be an integer.
 _Long SMA:_ the longer moving average (in days), validated to be an integer.
The input function also validates if the inputs are assigned to the correct variables. If the user by accident put the end date as the first date and viceversa, it automatically understands there was an error and automatically switches the two dates. If the SMAs are assigned wrongy (long SMA is shorter than Long SMA) then the function also recognizes this and assigns the higher value to “long SMA” and the smaller value to “short SMA”. 

**dataframe(stock, start, end)**: in order to get data we can analyze, we use the dataframe function.  The function has three parameters “stock”, “start”, “end”. “Stock” refers to the ticker of the stock we would like to analyze. “start” and “end” define the start and end period of the period we would like to analyze. The function then accesses yahoofinance to get the dataframe for the defined stock and assigns a dataframe containing relevant information to the variable df. The dataframe contains dates as an index and most importantly tracks the closing prices at a one day interval. The function returns the dataframe.

**sma(short_sma, long_sma, df)**: To calculate all the SMAs, across time, we created the “sma” function. The function takes three parameters: sma_short, sma_long and df. The first two are the number of days we want the short and long SMAs to cover. The latter is a dataframe that contains relevant information on the stock that we have gotten from yahoo finance. We make use of the “rolling” and the “mean” function from pandas, which calculate the mean of the past closing prices in a predefined time window. Then, we add the calculated SMAs as new columns to our data frame and name the columns “SMA_short” and “SMA_long. The function returns this new dataframe.

**analysis(df)**: The trend function yields two returns: buy_sell and stats. The function takes a dataframe “df” as an input and uses it to calculate For the actual buy or sell decision, we constructed the trend function yields the trend dictionary . We create the empty dictionary “buy_sell” to track the investment strategy. 

We use the variable “position” to see if we already have a position on the stock or not. Then we compare the short with the long SMA and we follow the strategy as mentioned in the beginning of the documentation. We run a for loop for every entry in the dataframe. Then we have a decision tree that follows the strategy: if SMA_short is larger than SMA_long, and we don’t have a position, we buy a position and add a “buy” statement to the “buy_sell”  dictionary. If SMA_long is larger or equal to SMA_short, and we hold a position, we issue a sell statement to the “buy_sell” dictionary. Finally, once the analysis is complete, and we happen to still hold a position we have to sell the final position. Every time we sell a position we track the “percent change” of the stock that corresponds to the sell price over the buy price minus one (and multiplied by 100 to get it in percent). The function returns a detailed review of the buy/sell decisions with the returned element “buy_sell”.
Then we want to perform some analysis over the given time period. To begin we open an empty dictionary “stats” to which we will attribute the statistics that we calculate. We calculate the following statistics:

  _Percent Changes_: is a list of the various percent differences of the sell prices over the buy prices. Every time we sell a position we track the difference to the previous buy price of the position that is either positive or negative and append it to the list.
  _Gains_: the total sum of positive percentage changes (gains) over the timeframe.
  
  _Losses_: the total sum of negative percentage changes (losses) over the period in timeframe.
  
  _Average Gain_: Average of all the percentual positive changes (gains) that occurred in the timeframe.
  
  _Average Loss_: Average of all the percentual negative changes (losses) that occurred in the timeframe.
  
  _Batting Average_: Returns how many of the overall trades were gains. This represents how accurate the strategy has been. 
  
  _Gain/Loss Ratio_: represents the ratio between the average Gain and the average Loss, leading us to understand the risk return ratio. 
  
  _Max Loss_: the maximum percentual loss
  
  _Max Gain_: the maximum percentual gain that occurred over the timeframe.
  
  _Number of Gains_: the amount of counted positive percentage changes (gains) over the timeframe.
  
  _Number of Losses_: the amount of counted negative percentage changes (losses) over the timeframe.
  
  _Total Returns_: percentage change overall, which is calculated by multiplying the initial percentual total return (1) by the percentage changes and then subtracting 1 to get the overall return over the timeframe.
  
  _Trades_: total amount of trades that have occurred when following this strategy. (where a buy and a sell is considered one overarching trade). 

**plot(df, short_sma, long_sma, stock)**: finally we plot the dataframe into a chart with the function plot. The function plot takes 4 parameters which are df, the dataframe, “short_sma”, the length of the short moving average, “long_sma” which is the length of the long moving average and “stock” which represents the ticker of the stock we want to research. Luckily the matplotlib finance library already has the tools we need to plot this chart and therefore we only need to fill out the mpf.plot function with the relevant details. Remember that blue is the short sma and pink is the long sma. The function returns the chart that we assigned to the matplotlib finance function that plotted the chart. 


 
 




