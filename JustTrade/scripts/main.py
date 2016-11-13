# coding: utf-8

import time, Queue

from Interactive_Broker.script import event, data
from Interactive_Broker.script import strategy, TechnicalStrategies
from Interactive_Broker.script import portfolio, PortfolioWithSimpleRM
from Interactive_Broker.script import execution, ibexecution
from tasks.models import tradeLog
from tasks.models import tradingTask
import json


def Execute(pk,realtimeindex=True,NPL =False, waiting_time = 0.1,symbol_list=["SPY"], strategy='Mean_Reversion'):
	task = tradingTask.objects.get(pk=pk)

	if realtimeindex:
		mode = "Realtime"
	else:
		if not NPL:
			mode = "Backtesting"
		elif NPL:
			mode = "NPL"

	if mode == "Realtime":

		# Must Run this while the market is not closed otherwise there will be a 0/0 problem, trying to fix this
		##-------------Initialization-------------------------------------------
		# Declare the components with respective parameters
		events = Queue.Queue()

		# You need to change this to your directory
		# symbol_list = ["SPY"]
		# (self, events, csv_dir, symbol_list)
		bars = data.RealTimeDataHandler(events, symbol_list)

		# TODO get strategy

		strategy = TechnicalStrategies.Mean_Reversion(bars, events)  # (self, bars, events)

		# (self, bars, events, start_date, initial_capital=100000.0)
		port = PortfolioWithSimpleRM.SimplePortfolio(bars, events, "12-5-2014", 10000000)

		# broker = execution.SimulatedExecutionHandler(events)
		broker = ibexecution.IBExecutionHandler(events)

		##--------------Start RealTime-----------------------------------------
		while True:
			# Update the bars (specific backtest code, as opposed to live trading)
			bars.update_bars()

			# Handle the events
			while True:
				try:
					event = events.get(False)
				except Queue.Empty:
					break
				else:
					if event is not None:
						if event.type == 'MARKET':
							info = strategy.calculate_signals(event)

							log = tradeLog.objects.create(trade_task=task)
							log.log_type = 'Market Event'
							if info:
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"stay put"})
							log.save()

							info = port.update_timeindex(event)

							log = tradeLog.objects.create(trade_task=task)
							log.log_type = 'Portfolio Update'
							if info:
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"no portfolio change"})	
							log.save()

						elif event.type == 'SIGNAL':
							info = port.update_signal(event)

							log = tradeLog.objects.create(trade_task=task)
							log.log_type = 'Portfolio Event'
							if info:
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"no order has placed"})
							log.save()

						elif event.type == 'ORDER':
							broker.execute_order(event)

							log = tradeLog.objects.create(trade_task=task)
							log.log_type = 'Order Event'
							log.save()
							time.sleep(3) # just to make sure the order could be filled by the broker

						elif event.type == 'FILL':
							port.update_fill(event)

							log = tradeLog.objects.create(trade_task =task)
							log.log_type = 'Order Done'
							log.save()

							# 0.1-Second heartbeat, accelerate backtesting
				time.sleep(10)

	# performace evaluation
		port.create_equity_curve_dataframe()
		performace_stats = port.output_summary_stats()
		print performace_stats

	elif mode =="NPL":
		events = Queue.Queue()

		# You need to change this to your directory
		# symbol_list = ["SPY"]
		# (self, events, csv_dir, symbol_list)
		bars = data.RealTimeDataHandler(events, symbol_list)
		strategy = TechnicalStrategies.Market_Information_Prediction(bars,events)
		urls,result = strategy.AlchemyAnalysis(symbol_list[0])
		return urls,result

	elif mode == "Backtesting":
		##-------------Initialization-------------------------------------------
		# Declare the components with respective parameters
		events = Queue.Queue()

		# You need to change this to your directory
		rootpath = "~/Documents/automatedTrading/JustTrade/Interactive_Broker/"
		symbol_list = ["chart"]
		# (self, events, csv_dir, symbol_list)
		bars = data.HistoricCSVDataHandler(events, rootpath, symbol_list)

		strategy = TechnicalStrategies.Mean_Reversion(bars, events) #(self, bars, events)

		# (self, bars, events, start_date, initial_capital=100000.0)
		port = PortfolioWithSimpleRM.SimplePortfolio(bars, events, "12-5-2014", 10000000)

		broker = execution.SimulatedExecutionHandler(events)

			##--------------Start backtesting-----------------------------------------
		while True:
			# Update the bars (specific backtest code, as opposed to live trading)
			if bars.continue_backtest == True:
				bars.update_bars()
			else:
				break

			while True:
				try:
					event = events.get(False)
				except Queue.Empty:
					break
				else:
					if event is not None:
						if event.type == 'MARKET':
							info = strategy.calculate_signals(event)
							log = tradeLog.objects.create(trade_task=task)
							log.log_type = 'Market Event'
							print info
							
							if info:
								info['time'] = 0
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"stay put"})
							log.save()

							info = port.update_timeindex(event)


							log = tradeLog.objects.create(trade_task=task)
							time.sleep(waiting_time)

							log.log_type = 'Portfolio Update'
							if info:
								info['time'] = 0
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"no portfolio change"})	
							log.save()
							time.sleep(waiting_time)
						elif event.type == 'SIGNAL':
							time.sleep(waiting_time)
							info = port.update_signal(event)

							log = tradeLog.objects.create(trade_task=task)
							log.log_type = 'Portfolio Event'
							if info:
								info['time'] = 0
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"no order has placed"})
							log.save()
						elif event.type == 'ORDER':
							time.sleep(waiting_time)
							info = broker.execute_order(event)

							log = tradeLog.objects.create(trade_task=task)
							log.log_type = 'Order Event'
							if info:
								info['time'] = 0
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"Just Ordered"})
							log.save()
							time.sleep(waiting_time) # just to make sure the order could be filled by the broker
						elif event.type == 'FILL':
							time.sleep(waiting_time)
							info = port.update_fill(event)

							log = tradeLog.objects.create(trade_task =task)
							if info:
								info['time'] = 0
								log.log_info = json.dumps(info)
							else:
								log.log_info = json.dumps({"info":"Just finished order"})
							log.log_type = 'Order Done'
							log.save()

	# 0.1-Second heartbeat, accelerate backtesting
	                #time.sleep(0.1)
	        time.sleep(waiting_time)

	# performace evaluation
	port.create_equity_curve_dataframe()
	performace_stats = port.output_summary_stats()
	print performace_stats
	return port.equity_curve

	



def run(pk):
	Execute(pk,realtimeindex = False,NPL = True)
