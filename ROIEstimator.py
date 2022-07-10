# Airbnb Rental Investment Calculator

# Required libraries
import requests
from bs4 import BeautifulSoup
import math

# Requires input from user
class inputs:
    def __init__(self):
        self.location = ""
        while len(self.location) not in range(3, 6):
            self.location = input("(Required) Input location of interest (5 digit zip code only):  ")
        self.adults = input("(Optional) Input number of adults:  ")
        self.kids = input("(Optional) Input number of kids:  ")
        self.checkin = input("(Optional) Input beginning date of the date range in interest (ex. 2022-06-22):  ")
        self.checkout = input("(Optional) Input end date of the date range in interest (ex. 2022-06-24):  ")


userInputs = inputs()

# Generate Airbnb url based on user inputs
url = "https://airbnb.com/s/" + userInputs.location + "/homes?"
if userInputs.adults: url += "&adults=" + userInputs.adults
if userInputs.kids: url += "&children=" + userInputs.kids
if userInputs.checkin: url += "&checkin=" + userInputs.checkin
if userInputs.checkout: url += "&checkout=" + userInputs.checkout
print("Generated url: " + url)

# Requests Airbnb web page
r = requests.get(url)
c = r.content
print(c)

# Scrapes Airbnb web page for pricing data
bs = BeautifulSoup(c, "html.parser")
all = bs.find_all("span", {"class": "a8jt5op dir dir-ltr"})
res = []
keyword = "per night"
for entry in all:
    txt = entry.text
    if keyword in txt:
        filtered = txt.replace("$", "")
        filtered = filtered.replace(" per night", "")
        res.append(int(filtered))
print("The prices per night for houses at " + userInputs.location + " are:")
print(res)
avg_rental_price = round(sum(res) / len(res), 2)
print("The average price is $" + str(avg_rental_price) + " per night")

# Generate Realtor.com url based on user inputs
url = "https://www.realtor.com/realestateandhomes-search/" + userInputs.location
if userInputs.adults:
    bed = str(math.ceil(int(userInputs.adults) / 2))
    url += "/beds-" + bed + "-" + bed
print(url)

# Requests Realtor.com Webpage. Header is needed to bypass bot detection
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
                  "Safari/537.36 "
}
r = requests.get(url, headers=headers)
c = r.content
if c:
    print("load successfully")
    print(c)
else:
    print("didn't load")
# Scrapes Realtor.com web page for housing prices
bs = BeautifulSoup(c, "html.parser")
all = bs.find_all("span", {"class": "rui__x3geed-0 kitA-dS", "data-label": "pc-price"})
house_res = []
keyword = "$"
for entry in all:
    txt = entry.text
    if keyword in txt:
        filtered = txt.replace("$", "")
        filtered = filtered.replace(",", "")
        house_res.append(int(filtered))
print("The housing prices at " + userInputs.location + " are:")
print(house_res)
avgHousePrice = round(sum(house_res) / len(house_res), 2)
print("The average housing price is $" + str(avgHousePrice))

# Requests Nerdwallet.com for latest mortgage rate
url = "https://www.nerdwallet.com/mortgages/mortgage-rates/investment-property"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                  "Safari/537.36 "
}
r = requests.get(url, headers=headers)
c = r.content

# Scrape NerdWallet for latest mortgage rate
bs = BeautifulSoup(c, "html.parser")
rate = bs.find("div", {"class": "_13J6Bq"}).text
rate = rate.replace("%", "")
print("The current 30-years fixed mortgage rate is: " + rate + "%")
downPayment = avgHousePrice // 5

# Calculates minimum down payment and monthly payment
print("Consider a 20% down-payment of $" + str(downPayment))
loan = avgHousePrice - downPayment
r = float(rate) / 12 / 100
a = (1 + r) ** 360 - 1
b = r * (1 + r) ** 360
P = round(float(loan / a * b), 2)
print("Your monthly payment would be: $" + str(P))

# Calculates cash flow
cashFlow = round(P - avg_rental_price * 15, 2)
print("Your monthly cash flow assuming 50% occupancy rate, with no other expenses considered, is: $" + str(cashFlow))
ROI = round(cashFlow * 12 / downPayment * 100, 2)
print("Your cash on cash ROI is " + str(ROI) + "%")
