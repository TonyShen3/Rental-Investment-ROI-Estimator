import folium
import pgeocode
import sqlite3
import math

# Creates map tiles on center of U.S.
ROImap = folium.Map(location=[39.83, -98.58], zoom_start=5, tiles="OpenStreetMap")

# Connect to database and extract table
con = sqlite3.connect('ROIdata.db')
cur = con.cursor()
cur.execute("SELECT * FROM ROIdata")
data = cur.fetchall()
con.commit()
con.close()

# Extract lat and lon values for each zip code and add marker to map
nomi = pgeocode.Nominatim('us')
for entry in data:
    query = nomi.query_postal_code(entry[0])
    lat = query["latitude"]
    lon = query["longitude"]
    print(entry)
    avgInvestment = math.floor(entry[1])
    avgReturn = math.floor(entry[2])
    ROI = avgReturn/(avgInvestment/0.2)
    # Add markers to map
    Popup = folium.map.Popup(html="Average Housing Price: $" + str(round(avgInvestment / 0.2)) +
                                  "<br><br> Annual Income: $" + str(round(avgReturn)) +
                                  "<br><br> Projected ROI: " + str(round(ROI * 100)) + "%", max_width=300)
    ROImap.add_child(folium.Marker(location=[lat, lon], popup=Popup, icon=folium.Icon(color='red')))

ROImap.save("ROIMap.html")
