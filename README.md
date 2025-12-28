# Weather App
An application that shows the current weather and the forecast of any place in the world

As soon as the app opens, the user is free to type in the name of any location on Earth and then click on the little magnifying glass on the right.

The app will pull the necessary data from the weather API and will properly display it within the window (temperature, weather condition, wind speed, air pressure, humidity, chance of rain, UV Index, moon phase etc.), along with a bit of advice for the user. The current weather condition will be printed, along with the forcast for the next 2 days, or 3 days if the key used belongs to a paid API plan (the key can be easily found and changed in the program's script if needed, residing inside the 'get_weather_info' method, within the text of the string variable 'url').

If an error occurs when the user attempts to fetch data, the error's name will be displayed along with a short explanation.

The background image will change based on the present weather condition.



I worked on this app to further practice using the PyQt5 module, along with the requests module to fetch data from an API, while also constructing a useful app with a nice design.
