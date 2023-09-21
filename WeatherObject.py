class WeatherObj:
    def __init__(self, time, wind, temperature, humidity, pressure, visibility, cloudCover):
        self.time = time
        self.wind = wind
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.visibility = visibility
        self.cloudCover = cloudCover
        
        
    def __str__(self):
        return self.time + '\n' + self.wind + '\n' + self.temperature + '\n' + self.humidity + '\n' + self.pressure + '\n' + self.visibility + '\n' + self.cloudCover + '\n'
        