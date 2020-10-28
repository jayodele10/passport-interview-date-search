#!/opt/anaconda3/envs/appointment/bin/python

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import chromedriver_binary
import random
import requests
import json
from push import pushbullet_message

# configure the options to be passed to the WebDriver initializer.
options = webdriver.ChromeOptions()
options.add_argument("headless")  # start chrome in headless mode
options.add_argument("window-size=1200x600")  # set the window size

driver = webdriver.Chrome(chrome_options=options)

url = "https://embassyberlin.appointment.ng/book/appointment"


def init():
    driver.get(url)
    time.sleep(random.random())
    select = Select(driver.find_element_by_id("member"))
    select.select_by_visible_text("1 Person")
    time.sleep(random.random())
    next_button = driver.find_element_by_xpath(
        "/html/body/section/div/div/div[2]/div/form/div[2]/div/div/div/button"
    )
    next_button.click()


def get_all_titles():
    show_table = driver.find_element_by_id("app_date")
    show_table.click()
    time.sleep(random.random())
    all_month_titles = []

    for i in range(4):
        next_table = driver.find_element_by_xpath(
            "/html/body/div[4]/div[1]/table/thead/tr[1]/th[3]"
        )
        month_titles = get_titles()
        all_month_titles.extend(month_titles)
        if next_table.is_displayed():
            next_table.click()
        else:
            pass

    return all_month_titles


def get_titles():
    titles_list = []
    i = 1
    while i < 7:
        cal_row = driver.find_element_by_xpath(
            f"/html/body/div[4]/div[1]/table/tbody/tr[{i}]"
        )
        titles = [
            str(td.get_attribute("title"))
            for td in cal_row.find_elements_by_tag_name("td")[1:-2]
        ]
        titles_list.extend(titles)
        i += 1

    return titles_list


def any_slot(titles):
    for title in titles:
        try:
            if title not in ["Booked Out", "Holiday", "Off Day"]:
                return True
        except Exception as e:
            print(e)
            print(title)
    return False


def loop():
    init()
    slots = get_all_titles()
    if any_slot(slots):
        pushbullet_message("Appointment slot", "There is currently an available slot!")
    else:
        pushbullet_message("Appointment slot", "No currently available slot.")


if __name__ == "__main__":
    loop()
