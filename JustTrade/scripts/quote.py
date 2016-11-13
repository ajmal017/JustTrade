import urllib
import time
import json
import datetime


class Quote(object):
	DATE_FMT = '%Y-%m-%d'
	TIME_FMT = '%H:%M:%S'

	def __init__(self):
		self.symbol = ''
		self.date, self.time, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(7))

	def append(self, dt, open_, high, low, close, volume):
		self.date.append(dt.date())
		self.time.append(dt.time())
		self.open_.append(float(open_))
		self.high.append(float(high))
		self.low.append(float(low))
		self.close.append(float(close))
		self.volume.append(int(volume))

	def to_json(self):
		json_return = []

		json_return.append(["'symbol':{0}, 'date':{1}, 'time':{2}, 'open':{3:.2f}, 'close':{4:.2f}, 'high':{5:.2f}, 'low':{6:.2f}, 'volume':{7}".format(self.symbol,
		                                                                           self.date[bar].strftime('%Y-%m-%d'),
		                                                                           self.time[bar].strftime('%H:%M:%S'),
		                                                                           self.open_[bar], self.close[bar],
		                                                                           self.low[bar], self.high[bar],
		                                                                           self.volume[bar])
		                for bar in xrange(len(self.close))])

		# json_return.append({'log_time': log.log_time.strftime("%Y-%m-%d %H:%M:%S"),
		#                     'trade_task': log.trade_task.pk,
		#                     'log_type': log.log_type,
		#                     'log_info': json.loads(log.log_info)})
		# for log in xrange(len(self.close))])

		json_return = json.dumps(json_return)
		return json_return

	def to_csv(self):
		return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
		                                                                           self.date[bar].strftime('%Y-%m-%d'),
		                                                                           self.time[bar].strftime('%H:%M:%S'),
		                                                                           self.open_[bar], self.high[bar],
		                                                                           self.low[bar], self.close[bar],
		                                                                           self.volume[bar])
		                for bar in xrange(len(self.close))])

	def write_csv(self, filename):
		with open(filename, 'w') as f:
			f.write(self.to_csv())

	def read_csv(self, filename):
		self.symbol = ''
		self.date, self.time, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(7))
		for line in open(filename, 'r'):
			symbol, ds, ts, open_, high, low, close, volume = line.rstrip().split(',')
			self.symbol = symbol
			dt = datetime.datetime.strptime(ds + ' ' + ts, self.DATE_FMT + ' ' + self.TIME_FMT)
			self.append(dt, open_, high, low, close, volume)
		return True

	def __repr__(self):
		return self.to_json()


class GoogleIntradayQuote(Quote):
	''' Intraday quotes from Google. Specify interval seconds and number of days '''

	def __init__(self, symbol, interval_seconds=300, num_days=5):
		super(GoogleIntradayQuote, self).__init__()
		self.symbol = symbol.upper()
		url_string = "http://www.google.com/finance/getprices?q={0}".format(self.symbol)
		url_string += "&i={0}&p={1}d&f=d,o,h,l,c,v".format(interval_seconds, num_days)
		csv = urllib.urlopen(url_string).readlines()
		for bar in xrange(7, len(csv)):
			if csv[bar].count(',') != 5:
				continue
			offset, close, high, low, open_, volume = csv[bar].split(',')
			if offset[0] == 'a':
				day = float(offset[1:])
				offset = 0
			else:
				offset = float(offset)
			open_, high, low, close = [float(x) for x in [open_, high, low, close]]
			dt = datetime.datetime.fromtimestamp(day + (interval_seconds * offset))
			self.append(dt, open_, high, low, close, volume)