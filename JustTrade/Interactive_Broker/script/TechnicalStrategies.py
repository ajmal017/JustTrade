from strategy import Strategy
from event import SignalEvent
import json
import ast
from watson_developer_cloud import AlchemyLanguageV1,AlchemyDataNewsV1
import numpy as np
import random

class RSI(Strategy):
    """
    Relative Strength Index strategy 
    """

    def __init__(self, bars, events):
        """
        Initialises the strategy,
        Params:
        bars: The DataHandler object that provides bar information
        events: The Event Queue object
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events

        # Initialize the holding status to False
        self.bought = self._calculate_initial_bought()


    def _calculate_initial_bought(self):
        """
        Set the holding status to False for all symbols
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] =  False
        return bought

 
    def calculate_signals(self, event, periods=12):
        """
        params:
        event: 
        periods: parameter of RSI, number of periods 
        """
        if event.type == "MARKET":
            for s in self.symbol_list:
                bars = self.bars.get_latest_bars(s, periods+1)
                # Wait until at least "periods"+1 time periods market data is available
                if len(bars) == periods+1:
                    # Calculate RSI
                    close_price = [x[5] for x in bars] # close price for "periods"+1 periods
                    close_price_diff = [close_price[i] - close_price[i-1] for i in range(1, periods+1)]
                    ups_ = [x for x in close_price_diff if x > 0]
                    drops_ = [x for x in close_price_diff if x < 0]
                    ups_total = sum(ups_)
                    drops_total = sum(drops_)

                    if drops_total == 0 and ups_total == 0: # close prices for the last "periods" + 1 periods
                                                            # haven't changed at all. Do not send signal, wait
                        RSI = 50 
                    elif drops_total == 0 and ups_total != 0:
                        RSI = 100
                    else:
                        RS = ups_total / drops_total
                        RSI = 100 * RS/(1+RS) # This is the RSI

                    # Calculate the direction and strenght of the signal
                    if RSI >= 70 and RSI < 80:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'SHORT', "weak")
                    elif RSI >= 80 and RSI < 90:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'SHORT', "mild")
                    elif RSI >= 90:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'SHORT', "strong")
                    elif RSI <= 30 and RSI > 20:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'LONG', "weak")
                    elif RSI <= 20 and RSI > 10:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'LONG', "mild")
                    elif RSI <= 10:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'LONG', "strong")

                    # Only when RSI is less than or equal to 30, or greater than or equal to
                    # 70, a trading signal will be triggered
                    if RSI <= 30 or RSI >= 70:
                        self.events.put(signal)

class Market_Information_Prediction(Strategy):

    def __init__(self, bars, events):
        """
        Initialises the strategy,
        Params:
        bars: The DataHandler object that provides bar information
        events: The Event Queue object
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events

        # Initialize the holding status to False
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        """
        Set the holding status to False for all symbols
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] =  False
        return bought

    
    def searchNews(self,text):
        #4e9a752f7bc8c85ee8a88f441b7ddb24db2c39c0 #a4fee8f87cfbfe973fa8cfd3454e91d6f5cd8e8c #63af3e40799acb3b2819f59130b03db239a8767a #16bc58b14b5ee52a14d817475173f347333f5a0e #4e1cb9a6ee6aa63df294081a617e4badcc9b5d33
        alchemy_data_news = AlchemyDataNewsV1(api_key='4e1cb9a6ee6aa63df294081a617e4badcc9b5d33')
        '''
        results = alchemy_data_news.get_news_documents(start='now-1h', end='now', time_slice='1h')
        print(json.dumps(results, indent=2))
        '''
        results = alchemy_data_news.get_news_documents(
            start='1453334400',
            end='1455444500',
            max_results=10,
            return_fields=['enriched.url.title',
                           'enriched.url.url',
                           'enriched.url.author',
                           'enriched.url.publicationDate'],
            query_fields={'q.enriched.url.enrichedTitle.entities.entity': '|text={},type=company|'.format(text)})
        #print(json.dumps(results))
        temp=json.dumps(results)
        _dict=ast.literal_eval(temp)
        
        res=_dict['result']['docs']
        print(res)
        print("sdfsdfsdfs")
        infolist=[]
        for i in range(0,len(res)):
            info={}
            link=res[i]['source']['enriched']['url']['url']
            title=res[i]['source']['enriched']['url']['title']
            info['title']=title
            info['url']=link
            infolist.append(info)
        print(infolist)
        print('AlchemyData finish')
        return infolist

    def emotion(self,url):

        alchemy_language = AlchemyLanguageV1(api_key='4e1cb9a6ee6aa63df294081a617e4badcc9b5d33')
        temp=json.dumps(alchemy_language.emotion(url=url))
        #print(temp)
        #print(type(temp))
        dict=ast.literal_eval(temp)
       #print(dict)
        #print(type(dict))
        emotion=dict['docEmotions']
        #print(emotion)
        #print(type(emotion))
        positive=float(emotion['joy'])
        print(positive)
        negative=float(emotion['anger'])+float(emotion['fear'])+float(emotion['disgust'])+float(emotion['sadness'])
        print(negative)
        if positive > negative:
            return 1
        else:
            return 0


    def AlchemyAnalysis(self,text):
            infolist=self.searchNews("Google")

            urllist=[]
            for i in range(0,len(infolist)):
                url=infolist[i]['url']
                #print(url)
                urllist.append(url)
            posnum = 0 # the number of the positive website
            totalnum = len(urllist)
            print('total number of websites:',totalnum)
            
            # for j in range(0,totalnum):
            #     posnum += self.emotion(urllist[j])
            #     print('Loop:',j)
            #     #time.sleep(4000)
            # percent=posnum/totalnum
            # print(percent)
            percent = random.random()
            if percent > 0.9:
                return infolist,['LONG',"strong"]
            elif percent > 0.8:
                return infolist,['LONG',"mild"]
            elif percent > 0.7:
                return infolist,['LONG',"weak"]
            elif percent < 0.1:
                return infolist,['SHORT',"strong"]
            elif percent < 0.2:
                return infolist,['SHORT',"mild"]
            elif percent < 0.3:
                return infolist,['SHORT',"weak"]
            else:
                return infolist,None 

    def calculate_signals(self,event):
        if event.type == "MARKET":
            return 1


class Mean_Reversion(Strategy):
    """
    Mean Reversion is a very common class of strategies in trading. 
    It assumes that the price of a stock tends to converge to its 
    historical average.  
    Currently, we implement a simple mean reversion trading strategy,
    called Bollinger Band. In practice, a lot of constrains are added
    to Bollinger Band to construct accurate signals.
    """

    def __init__(self, bars, events):
        """
        Initialises the strategy,
        Params:
        bars: The DataHandler object that provides bar information
        events: The Event Queue object
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events

        # Initialize the holding status to False
        self.bought = self._calculate_initial_bought()


    def _calculate_initial_bought(self):
        """
        Set the holding status to False for all symbols
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] =  False
        return bought

 
    def calculate_signals(self, event, periods=20, width=2):
        """
        params:
        event: 
        periods: parameter of Bollinger Band, number of periods, 
                 usually use "day" as the unit of period
        width: width of band
        Very few constrains is added to Bollinger Band for now
        """
        if event.type == "MARKET":
            for s in self.symbol_list:
                bars = self.bars.get_latest_bars(s, periods)
                # Wait until at least "periods" time periods market data is available
                if len(bars) == periods:
                    close_price = [x[5] for x in bars] # close price for "periods" periods 

                    # Currently, the three bands are scalers. In the future, we will modify 
                    # the code to extend them to vectors, for purpose of accurate signals
                    mid_band = np.mean(close_price) # middle band
                    std = np.std(close_price)
                    upper_band = mid_band + width*std # upper band
                    lower_band = mid_band - width*std # lower band

                    curr_price = close_price[-1] # current price

                    if curr_price > upper_band:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'SHORT', "strong")
                        self.events.put(signal)
                        return {'name':bars[0][0],'time':bars[0][1], 'type':'SHORT', 'strength':"strong"}
                    elif curr_price < lower_band:
                        signal = SignalEvent(bars[0][0], bars[0][1], 'LONG', "strong")
                        self.events.put(signal)
                        return {'name':bars[0][0],'time':bars[0][1], 'type':'LONG', 'strength':"strong"}