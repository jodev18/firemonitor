
import Adafruit_DHT

#returns zero upon failure to get temp or humidity
#class to fetch data from the sensor.
class AdafruitDHT22:
	
	humidity = 0
	temp = 0	

	def __init__(self):
		self.humidity,self.temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
	
	def get_temp(self):
		
		if self.temp is not None:
			return self.temp
		else:
			return 0

	def get_humidity(self):
		
		if self.humidity is not None:
			return self.humidity
		else:
			return 0

	def retry(self):
		self.humidity,self.temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)