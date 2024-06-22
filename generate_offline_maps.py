# Create png with Mapbox Static Images API 
# You'll need a free mapbox token

import requests
import config

token = config.mapbox_token
# url = "https://api.mapbox.com/styles/v1/{username}/{style_id}/static/{overlay}/{lon},{lat},{zoom},{bearing},{pitch}|{bbox}|{auto}/{width}x{height}{@2x}"
# url = "https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/-121.5355,37.8505,12.34,0/300x200?access_token="

url = "https://api.mapbox.com/styles/v1/"

style_id = "ninja1221/clwv6cemx017o01qx320whazx"

coords = "5.1030,52.0843"
zoom = "15"
size = "720x400"

file_path = "images/map/"

def one_map(file_name):
    response = requests.get(f"{url}{style_id}/static/{coords},{zoom},0/{size}?access_token={token}")
    print(f"{url}{style_id}/static/{coords},{zoom},0/{size}?access_token={token}")
    if response:
        with open(file_path + file_name, "wb") as file:
            for chunk in response:
                file.write(chunk)
                
    print("done")

# zooms = number of zooms, aka how many maps 
def maps(zooms):
    for i in range(0,zooms):
        zoom = str(i)
        response = requests.get(f"{url}{style_id}/static/{coords},{zoom},0/{size}?access_token={token}")
        if response:
            with open(file_path + zoom + ".png", "wb") as file:
                for chunk in response:
                    file.write(chunk)
    print("done")
        

# one_map("map2.png")


maps(18)
