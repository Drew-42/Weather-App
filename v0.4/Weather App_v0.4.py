import sys
import os
from pathlib import Path
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLineEdit, QMainWindow)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt

files_path = Path('C:/Users/rodok/Desktop/program_files')

class Weather_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather App')
        self.setWindowIcon(QIcon('program_files/icon.png'))
        self.setMinimumWidth(900)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowMaximizeButtonHint)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setObjectName('background_widget')

        self.line_edit = QLineEdit(self)
        self.button = QPushButton('🔍', self)
        self.button.setFixedSize(50, 50)
        self.result1 = QLabel(self)
        self.result2 = QLabel(self)
        self.result3 = QLabel(self)
        self.result4 = QLabel(self)
        self.result5 = QLabel(self)
        self.result6 = QLabel(self)
        self.result7 = QLabel(self)
        self.result8 = QLabel(self)
        self.result9 = QLabel(self)
        self.result10 = QLabel(self)
        self.result11 = QLabel(self)
        self.result12 = QLabel(self)

        self.pixmap = QPixmap()
        self.grey = 0

        self.button.clicked.connect(self.on_button_clicked)

        self.initUI()
        self.applyStyles()

    def initUI(self):
        main_vbox = self.central_widget.layout()
        if main_vbox is None:
            main_vbox = QVBoxLayout(self.central_widget)

        self.delete_layout(main_vbox) 
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.line_edit)
        hbox1.addWidget(self.button)

        main_vbox.addLayout(hbox1)
        main_vbox.addWidget(self.result1)
        main_vbox.addWidget(self.result2)

        main_vbox.addSpacing(50)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.result3)
        hbox2.addWidget(self.result4)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.result5)
        hbox3.addWidget(self.result6)

        main_vbox.addLayout(hbox2)
        main_vbox.addLayout(hbox3)
        main_vbox.addWidget(self.result7)

        main_vbox.addSpacing(50)

        main_vbox.addStretch(1)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.result8)
        hbox4.addWidget(self.result9)
        hbox4.addWidget(self.result10)
        hbox4.addWidget(self.result11)
        hbox4.addWidget(self.result12)

        main_vbox.addLayout(hbox4)

        main_vbox.setSpacing(5)

        self.line_edit.setPlaceholderText('Enter location to get weather')

    def applyStyles(self):
        self.central_widget.setStyleSheet("""
            #background_widget {
                background-image: url(program_files/backgrounds/forest.png);
            }
        """)

        self.setStyleSheet("""
            QLineEdit{
                font-size: 30px;
                color: white;
                border-radius: 10px;
                padding: 12px;
                background-color: rgba(60, 40, 60, 120);
            }
            QPushButton{
                font-size: 35px;
                background-color: transparent;
            }
            QPushButton:hover{
                font-size: 38px;
            }
            QPushButton:pressed{
                font-size: 30px;
            }
            QLabel{
                font-size: 20px;
                padding: 4px;
                color: white;
            }
        """)
        
        self.result1.setAlignment(Qt.AlignCenter)
        self.result1.setStyleSheet('font-family: arial; font-weight: bold;')

        self.result2.setAlignment(Qt.AlignCenter)
        self.result2.setStyleSheet('font-size: 15px;')

        font_id = QFontDatabase.addApplicationFont('program_files/Heathergreen.otf')
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 150)
        self.result3.setFont(my_font)

        bg_style = 'background-color: rgba(60, 40, 60, 120);' if self.grey == 1 else 'background-color: transparent;'
        self.result3.setStyleSheet(f'font-size: 100px; border-radius: 10px; {bg_style}')
        
        self.result4.setAlignment(Qt.AlignCenter)
        
        self.result5.setStyleSheet(f'font-size: 20px; font-family: arial; font-weight: bold; border-radius: 10px; {bg_style}')
      
        self.result6.setAlignment(Qt.AlignCenter)
        self.result6.setStyleSheet('font-size: 15px; font-family: arial; font-weight: bold; border-radius: 10px;')
       
        self.result7.setStyleSheet('font-size: 15px;')

        self.result8.setStyleSheet(f'font-size: 20px; font-family: arial; font-weight: bold; border-radius: 10px;')
        
        self.result9.setAlignment(Qt.AlignCenter)
        self.result9.setStyleSheet(f'font-size: 20px; font-family: arial; font-weight: bold; border-radius: 10px; {bg_style}')
       
        self.result10.setAlignment(Qt.AlignCenter)
        self.result10.setStyleSheet(f'font-size: 20px; font-family: arial; font-weight: bold; border-radius: 10px; {bg_style}')
       
        self.result11.setAlignment(Qt.AlignCenter)
        self.result11.setStyleSheet(f'font-size: 20px; font-family: arial; font-weight: bold; border-radius: 10px; {bg_style}')

        self.result12.setAlignment(Qt.AlignCenter)
        self.result12.setStyleSheet(f'font-size: 20px; font-family: arial; font-weight: bold; border-radius: 10px; {bg_style}')

    def on_button_clicked(self):
        city_name = self.line_edit.text()
        if city_name:
            weather_info = self.get_weather_info(city_name)
            self.applyStyles()
            self.show_weather(city_name, weather_info)

    def get_weather_info(self, city_name):
        url = f'http://api.weatherapi.com/v1/forecast.json?key=d0a66f3e42844fed973212014252011&q={city_name}&days=4'
        response = requests.get(url)

        self.reset_labels()

        if response.status_code == 200:
            self.grey = 1
            weather_data = response.json()
            return weather_data
        else:
            self.grey = 0

            if response.status_code == 400:
                description = 'Invalid request/url or internal application error'
            elif response.status_code == 401:
                description = 'API key not provided/invalid'
            elif response.status_code == 403:
                description = 'API key has exceeded calls per month quota/has been disabled/API key can\'t access to resource'
            else:
                description = 'An unknown error occurred.'

            self.result2.setText('Error: Failed to retrieve data' + '\n' + 
                                f'HTTP Status Code: {response.status_code}' + '\n' + 
                                f'Description: {description}')
            return None

    def show_weather(self, text, weather_info):
        if weather_info:
            self.result1.setText(f'{weather_info['location']['name']}, {weather_info['location']['country']}')
            self.result2.setText(f'{weather_info['location']['localtime']}')
            
            self.get_set_image(weather_info)
            self.result4.setPixmap(self.pixmap.scaled(150, 150))
            
            self.result3.setText(f'{weather_info['current']['temp_c']}°C | {weather_info['current']['temp_f']}°F')

            self.result5.setText(f'Wind speed:        {weather_info['current']['wind_kph']} km/h | {weather_info['current']['wind_mph']} mi/h' + 
                                 '\n' + f'Air pressure:       {weather_info['current']['pressure_mb']} mbar | {weather_info['current']['pressure_in']} in Hg' + 
                                 '\n' + f'Precipitation:      {weather_info['current']['precip_mm']} mm | {weather_info['current']['precip_in']} inch' + 
                                 '\n' + f'Humidity:             {weather_info['current']['humidity']}%' + 
                                 '\n' + f'UV Index:             {weather_info['current']['uv']}')

            self.result6.setText('Weather condition:' + '\n' + f'{weather_info['current']['condition']['text']}' + '\n\n' + 
                                f'Moon phase: {weather_info['forecast']['forecastday'][0]['astro']['moon_phase']} {self.moon_phase(weather_info)}')
            
            self.result7.setText(f'Advice:{self.advice(weather_info)}')

            self.result8.setText('\n\n\n' + 'Med. temp. 🌡:' + '\n\n' + 'Min. temp. 🌡❄:' + '\n' + 'Max. temp. 🌡🔥:' + '\n\n' + 'Chance of rain ☂:')

            self.result9.setText(f'{weather_info['forecast']['forecastday'][0]['date']}' + '\n' + '(today)' + '\n\n' + 
                                f'{weather_info['forecast']['forecastday'][0]['day']['avgtemp_c']}°C | {weather_info['forecast']['forecastday'][0]['day']['avgtemp_f']}°F' + '\n\n' + 
                                f'{weather_info['forecast']['forecastday'][0]['day']['mintemp_c']}°C | {weather_info['forecast']['forecastday'][0]['day']['mintemp_f']}°F' + '\n' + 
                                f'{weather_info['forecast']['forecastday'][0]['day']['maxtemp_c']}°C | {weather_info['forecast']['forecastday'][0]['day']['maxtemp_f']}°F' + '\n\n' + 
                                f'{weather_info['forecast']['forecastday'][0]['day']['daily_chance_of_rain']}%')
           
            self.result10.setText(f'{weather_info['forecast']['forecastday'][1]['date']}' + '\n' + '(tomorrow)' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][1]['day']['avgtemp_c']}°C | {weather_info['forecast']['forecastday'][1]['day']['avgtemp_f']}°F' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][1]['day']['mintemp_c']}°C | {weather_info['forecast']['forecastday'][1]['day']['mintemp_f']}°F' + '\n' + 
                                  f'{weather_info['forecast']['forecastday'][1]['day']['maxtemp_c']}°C | {weather_info['forecast']['forecastday'][1]['day']['maxtemp_f']}°F' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][1]['day']['daily_chance_of_rain']}%')
         
            self.result11.setText(f'{weather_info['forecast']['forecastday'][2]['date']}' + '\n' + '(overmorrow)' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][2]['day']['avgtemp_c']}°C | {weather_info['forecast']['forecastday'][2]['day']['avgtemp_f']}°F' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][2]['day']['mintemp_c']}°C | {weather_info['forecast']['forecastday'][2]['day']['mintemp_f']}°F' + '\n' + 
                                  f'{weather_info['forecast']['forecastday'][2]['day']['maxtemp_c']}°C | {weather_info['forecast']['forecastday'][2]['day']['maxtemp_f']}°F' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][2]['day']['daily_chance_of_rain']}%')
            
            self.result12.setText(f'{weather_info['forecast']['forecastday'][3]['date']}' + '\n\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][3]['day']['avgtemp_c']}°C | {weather_info['forecast']['forecastday'][3]['day']['avgtemp_f']}°F' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][3]['day']['mintemp_c']}°C | {weather_info['forecast']['forecastday'][3]['day']['mintemp_f']}°F' + '\n' + 
                                  f'{weather_info['forecast']['forecastday'][3]['day']['maxtemp_c']}°C | {weather_info['forecast']['forecastday'][3]['day']['maxtemp_f']}°F' + '\n\n' + 
                                  f'{weather_info['forecast']['forecastday'][3]['day']['daily_chance_of_rain']}%')

            print(weather_info)

    def reset_labels(self):
        self.result1.clear()
        self.result2.clear()
        self.result3.clear()
        self.result4.clear()
        self.result5.clear()
        self.result6.clear()
        self.result7.clear()
        self.result8.clear()
        self.result9.clear()
        self.result10.clear()
        self.result11.clear()
        self.result12.clear()

    def get_set_image(self, weather_info):
        request_image = requests.get(f'https:{weather_info['current']['condition']['icon']}')
        self.pixmap.loadFromData(request_image.content)

    def background(self, weather_info):
        if weather_info:
            if weather_info['current']['is_day'] == 0: return 'bg_night.png'
            else: return 'bg_night.png'
        else: return 'intro.png'

    def advice(self, weather_info):
        message = ''
        if weather_info['current']['precip_mm'] > 0: message += '\n' + '* Take an umbrella!'
        if weather_info['current']['feelslike_c'] >= 35 and weather_info['current']['condition']['text'] == 'Sunny': message += '\n' + '* Avoid staying in the sun, use a hat for protection' + '\n' + '* Have water on you'
        if weather_info['current']['feelslike_c'] >= 22: message += '\n' + '* Dress lightly (shirt, short pants)'
        if weather_info['current']['feelslike_c'] > 29: message += ', or get naked'
        if 15 <= weather_info['current']['feelslike_c'] < 22: message += '\n' + '* Take a light jacket'
        if 6 <= weather_info['current']['feelslike_c'] < 15: message += '\n' + '* Take a jacket'
        if weather_info['current']['feelslike_c'] < 6: message += '\n' + '* Cover with winter coat, beanie, boots, scarf, gloves'
        if weather_info['current']['uv'] >= 3: message += '\n' + '* Use sunscreen'
        return message if message else ' none'

    def moon_phase(self, weather_info):
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'New Moon': return '🌑'
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'Waxing Crescent': return '🌒'
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'First Quarter': return '🌓'
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'Waxing Gibbous': return '🌔'
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'Full Moon': return '🌕'
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'Waning Gibbous': return '🌖'
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'Last Quarter': return '🌗'
        if weather_info['forecast']['forecastday'][0]['astro']['moon_phase'] == 'Waning Crescent': return '🌑'
        else: return 'unknown'

    def delete_layout(self, layout_to_clear):
        if layout_to_clear is not None:
            while layout_to_clear.count():
                item = layout_to_clear.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
                elif item.layout() is not None:
                    self.delete_layout(item.layout())
                del item

    def showEvent(self, event):
        super().showEvent(event)
        
        self.adjustSize()

        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())


def main():
    app = QApplication(sys.argv)
    weather_app = Weather_app()
    weather_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()