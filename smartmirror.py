"""
@author Jacob Dubs
@date 3-24-2018
@file smartmirror.py
@brief A better raspberry pi smart mirror.
"""

# PyQt5 Imports
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

# Python Imports
import sys
import requests
import json

class SmartMirror(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # Initialize some member vars.
        self._engine = QQmlApplicationEngine()
        
        # Start the main ui.
        self._engine.load('smview.qml')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_c:
            print('Key Press: ' + event.key())
            self.close()

class Weather(QObject):
    iconUrlChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize some member vars.
        self._tempCelcius = 0
        self._iconUrl = 'test'
        self.updateWeather()

    @pyqtProperty(float)
    def tempFahrenheit(self):
        return self._tempCelcius

    @pyqtProperty('QString', notify=iconUrlChanged)
    def iconUrl(self):
        return self._iconUrl

    @iconUrl.setter
    def iconUrl(self, url):
        self._iconUrl = url


    def updateWeather(self):
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4996248&appid=371e94d08311d3945725e693cdd483a4")
        
        if response.status_code is not 401:
            weatherData = response.json()
            self._tempCelcius = weatherData['main']['temp']
            iconCode = weatherData['weather'][0]['icon']
            self._iconUrl = 'http://openweathermap.org/img/w/' + iconCode + '.png'
            
            self.iconUrlChanged.emit()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        qmlRegisterType(Weather, 'Weather', 1, 0, 'Weather')
        sm = SmartMirror() 
        app.exec()
    except Exception as e:
        print(e)
        sys.exit()
