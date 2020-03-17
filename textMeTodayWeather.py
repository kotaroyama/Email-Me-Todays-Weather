import smtplib
import datetime
import urllib.request
import json

def getTodayWeather(cityName):

    # Find out if the city name contains space
    #   If it does, replace it with "%20" to be used in the URL
    if (" " in cityName):
        cityName = cityName.replace(" ", "%20")

    unit = 'imperial'

    response = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q={}&units={}&APPID={}".format(cityName, unit, 'a748d4cee36119dedfc8827a2c6cb125'))

    # Convert JSON data into a list
    weatherData = json.loads(response.read().decode('utf8'))

    # Print weather
    print('City:    ' + weatherData['name'])
    print('Weather: ' + weatherData['weather'][0]['main'])
    print('Temp:    ' + str(weatherData['main']['temp']))
    print('Wind:    ' + str(weatherData['wind']['speed']))

    return weatherData

def sendEmail(hostUsername, hostPassword, targetEmail, content):

    # Login to email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(hostUsername, hostPassword)

    # Send email
    try:
        server.sendmail(hostUsername, targetEmail, content)
        print('sent')
    except Exception as e:
        print(e)

def setTimer(hostUsername, hostPassword, targetEmail, content, targetNotifyTime, timeDiff):

    while True:

        # Get current time - hour, minute, second.
        currentTime = str(datetime.datetime.now())
        currentMinute = int(currentTime.split(":")[1])
        currentHour = int(currentTime.split(":")[0].split(" ")[1])

        # Adjust to target's timezone (24h)
        targetHour = (currentHour + timeDiff) % 24

        # When time comes
        if (targetHour == targetNotifyTime[0]) and (currentMinute == targetNotifyTime[1]):

            # Send email
            sendEmail(hostUsername, hostPassword, targetEmail, content)

            # Break out of the loop
            break

if __name__ == "__main__":

    # Host email account details
    hostUsername = "yourEmailAddress@gmail.com"
    hostPassword = "yourPassword"

    # Target time details
    targetNotifyTime = [0, 0]  # [hour, minute] in 24 hour clock
    timeDiff = 0   # In hours

    # Target email details
    targetEmail = "yourTargetEmailAddress"
    cityName = input("Enter the City: ")

    # Obtain weather info
    weatherData = getTodayWeather(cityName)

    print('City:    ' + weatherData['name'])
    print('Weather: ' + weatherData['weather'][0]['main'])
    print('Temp:    ' + str(weatherData['main']['temp']))
    print('Wind:    ' + str(weatherData['wind']['speed']))

    # Construct the message
    content = "\nCity: " + str(weatherData['name']) + "\nWeather: " + str(weatherData['weather'][0]['main']) + "\nTemp: " + str(weatherData['main']['temp']) + " F" + "\nWind: " + str(weatherData['wind']['speed']) + " miles"


    # Set timer
    setTimer(hostUsername, hostPassword, targetEmail, content, targetNotifyTime, timeDiff)
