import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLineEdit, QMainWindow)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt

class Weather_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather App')
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedSize(900, 600)

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
        self.pixmap = QPixmap()
        self.grey = 0

        self.button.clicked.connect(self.on_button_clicked)

        self.initUI()
        self.applyStyles()

    def initUI(self):
        self.central_widget.setStyleSheet("""
            #background_widget {
                background-image: url(wallpaper.png);
            }
        """)

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

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.result3)
        hbox2.addWidget(self.result4)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.result5)
        hbox3.addWidget(self.result6)

        main_vbox.addLayout(hbox2)
        main_vbox.addLayout(hbox3)
        main_vbox.addWidget(self.result7)

        main_vbox.setSpacing(5)
        self.line_edit.setPlaceholderText('Enter location to get weather')

    def applyStyles(self):
        self.setStyleSheet("""
            QLineEdit{
                font-size: 30px;
                color: white;
                border-radius: 10px;
                padding: 12px;
                background-color: rgba(0, 0, 20, 100);
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

        font_id = QFontDatabase.addApplicationFont('Heathergreen.otf')
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 150)
        self.result3.setFont(my_font)

        bg_style = 'background-color: rgba(0, 0, 20, 100);' if self.grey == 1 else 'background-color: transparent;'
        self.result3.setStyleSheet(f'font-size: 100px; border-radius: 10px; {bg_style}')
        
        self.result4.setAlignment(Qt.AlignCenter)
        self.result4.setStyleSheet(f'background-color: transparent')
        
        self.result5.setStyleSheet(f'font-size: 20px; font-family: arial; font-weight: bold; border-radius: 10px; {bg_style}')
      
        self.result6.setAlignment(Qt.AlignCenter)
        self.result6.setStyleSheet('font-size: 15px; font-family: arial; font-weight: bold; background-color: transparent; border-radius: 10px;')
       
        self.result7.setStyleSheet('font-size: 15px;')


    def on_button_clicked(self):
        city_name = self.line_edit.text()
        if city_name:
            weather_info = self.get_weather_info(city_name)
            self.show_weather(city_name, weather_info)

    def get_weather_info(self, text):
        url = f'http://api.weatherapi.com/v1/current.json?key=d0a66f3e42844fed973212014252011&q={text}'
        response = requests.get(url)

        self.reset_labels()

        if response.status_code == 200:
            self.grey = 1
            self.applyStyles()
            weather_data = response.json()
            return weather_data
        else:
            self.grey = 0
            self.applyStyles()

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
            self.result2.setText(f'{weather_info['location']['localtime']}' + '\n\n')
            
            self.get_set_image(weather_info)
            self.result4.setPixmap(self.pixmap.scaled(200, 200))
            
            self.result3.setText(f'{weather_info['current']['temp_c']}°C | {weather_info['current']['temp_f']}°F')

            self.result5.setText(f'Wind speed:        {weather_info['current']['wind_kph']} km/h | {weather_info['current']['wind_mph']} mi/h' + 
                                 '\n' + f'Air pressure:       {weather_info['current']['pressure_mb']} mbar | {weather_info['current']['pressure_in']} in Hg' + 
                                 '\n' + f'Precipitation:      {weather_info['current']['precip_mm']} mm | {weather_info['current']['precip_in']} inch' + 
                                 '\n' + f'Humidity:             {weather_info['current']['humidity']}%' + 
                                 '\n' + f'UV Index:             {weather_info['current']['uv']}')

            self.result6.setText('Weather condition:' + '\n' + f'{weather_info['current']['condition']['text']}')
            self.result7.setText('\n' + f'Advice:{self.advice(weather_info)}')
            
            print(weather_info)

    def reset_labels(self):
        self.result1.clear()
        self.result2.clear()
        self.result3.clear()
        self.result4.clear()
        self.result5.clear()
        self.result6.clear()
        self.result7.clear()

    def get_set_image(self, weather_info):
        request_image = requests.get(f'https:{weather_info['current']['condition']['icon']}')
        self.pixmap.loadFromData(request_image.content)

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


    def delete_layout(self, layout_to_clear):
        if layout_to_clear is not None:
            while layout_to_clear.count():
                item = layout_to_clear.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
                elif item.layout() is not None:
                    self.delete_layout(item.layout())
                del item

def main():
    app = QApplication(sys.argv)
    weather_app = Weather_app()
    weather_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()