import os

import inquirer
import requests

if not os.path.isfile('calendar.ics'):
#    questions = [
#      inquirer.Text('calendar_url', message="Enter your calendar url")
#    ]
#    answers = inquirer.prompt(questions)

    # Download .ics calendar
#    url = answers['calendar_url']
    url = "https://intechsud.hyperplanning.fr/hp/Telechargements/ical/Edt_NICOLAS.ics?version=2020.0.5.0&idICal=7188615FECA9AC9AA6A55CC6876C8CF8&param=643d5b312e2e36325d2666683d3126663d31"
    r = requests.get(url)

    with open("calendar.ics", 'wb') as f:
        f.write(r.content)
    f.close()

    print("Calendar downloaded")