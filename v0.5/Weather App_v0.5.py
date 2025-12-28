import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QMainWindow)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize

# Defining the class of this app, that contains all the functions and preperties of the
# application:

class Weather_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather App')
        self.move(300, 100)
        self.setWindowIcon(QIcon('program_files/icon.png'))
        self.setMinimumWidth(900)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowMaximizeButtonHint)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setObjectName('background_widget')

        self.line_edit = QLineEdit(self)

        self.button = QPushButton(self)
        self.button.setFixedSize(50, 50)
        self.button.setIcon(QIcon('program_files/magnifying_glass.png'))
        self.button.setIconSize(QSize(35, 35))

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

        self.button.setMouseTracking(True)

        self.button.clicked.connect(self.on_button_clicked)

        self.initUI()

        bg_pic = 'bg_intro.png'

        self.applyStyles(bg_pic)

    def initUI(self):

# Defining the layout of the window:

        main_vbox = self.central_widget.layout()
        if main_vbox is None:
            main_vbox = QVBoxLayout(self.central_widget)
        
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

# Defining the appearence of the window's contents, based on search results:

    def applyStyles(self, bg_pic):
        self.central_widget.setStyleSheet(f"""
            #background_widget {{
                background-image: url(program_files/backgrounds/{bg_pic});
            }}
        """)

        self.setStyleSheet("""
            QLineEdit{
                font-size: 30px;
                color: white;
                border-radius: 10px;
                padding: 12px;
                background-color: rgba(50, 50, 50, 130);
            }
            QPushButton{
                background-color: transparent;
            }
            QLabel{
                font-size: 20px;
                padding: 4px;
                color: white;
            }
        """)
        
        self.button.enterEvent = self.button_enter
        self.button.leaveEvent = self.button_leave
        self.button.pressed.connect(self.button_pressed)
        self.button.released.connect(self.button_released)

        self.result1.setAlignment(Qt.AlignCenter)
        self.result1.setStyleSheet('font-family: arial; font-weight: bold;')

        self.result2.setAlignment(Qt.AlignCenter)
        self.result2.setStyleSheet('font-size: 15px;')

        font_id = QFontDatabase.addApplicationFont('program_files/Heathergreen.otf')
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 150)
        self.result3.setFont(my_font)

        bg_style = 'background-color: rgba(50, 50, 50, 130);' if self.grey == 1 else 'background-color: transparent;'
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

# The methods that describe what the program can do:

    def on_button_clicked(self):
        city_name = self.line_edit.text()
        if city_name:
            weather_info = self.get_weather_info(city_name)
            bg_pic = self.background(weather_info)
            self.applyStyles(bg_pic)
            self.show_weather(city_name, weather_info)

# This is the method that fetches data from the weather API. The key in 
# the url can be easily changed
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

# This method prints the weather data within the window's labels
    def show_weather(self, text, weather_info):
        if weather_info:
            self.result1.setText(f'{weather_info['location']['name']}, {weather_info['location']['country']}')
            self.result2.setText(f'{weather_info['location']['localtime']}')
            
            self.get_set_image(weather_info)
            self.result4.setPixmap(self.pixmap.scaled(150, 150))
            
            self.result3.setText(f'{weather_info['current']['temp_c']}°C | {weather_info['current']['temp_f']}°F')

            self.result5.setText(f'Wind speed:        {weather_info['current']['wind_kph']} km/h | {weather_info['current']['wind_mph']} mi/h' + 
                                 '\n' + f'Air pressure:       {weather_info['current']['pressure_mb']} mbar | {weather_info['current']['pressure_in']} in Hg' + 
                                 '\n' + f'Precipitation:       {weather_info['current']['precip_mm']} mm | {weather_info['current']['precip_in']} inch' + 
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
            
            try:              
                self.result12.setText(f'{weather_info['forecast']['forecastday'][3]['date']}' + '\n\n\n' + 
                                      f'{weather_info['forecast']['forecastday'][3]['day']['avgtemp_c']}°C | {weather_info['forecast']['forecastday'][3]['day']['avgtemp_f']}°F' + '\n\n' + 
                                      f'{weather_info['forecast']['forecastday'][3]['day']['mintemp_c']}°C | {weather_info['forecast']['forecastday'][3]['day']['mintemp_f']}°F' + '\n' + 
                                      f'{weather_info['forecast']['forecastday'][3]['day']['maxtemp_c']}°C | {weather_info['forecast']['forecastday'][3]['day']['maxtemp_f']}°F' + '\n\n' + 
                                      f'{weather_info['forecast']['forecastday'][3]['day']['daily_chance_of_rain']}%')
            except IndexError:
                self.result12.setText('Forecast data\nunavailable\n(API key - free plan)')
                

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

# This method showcases an image that represents the state of the weather
    def get_set_image(self, weather_info):
        request_image = requests.get(f'https:{weather_info['current']['condition']['icon']}')
        self.pixmap.loadFromData(request_image.content)

# This method establishes what background picture will be displayed based on the weather
# condition
    def background(self, weather_info):
        if weather_info:
            if weather_info['current']['condition']['text'] in ('Mist', 'Fog', 'Freezing fog'): return 'bg_fog.png'
            if weather_info['current']['condition']['text'] in ('Patchy rain nearby', 'Patchy rain possible', 'Patchy light drizzle', 'Light drizzle', 'Patchy light rain', 'Light rain', 'Moderate rain at times', 'Moderate rain', 'Heavy rain at times', 'Heavy rain', 'Light rain shower', 'Moderate or heavy rain shower', 'Torrential rain shower', 'Patchy freezing drizzle possible', 'Freezing drizzle', 'Heavy freezing drizzle', 'Light freezing rain', 'Moderate or heavy freezing rain'): return 'bg_rain.png'
            if weather_info['current']['condition']['text'] in ('Patchy snow possible', 'Blowing snow', 'Blizzard', 'Patchy light snow', 'Light snow', 'Patchy moderate snow', 'Moderate snow', 'Patchy heavy snow', 'Heavy snow', 'Light snow showers', 'Moderate or heavy snow showers'): return 'bg_snowy.png'
            if weather_info['current']['condition']['text'] in ('Patchy sleet possible', 'Light sleet', 'Moderate or heavy sleet', 'Ice pellets', 'Light sleet showers', 'Moderate or heavy sleet showers', 'Light showers of ice pellets', 'Moderate or heavy showers of ice pellets', ''): return 'bg_sleet.png'
            if weather_info['current']['condition']['text'] in ('Thundery outbreaks possible', 'Patchy light rain with thunder', 'Moderate or heavy rain with thunder', 'Patchy light snow with thunder', 'Moderate or heavy snow with thunder'): return 'bg_thunder.png'

            if weather_info['current']['is_day'] == 0:
                if weather_info['current']['feelslike_c'] >= 35:
                    if weather_info['current']['condition']['text'] in ('Clear', 'Partly Cloudy', 'Partly cloudy'): return 'bg_canyon_night.png'
                    if weather_info['current']['condition']['text'] in ('Cloudy', 'Overcast'): return 'bg_red_night.png'
                if 5 <= weather_info['current']['feelslike_c'] < 35:
                    if weather_info['current']['condition']['text'] in ('Clear', 'Partly Cloudy', 'Partly cloudy'): return 'bg_night.png'
                    if weather_info['current']['condition']['text'] in ('Cloudy', 'Overcast'): return 'bg_cloudy_night.png'
                if -30 < weather_info['current']['feelslike_c'] < 5:
                    if weather_info['current']['condition']['text'] in ('Clear', 'Partly Cloudy', 'Partly cloudy'): return 'bg_snowy_clear.png'
                    if weather_info['current']['condition']['text'] in ('Cloudy', 'Overcast'): return 'bg_cold_town.png'
                if weather_info['current']['feelslike_c'] <= -30: return 'bg_arctic.png'

            if weather_info['current']['is_day'] == 1:
                if weather_info['current']['feelslike_c'] >= 35:
                    if weather_info['current']['condition']['text'] in ('Clear', 'Sunny', 'Partly Cloudy', 'Partly cloudy'): return 'bg_hot_clear.png'
                    if weather_info['current']['condition']['text'] in ('Cloudy', 'Overcast'): return 'bg_rainforest.png'
                if 5 <= weather_info['current']['feelslike_c'] < 35:
                    if weather_info['current']['condition']['text'] in ('Clear', 'Sunny', 'Partly Cloudy', 'Partly cloudy'): return 'bg_deciduousforest.png'
                    if weather_info['current']['condition']['text'] in ('Cloudy', 'Overcast'): return 'bg_cloudy.png'
                if -30 < weather_info['current']['feelslike_c'] < 5:
                    if weather_info['current']['condition']['text'] in ('Clear', 'Sunny', 'Partly Cloudy', 'Partly cloudy'): return 'bg_village.png'
                    if weather_info['current']['condition']['text'] in ('Cloudy', 'Overcast'): return 'bg_sphinx.png'
                if weather_info['current']['feelslike_c'] <= -30: return 'bg_antarctica.png'

        else: return 'bg_error.png'

# This method establishes which advice to be displayed based on the weather condition
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

# This method establishes which moon phase to be displayed
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

    def showEvent(self, event):
        super().showEvent(event)
        
        self.adjustSize()

        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())

    def button_enter(self, event):
        self.button.setIconSize(QSize(40, 40))

    def button_leave(self, event):
        self.button.setIconSize(QSize(35, 35))

    def button_pressed(self):
        self.button.setIconSize(QSize(28, 28))

    def button_released(self):
        self.button.setIconSize(QSize(35, 35))


# The main code of the app:

def main():
    app = QApplication(sys.argv)
    weather_app = Weather_app()
    weather_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
