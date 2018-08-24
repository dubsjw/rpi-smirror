"""
@author Jacob Dubs
@date 3-24-2018
@file smartmirror.py
@brief A better raspberry pi smart mirror.
"""

# PyQt5 Imports
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

# Other Imports
import sys
import requests
import json
import os


class smart_mirror(QObject):
    def __init__(self, parent=None):
        '''
            Initialize the smart mirror class to show the ui.
        '''
        QWidget.__init__(self, parent=parent)

        # Initialize some member vars.
        self._engine = QQmlApplicationEngine()

    def load_ui(self, path):
        self._engine.load(path)

    def setContextProperty(self, name, property):
        '''
        Method to set context object for use within qml.
        '''
        ctx = self._engine.rootContext()
        ctx.setContextProperty(name, property)

class weather_engine(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._temperatureF = 0
        self._tempCelcius = 0
        self._tempKelvin = 0
        self._iconUrl = ''
        self.timer = QTimer()

        # Setup the timer for updating the weather.
        self.timer.timeout.connect(self.updateWeather)
        self.timer.setInterval(60000)

        #Update the weather for the first time.
        self.updateWeather()

    # Setup signals for change notifications.
    temperature_changed = pyqtSignal()
    icon_url_changed = pyqtSignal()

    @pyqtProperty('QString', notify=temperature_changed)
    def temperature(self):
        return str(self.kelvin_to_fahrenheit(self._tempKelvin)) + '* F'

    @temperature.setter
    def temperature(self, temperature):
        if self._tempKelvin != temperature:
            self._tempKelvin = temperature
            self.temperature_changed.emit()

    @pyqtProperty('QString', notify=icon_url_changed)
    def iconUrl(self):
        return self._iconUrl

    @iconUrl.setter
    def iconUrl(self, iconUrl):
        if self._iconUrl != iconUrl:
            self._iconUrl = iconUrl

    def kelvin_to_fahrenheit(self, kelvin):
        return round((9/5 * (kelvin - 273) + 32), 1)

    def parse_icon_url(self, json):
        iconCode = json['weather'][0]['icon']
        self._iconUrl = 'http://openweathermap.org/img/w/' + iconCode + '.png'
        self.icon_url_changed.emit()

    def parse_temperature(self, json):
        self._tempKelvin = json['main']['temp']
        self.temperature_changed.emit()

    def updateWeather(self):
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4996248&appid=371e94d08311d3945725e693cdd483a4")
        if response.status_code is not 401:
            weatherData = response.json()
            self.parse_temperature(weatherData)
            self.parse_icon_url(weatherData)
            self.timer.start()

class timeengine(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def get_time(self):
        pass

    def update_time(self):
        pass

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        sm = smart_mirror() 

        # Create the widget engines
        weatherengine = weather_engine()

        sm.setContextProperty('weatherengine', weatherengine)

        sm.load_ui('smview.qml')
        app.exec()
    except Exception as e:
        print(e)
        sys.exit()
