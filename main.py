"""
Creating application that can assist in various tasks:
    - Open and close application on system - Done/ only apps adding needed/
    - Get weather updates on any location that user asks /done/
    - Tell current date and time /done/
    - Give calendar reminders for upcoming events
    - Search anything on Google, Wikipedia, Youtube
        - Website
    - Multi-user

Some useful tools:
    -pyttsx3, speech recognition, Twilio


For now the features that need more work, but are their bases are done are:
- Open/Close apps: TODO - list of apps
- weather: TODO - more functionality
- reminders: TODO - delete reminders, migrate, scheduling
- database: TODO - create Firebase db
"""

import assistant

greeting_message = "HELLO, IM FEACMe (First Ever Assistant Created by ME), I'm glad to help you with what I can!"
commands_terminal = "You can use these commands from the terminal: \n" \
                    "   - Type \'listen\' for me to listen to your commands\n" \
                    "   - Type \'text\' to input commands as text\n" \
                    "   - After every command done, press any key(not the shutdown key, xd) for me to listen again\n" \
                    "   - If you want to change the input type, please enter \'change <input_type>\'\n" \
                    "   - If you want to shut me down, type \'x\' and press enter"

a = assistant.Assistant()  # initializing assistant


def startup_procedure():
    a.read(greeting_message)
    print(commands_terminal + '\n')


if __name__ == '__main__':
    startup_procedure()  # Startup procedure

    a.run()
