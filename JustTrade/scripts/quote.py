import urllib2
import time
import json
import datetime

class Quote(object):
	def __init__(self, symbol, interval_seconds=300, num_days=5):
		self.date, self.time, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(7))
		self.symbol = symbol.upper()
		url_string = "http://www.google.com/finance/getprices?q={0}".format(self.symbol)
		url_string += "&i={0}&p={1}d&f=d,o,h,l,c,v".format(interval_seconds, num_days)
		csv = urllib2.urlopen(url_string).readlines()
		for bar in xrange(7, len(csv)):
			if csv[bar].count(',') != 5: continue
			offset, close, high, low, open_, volume = csv[bar].split(',')
			if offset[0] == 'a':
				day = float(offset[1:])
				offset = 0
			else:
				offset = float(offset)
			open_, high, low, close = [float(x) for x in [open_, high, low, close]]
			dt = datetime.datetime.fromtimestamp(day + (interval_seconds * offset))
			self.append(dt, open_, high, low, close, volume)

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
		#  how i calculate the index:
		# (time - (9*3600+30*60))/ (16*3600 - (9*3600/+30*60)) * 27
		# 27*(time-34200)/23400
		for bar in xrange(len(self.close)):
			(h, m, s) = self.time[bar].strftime('%H:%M:%S').split(':')
			index = 27.0 * ((int(h) * 3600 + int(m) * 60 + int(s))- 34200.0) / 23400.0
			json_return.append(
					[
					 round(index,2),
					# 'symbol': self.symbol,
					#  'date': self.date[bar].strftime('%Y-%m-%d'),
					#  'time': self.time[bar].strftime('%H:%M:%S'),
					#  'open': self.open_[bar],
					 self.close[bar]
					 # 'volume': self.volume[bar],
					 ])
		json_return = json.dumps(json_return)
		return json_return
