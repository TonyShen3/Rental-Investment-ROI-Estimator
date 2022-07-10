# Function that scrapes Airbnb, Realtor.com and NerdWallet.com
# Input: zip code
# Output: [avgInvestment, avgReturn, ROI]

import requests
from bs4 import BeautifulSoup
import math


def getMortgageRate():
    # Obtain latest mortgage rate from Nerdwallet.com
    url = "https://www.nerdwallet.com/mortgages/mortgage-rates/investment-property"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
                      "Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    c = r.content

    # Scrape NerdWallet for latest mortgage rate
    bs = BeautifulSoup(c, "html.parser")
    rate = bs.find("div", {"class": "_13J6Bq"}).text
    rate = rate.replace("%", "")
    return float(rate)


def getHousingPrice(zipcode, adults):
    bed = str(math.ceil(int(adults) / 2))
    url = "https://www.redfin.com/zipcode/" + zipcode + "/filter/min-beds=" + str(bed) + ",max-beds=" + str(bed)


    # Requests Realtor.com Webpage. Header is needed to bypass bot detection
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
                      "Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    c = r.content

    # Scrapes Realtor.com web page for housing prices
    bs = BeautifulSoup(c, "html.parser")
    allEntries = bs.find_all("span", {"class": "homecardV2Price", "data-rf-test-name": "homecard-price"})
    house_res = []
    keyword = "$"
    for entry in allEntries:
        txt = entry.text
        if keyword in txt:
            filtered = txt.replace("$", "")
            filtered = filtered.replace(",", "")
            house_res.append(int(filtered))
    if house_res:
        avgHousePrice = round(sum(house_res) / len(house_res), 2)
    else:
        avgHousePrice = None
    return avgHousePrice


def getAirbnbRates(location, adults):
    url = "https://airbnb.com/s/" + location + "/homes?"
    url += "&adults=" + str(adults)
    r = requests.get(url)
    c = r.content
    bs = BeautifulSoup(c, "html.parser")
    allEntries = bs.find_all("span", {"class": "a8jt5op dir dir-ltr"})
    res = []
    keyword = "per night"
    for entry in allEntries:
        txt = entry.text
        if keyword in txt:
            filtered = txt.replace("$", "")
            filtered = filtered.replace(" per night", "")
            filtered = filtered.replace(",", "")
            res.append(int(filtered))
    if res:
        avg_rental_price = round(sum(res) / len(res), 2)
    else:
        avg_rental_price = None
    return avg_rental_price
