import os

import inquirer
import requests

if not os.path.isfile('calendar.ics'):
    questions = [
      inquirer.Text('calendar_url', message="Enter your calendar url")
    ]
    answers = inquirer.prompt(questions)

    # Download .ics calendar
    url = answers['calendar_url']
    r = requests.get(url)

    with open("calendar.ics", 'wb') as f:
        f.write(r.content)
    f.close()

    print("Calendar downloaded")

    print("Waiting for login...")