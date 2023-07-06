import speech_recognition as sr
from speech_recognition import AudioData
import os
import pyttsx3 as t2s
import socket
import requests as rq
import datetime
import rcalendar

'''
THIS IS THE APP DICTIONARY
'''

# app_dict =
month_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

name = 'FEACMe'
voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# A function that opens app that is in the dictionary
def _open_app(application):
    try:
        os.startfile(f'{application}.exe')  # Using the os library to start the program
    except Exception as e:
        print(f'Error: {e}')


# A function that closes app that is in the dictionary
def _close_app(application):
    try:
        os.system(f'taskkill /F /IM {application}.exe > ' + os.devnull + ' 2>&1')  # Using os to kill the process.
        # /F - forcefully close; /IM indicates that the name of the app will be next
        # 2>&1 Changing the default output from stderr to stdout and placing it in devnull(the black hole)
    except Exception as e:
        print(f'Error: {e}')


def _tell_time():
    time = datetime.datetime.now()

    return f'{time.hour}:{time.minute}'


def _tell_date():
    date = datetime.datetime.now()
    day = date.day
    month = date.month

    suffix = 'th'
    if day == 1:
        suffix = 'st'
    elif day == 2:
        suffix = 'nd'
    elif day == 3:
        suffix = 'rd'

    return f'{day}{suffix} of {month_dict[month]}'


def _process_date(data: str, processed_data='date'):
    # format = dd:mm:yyyy
    if processed_data == 'date':
        datas = data.split('.')
        day = int(datas[0])
        month = int(datas[1])
        year = int(datas[2])

        return datetime.date(year, month, day)
    # format = hh:mm
    elif processed_data == 'time':
        datas = data.split(':')
        hour = int(datas[0])
        minutes = int(datas[1])

        return datetime.time(hour, minutes)


class Assistant:
    def __init__(self):
        self.r = sr.Recognizer()  # Initializing recogniser
        self.name = name  # Setting the name
        self.engine = t2s.init()  # Initializing the text to speech engine
        self.engine.setProperty('rate', 150)  # Setting the rate of talk /150 words per minute/
        self.engine.setProperty('volume', 0.8)  # Setting the volume /80%/
        # self.engine.setProperty('voice', voice_id)  # Setting the voice with voiceID
        self.weather = Weather()  # Weather assistant init
        self.rcalendar = rcalendar.Calendar()

    # function that listens to the mic
    def listen_microphone(self):
        print('Listening: ')

        with sr.Microphone() as source:
            audio = self.r.listen(source)

        return audio

    # audio to text using google's speech to text
    def convert_audio_to_text(self, audio: AudioData):
        try:
            text = self.r.recognize_google(audio)
            return text
        except Exception as e:
            print(e)

    # processing the given command and executing
    def process_command(self, command: str):
        text = None

        if command == 'listen':
            audio = self.listen_microphone()
            text = self.convert_audio_to_text(audio)
        elif command == 'text':
            text = input('How can I help?: ')
        else:
            raise Exception('Invalid command')

        self._execute_command(text.lower())

    # executing command
    def _execute_command(self, command: str):
        command_words = command.split()

        if command.__contains__('open'):
            app_index = command_words.index('open') + 1
            _open_app(command_words[app_index])

            message = f'OK! Opening {command_words[app_index]}'
            self.read(message)
        elif command.__contains__('close'):
            app_index = command_words.index('close') + 1
            _close_app(command_words[app_index])

            message = f'OK! Closing {command_words[app_index]}'
            self.read(message)
        elif command.__contains__('porn'):
            self.read('pervert.')
        elif command.__contains__('repeat'):
            self.read('OK \n')

            start_index = command_words.index('repeat') + 1
            message = command_words[start_index:]
            self.read(' '.join(message))
        elif command.__contains__('weather'):
            if command.__contains__('now'):
                self.read(self.weather.get_current())
            else:
                self.read(self.weather.get_today())
        elif command.__contains__('time'):
            message = f'It\'s {_tell_time()}'
            self.read(message)
        elif command.__contains__('date') or command.__contains__('today'):
            message = f'It\'s the {_tell_date()}'
            self.read(message)
        elif command.__contains__('reminder'):
            if command.__contains__('new') or command.__contains__('create'):
                self.read('Fill the boxes manually to create a reminder')

                rtype = input('Input the type: ')
                title = input('Reminder title: ')
                description = input('Reminder description: ')
                date = _process_date(input('Set date /follow the format: (dd.mm.yyyy)/: '))
                is_time_needed = input('Is time needed(y/n): ')

                if is_time_needed == 'y':
                    time = _process_date(input('Set time /follow the format: (hh:mm)/: '), processed_data='time')
                    self.rcalendar.add_reminder(rtype, title, description, date, time)
                else:
                    self.rcalendar.add_reminder(rtype, title, description, date)
            elif command.__contains__('show'):
                self.read('Here are your upcoming reminders: ')
                self.rcalendar.check_reminders(3)
        else:
            self.read(f'{command} is either a wrong command or not available')

    # reading a message with the tts engine
    def read(self, message: str):
        self.engine.say(message)
        print(message)
        self.engine.runAndWait()

    # running the assistant
    def run(self):
        user_input = input('Waiting for input: ')
        default_input = user_input

        while True:
            self.process_command(default_input)
            user_input = input('Assistant waiting: ')

            if user_input == 'x':
                break
            elif user_input == 'change listen':
                default_input = 'listening'
            elif user_input == 'change text':
                default_input = 'text'


class Weather:
    def __init__(self):
        self.key = '1c302880548140eba8b63347232206'
        self.response = rq.get(
            f'http://api.weatherapi.com/v1/forecast.json?key={self.key}&q=auto:ip&days=7&aqi=no&alerts=yes')
        status_code = self.response.status_code
        self.status_code_ok = 200 <= status_code < 400

    def get_current(self) -> str:
        if self.status_code_ok:
            json = self.response.json()
            location = json['location']['name'] + ' ' + json['location']['country']
            degrees = json['current']['temp_c']
            condition = json['current']['condition']['text']

            message = f'Today in {location} is {degrees} degrees and {condition}'
            return message

    def get_today(self) -> str:
        if self.status_code_ok:
            forecast = self.response.json()['forecast']['forecastday']
            date = forecast[0]['date']
            max_temp = forecast[0]['day']['maxtemp_c']
            min_temp = forecast[0]['day']['mintemp_c']
            avg_temp = forecast[0]['day']['avgtemp_c']
            chance_of_rain = forecast[0]['day']['daily_chance_of_rain']
            max_wind = forecast[0]['day']['maxwind_kph']

            return f'{self.get_current()}\nToday, we expect the average temperature to be around ' \
                   f'{avg_temp} degrees Celsius\nThe highest temperature should reach {max_temp} degrees and the ' \
                   f'temperature should drop as low as {min_temp} degrees.\nToday, the chance of rain is ' \
                   f'{chance_of_rain}%, and the wind will average speeds of around {max_wind} kilometers per hour'

    def get_forecast(self):
        response = rq.get(f'http://api.weatherapi.com/v1/forecast.json?key={self.key}&q=auto:ip&days=7&aqi=no'
                          f'&alerts=yes')
        status_code_ok = 200 <= response.status_code < 400

        if status_code_ok:
            json = response.json()
