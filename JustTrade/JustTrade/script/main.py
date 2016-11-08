# coding: utf-8

import time, Queue

from Interactive_Broker.script import event, data
from Interactive_Broker.script import strategy, TechnicalStrategies
from Interactive_Broker.script import portfolio, PortfolioWithSimpleRM
from Interactive_Broker.script import execution, ibexecution

from tasks.models import tradingTask, tradeLog


def Execute(realtimeindex=True, symbol_list=["SPY"], strategy='Mean_Reversion', pk=1):

	task = tradingTask.objects.filter(pk=pk)
	log = tradeLog(trade_task=task)

	if realtimeindex:
		mode = "Realtime"

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
							strategy.calculate_signals(event)
							print "Market Event"
							port.update_timeindex(event)
							print "Portfolio Update"

						elif event.type == 'SIGNAL':
							port.update_signal(event)
							print "Portfolio Event"

						elif event.type == 'ORDER':
							broker.execute_order(event)
							print "Order Event"
						# time.sleep(3) # just to make sure the order could be filled by the broker

						elif event.type == 'FILL':
							port.update_fill(event)
							print "Order Done"

							# 0.1-Second heartbeat, accelerate backtesting
		time.sleep(60)

		# performace evaluation
		port.create_equity_curve_dataframe()
		performace_stats = port.output_summary_stats()
		print performace_stats
