# import Selenium and create a driver object
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import platform

# create an edge driver object
print(platform.system())
# identify the OS type
if platform.system() == 'Windows':
    #TODO: add the path to the driver
    # edge_driver = webdriver.Edge(#path to driver)
    pass
elif platform.system() == 'Darwin' or platform.system() == 'Linux':
    edge_driver = webdriver.Edge()
# elif platform.system() == 'Linux':
#     from selenium.webdriver.chrome.service import Service
#     from selenium.webdriver.chrome.options import Options

#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('disable-gpu')
#     service = Service(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
#     edge_driver = webdriver.Chrome(service=service)


# navigate to the website
edge_driver.get('https://en.allmetsat.com/metar-taf/europe.php?icao=LROP')


# While true loop and get data at 12:00 and 20:00

import time

while True:
    if time.localtime().tm_hour == 12 or time.localtime().tm_hour == 20:
        # refresh the page
        edge_driver.refresh()
        ##############################################################################################################
        # get the METAR data


        # get the weather data
        time = edge_driver.find_element(By.XPATH , "//*[contains(text(), 'The report was made')]")
        print(time.text, ': ')
        wind = edge_driver.find_element(By.XPATH , "//*[contains(text(), 'Wind')]")
        print(wind.text)
        temp = edge_driver.find_element(By.XPATH , "//*[contains(text(), 'Temperature')]")
        print(temp.text)
        hum = edge_driver.find_element(By.XPATH , "//*[contains(text(), 'Humidity')]")
        print(hum.text)
        press = edge_driver.find_element(By.XPATH , "//*[contains(text(), 'Pressure')]")
        print(press.text)
        vis = edge_driver.find_element(By.XPATH , "//*[contains(text(), 'Visibility')]")
        print(vis.text)
        cloud = edge_driver.find_element(By.XPATH , "//*[contains(text(), 'cloud') or contains(text(), 'Cloud')]")
        print(cloud.text)



        ##############################################################################################################




        # Create an weahter object
        from WeatherObject import WeatherObj
        weather = WeatherObj(time = time.text, wind = wind.text, temperature = temp.text, humidity = hum.text, pressure = press.text, visibility = vis.text, cloudCover = cloud.text)

        # print the weather object
        # print(weather)


        ##############################################################################################################


        # upload the data to the database
        import sqlite3
        # create a connection to the database
        conn = sqlite3.connect('WeatherDB.sqlite')

        # Create the table if it doesn't exist
        conn.execute('''CREATE TABLE IF NOT EXISTS WEATHER
                    (TIME TEXT PRIMARY KEY NOT NULL,
                    WIND TEXT NOT NULL,
                    TEMPERATURE TEXT NOT NULL,
                    HUMIDITY TEXT NOT NULL,
                    PRESSURE TEXT NOT NULL,
                    VISIBILITY TEXT NOT NULL,
                    CLOUDCOVER TEXT NOT NULL);''')

        # insert the data into the table
        conn.execute('''INSERT INTO WEATHER (TIME, WIND, TEMPERATURE, HUMIDITY, PRESSURE, VISIBILITY, CLOUDCOVER)
                    VALUES (?, ?, ?, ?, ?, ?, ?);''', (weather.time, weather.wind, weather.temperature, weather.humidity, weather.pressure, weather.visibility, weather.cloudCover))

        # commit the changes
        conn.commit()

        # close the connection
        conn.close()

        #################################################################################################################
    else:
        # wait for the amount of time until the next hour
        print('The time is: ', time.localtime().tm_hour, ':', time.localtime().tm_min , ':', time.localtime().tm_sec)
        print('Waiting until ' , time.localtime().tm_hour + 1, '...')
        time.sleep(3600 - (time.localtime().tm_min * 60 + time.localtime().tm_sec))