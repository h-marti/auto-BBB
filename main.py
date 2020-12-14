# ScriptName : main.py
# ---------------------
import os
import time

from datetime import datetime

import pytz
from decouple import config
from icalendar import Calendar
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

teachers = {
    "HARDY": "https://visio.intech-sud.fr/b/mar-wxx-xqn-2cp",
    "MALACRINO": "https://visio.intech-sud.fr/b/mar-wxx-xqn-2cp",
    "CAMBET PETIT JEAN": "https://visio.intech-sud.fr/b/car-t6h-80a-zro",
    "CERLO": "https://visio.intech-sud.fr/b/rem-mue-mix-2v7",
    "MONTANARO": "https://visio.intech-sud.fr/b/mag-8pu-vyd-2ts",
    "MALARD": "https://visio.intech-sud.fr/b/jul-m2n-vxs-ulx",
    "POIROT": "https://visio.intech-sud.fr/b/mat-ubw-pye-zyl",
    "CANINI": "https://visio.intech-sud.fr/b/rac-tdl-cnq-bhm"
}


def set_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def get_room_url(teacher):
    switcher = teachers
    return switcher.get(teacher, "Invalid teacher ")


def connect_to_bbb(teacher_name=None):
    chrome_options = set_chrome_options()
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Firefox()

    username = config('USERNAME')
    password = config('PASSWORD')

    signinUrl = "https://visio.intech-sud.fr/b/signin"
    roomUrl = "https://visio.intech-sud.fr/b/rooms"

    xpaths = {'emailTxtBox': "//input[@name='loginfmt']",
              'passwordTxtBox': "//input[@name='passwd']",
              'nextButton': "//input[@id='idSIButton9' and @value='Next']",
              'signinButton': "//input[@id='idSIButton9' and @value='Sign in']",
              'yesButton': "//input[@id='idSIButton9' and @value='Yes']",
              'roomTxtBox': "//input[@id='join_room_url']",
              'goToRoomButton': "//input[@name='commit']",
              'joinButton': "//button[@id='room-join']",
              'listenButton': "//i[@class='icon--2q1XXw icon-bbb-listen']"
              }

    while browser.current_url != roomUrl:

        browser.get(signinUrl)

        try:
            print("Trying to sign in...")

            # Clear Username TextBox if already allowed "Remember Me"
            browser.find_element_by_xpath(xpaths['emailTxtBox']).clear()

            # Write Email in TextBox
            browser.find_element_by_xpath(xpaths['emailTxtBox']).send_keys(username)

            # Click Next button
            browser.find_element_by_xpath(xpaths['nextButton']).click()

            # Clear Password TextBox if already allowed "Remember Me"
            browser.find_element_by_xpath(xpaths['passwordTxtBox']).clear()

            # Write Password in password TextBox
            browser.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)

            time.sleep(2)

            # Click SignIn button
            browser.find_element_by_xpath(xpaths['signinButton']).click()

            browser.find_element_by_xpath(xpaths['yesButton']).click()

        except:
            time.sleep(1)

    print("Signed in !")

    print("Trying to connect into " + teacher_name + " room...")

    # Write selected URL in Room URL TextBox
    browser.find_element_by_xpath(xpaths['roomTxtBox']).clear()
    browser.find_element_by_xpath(xpaths['roomTxtBox']).send_keys(get_room_url(teacher_name))

    # Go to the room
    browser.find_element_by_xpath(xpaths['goToRoomButton']).click()

    # Join the room
    browser.find_element_by_xpath(xpaths['joinButton']).click()

    print("Joining the session...")

    time.sleep(3)

    # If room is joined, connect to the audio
    if str(browser.current_url)[28:39] == 'html5client':
        try:
            browser.find_element_by_xpath(xpaths['listenButton']).click()
            print("Room successfully joined !")
        except:
            print("Session has not started yet...")

    time.sleep(900)


def run():
    current_teacher = None
    today = datetime.now(pytz.utc)
    # today = datetime(2020, 12, 14, 13, 25, 30)
    todayDay = str(today)[0:10]
    todayHour = str(today)[11:13]

    # Read calendar
    g = open('calendar.ics', 'rb')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            start = component.decoded('dtstart')
            startDay = str(start)[0:10]
            startHour = str(start)[11:13]
            end = component.decoded('dtend')
            endHour = str(end)[11:13]
            summary = str(component.decoded('summary'))
            if startDay == todayDay:
                if (int(startHour) - 1) <= int(todayHour) <= int(endHour):
                    for teacher in teachers:
                        if summary.__contains__(teacher):
                            current_teacher = teacher
                    if current_teacher is not None:
                        connect_to_bbb(current_teacher)
                    else:
                        connect_to_bbb('CANINI')
    g.close()


if __name__ == '__main__':
    run()
