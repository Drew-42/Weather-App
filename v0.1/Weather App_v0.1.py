import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
							 QVBoxLayout, QHBoxLayout, QLineEdit)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class Weather_app(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Weather App')
		self.setWindowIcon(QIcon('icon.png'))

		self.line_edit = QLineEdit(self)
		self.button = QPushButton('Get Weather', self)
		self.result1 = QLabel(self)
		self.result2 = QLabel(self)
		self.result3 = QLabel(self)
		self.result4 = QLabel(self)
		self.result5 = QLabel(self)
		self.pixmap = QPixmap()
		self.initUI()

	def initUI(self):
		vbox = QVBoxLayout()
		self.setLayout(vbox)

		hbox = QHBoxLayout()
		hbox.addWidget(self.line_edit)
		hbox.addWidget(self.button)

		vbox.addLayout(hbox)
		vbox.addWidget(self.result1)
		vbox.addWidget(self.result2)
		vbox.addWidget(self.result3)
		vbox.addWidget(self.result4)
		vbox.addWidget(self.result5)

		self.result1.setAlignment(Qt.AlignCenter)
		self.result2.setAlignment(Qt.AlignCenter)
		self.result3.setAlignment(Qt.AlignCenter)
		self.result4.setAlignment(Qt.AlignCenter)

		self.setStyleSheet("""
			QLineEdit, QLabel, QPushButton{
				font-family: calibri;
			}
			QLineEdit{
				font-size: 30px;
			}
			QPushButton{
				font-size: 22px;
				font-weight: bold;
				padding: 8px;
			}
			QLabel{
				font-size: 25px;
				padding: 10px;
			}
		""")

		self.result1.setStyleSheet('font-size: 18px; color: red;')
		self.result5.setStyleSheet('font-size: 25px; color: red;')

		self.line_edit.setPlaceholderText('Enter location')

		self.button.clicked.connect(self.get_weather_button)

	def get_weather_button(self):
		self.reset_labels()
		
		text = self.line_edit.text()
		self.show_weather(text)

	def get_weather_info(self, text):
		url = f'http://api.weatherapi.com/v1/current.json?key=d0a66f3e42844fed973212014252011&q={text}'
		response = requests.get(url)

		if response.status_code == 200:
			weather_data = response.json()
			return weather_data
		else:
			if response.status_code == 400:
				description = 'Invalid request/url or internal application error'
			if response.status_code == 401:
				description = 'API key not provided/invalid'
			if response.status_code == 403:
				description = 'API key has exceeded calls per month quota/has been disabled/API key can\'t access to resource'

			self.result1.setText('Error: Failed to retrieve data' + '\n' + 
				                f'HTTP Status Code: {response.status_code}' + '\n' + 
			                    f'Description: {description}')

	def show_weather(self, text):
		weather_info = self.get_weather_info(text)
		
		if weather_info:
			self.result2.setText(f'Location: {weather_info['location']['name']}, {weather_info['location']['country']}' 
				+ '\n' + f'Local time: {weather_info['location']['localtime']}')
			
			self.get_set_image(weather_info)
			self.result3.setPixmap(self.pixmap.scaled(100, 100))
			
			self.result4.setText(f'Temperature: {weather_info['current']['temp_c']}℃ | {weather_info['current']['temp_f']}℉' 
				+ '\n' + f'Weather condition: {weather_info['current']['condition']['text']}' 
				+ '\n' + f'Wind speed: {weather_info['current']['wind_kph']}km/h | {weather_info['current']['wind_mph']}mi/h')

			self.result5.setText('\n' + f'Advice:{self.advice(weather_info)}')
			
			print(weather_info)

	def reset_labels(self):
		self.result1.clear()
		self.result2.clear()
		self.result3.clear()
		self.result4.clear()
		self.result5.clear()

	def get_set_image(self, weather_info):
		request_image = requests.get(f'https:{weather_info['current']['condition']['icon']}')
		self.pixmap.loadFromData(request_image.content)

	def advice(self, weather_info):
		message = ''

		if weather_info['current']['precip_mm'] > 0:
			message += '\n' + '* Take an umbrella!'

		if weather_info['current']['feelslike_c'] >= 35 and weather_info['current']['condition']['text'] == 'Sunny':
			message += '\n' + '* Avoid staying in the sun, take a hat for protection' + '\n' + '* Have water on you'

		if weather_info['current']['feelslike_c'] >= 22:
			message += '\n' + '* Dress lightly (shirt, short pants)'
			if weather_info['current']['feelslike_c'] > 29:
				message += ', or get naked'

		if 15 <= weather_info['current']['feelslike_c'] < 22:
			message += '\n' + '* Take a light jacket'

		if 6 <= weather_info['current']['feelslike_c'] < 15:
			message += '\n' + '* Take a jacket'

		if weather_info['current']['feelslike_c'] < 6:
			message += '\n' + '* Cover with winter coat, beanie, scarf, gloves, boots'

		if weather_info['current']['uv'] >= 3:
			message += '\n' + '* Use sunscreen'

		if message == '':
			return ' none'
		else:
			return message

def main():
	app = QApplication(sys.argv)
	weather_app = Weather_app()
	weather_app.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()