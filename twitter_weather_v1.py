import sys, requests, json, tweepy

try:
    import Adafruit_DHT
except ImportError:
    print("You're probably not on Raspberry Pi! (or install the Adafruit_DHT module on it)")

# Tweepy auth section

# Twitter Authentication
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")

# Create Twitter API
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

try:
 w, t = Adafruit_DHT.read_retry(11, 4) #Setting up the DHT11 Sensor on Raspberry Pi
except NameError:
 data_inside = "No data from the inside"
else:
    data_inside = 'Temperature Inside ' + t + 'C\nHumidity Inside ' + w + '%'

api_key = "openweathermap_api_key"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = input("Enter your city name: ")
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
response = requests.get(complete_url)
x = response.json()
if x["cod"] != "404":
    y = x["main"]
    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidity = y["humidity"]
    z = x["weather"]
    weather_description = z[0]["description"] 
    data_outside = (' Temperature Outside ' + str(current_temperature) + ' C \n Air Pressure ' 
        + str(current_pressure) + ' hPa \n Humidity Outside ' + str(current_humidity) + ' %')
else:
    print('City not found')
    exit()

string_before_data = 'Data from city of ' + str.title(city_name) + ' : \n'

complete_data = string_before_data + data_outside + '\n\n' + data_inside
#Tweet data

api.update_status(complete_data)

print(complete_data)
