# Scraping data for all US zip codes and saving into a SQLite3 database

import sqlite3
import ScraperFunctions
import time
import MajorUSCities


def createDatabase(array):
    cur.execute("CREATE TABLE ROIdata (zip text, avgInvestment real, avgReturn real, ROI real)")

def insertEntry(zipCode):
    con.execute("INSERT INTO ROIdata VALUES (?, NULL, NULL, NULL)", (zipCode,))

def updateEntry(zipcode, avgInvestment, avgReturn, ROI):
    con.execute("UPDATE ROIdata "
                "SET avgInvestment = ?, avgReturn = ?, ROI =? "
                "WHERE zip = ?", (avgInvestment, avgReturn, ROI, zipcode))

def printDatabase():
    cur.execute("SELECT * FROM ROIdata")
    print(cur.fetchall())

# Connect to database
con = sqlite3.connect('ROIdata.db')
cur = con.cursor()

# Load zip codes of interest
data = MajorUSCities.majorZipCodes

# # Create database
# createDatabase(data)

RecreateDatabase = input("Would you like to recreate the database? Selecting 'Y' will empty the current database (Y/N):")

if RecreateDatabase == "Y":
    con.execute("DELETE FROM ROIdata")
    print("Scraping data and recreating database")
    rate = ScraperFunctions.getMortgageRate()
    for zipcode in data:
        zipcode = str(zipcode)
        time.sleep(5)
        housePrice = ScraperFunctions.getHousingPrice(zipcode, 4)
        if not housePrice:
            print("Encountered error scraping housing price. This is likely due to website blocking bot scraping.")
            continue
        rates = ScraperFunctions.getAirbnbRates(zipcode, 4)
        if not rates:
            print("Encountered error scraping Airbnb rates. This is likely due to website blocking bot scraping")
            continue
        avgReturn = 365 * 0.5 * rates
        avgInvestment = 0.2 * housePrice
        ROI = avgReturn / housePrice
        con.execute("INSERT INTO ROIdata VALUES (?, NULL, NULL, NULL)", (zipcode,))
        con.execute("UPDATE ROIdata "
                    "SET avgInvestment = ?, avgReturn = ?, ROI =? "
                    "WHERE zip = ?", (avgInvestment, avgReturn, ROI, zipcode))
        print("Data scraped and added to database successfully")

else:
    print("Current database info")
    printDatabase()
# Close database
con.commit()
con.close()
