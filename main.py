from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    images = [
        {
            "name": "Calle Crisologo",
            "url": "https://ik.imagekit.io/tvlk/blog/2017/11/Calle-Crisologo-by-night-750x469.jpg?tr=dpr-2,w-675,",
            "latitude": 17.57278,
            "longitude": 120.38889
        },
        {
            "name": "Boracay",
            "url": "https://www.rappler.com/tachyon/2022/07/boracay.jpg",
            "latitude": 11.967222,
            "longitude": 121.924722
        },
        {
            "name": "Mayon Volcano",
            "url": "https://gttp.imgix.net/266095/x/0/guide-to-mayon-volcano-in-albay-bicol-world-s-most-perfect-volcanic-cone-4.jpg?auto=compress%2Cformat&ch=Width%2CDPR&dpr=1&ixlib=php-3.3.0&w=883",
            "latitude": 13.254722,
            "longitude": 123.685833
        },
        {
            "name": "Siargao Island",
            "url": "https://www.agoda.com/wp-content/uploads/2020/01/Things-to-do-in-Siargao-Island-Cloud-9-surfing-area-in-General-Luna.jpg",
            "latitude": 9.854167,
            "longitude": 126.040278
        },
        {
            "name": "Mt. Pinatubo",
            "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQs5noQ1YdK7lM-h1KOfQ7opRjb90XSVD_s0Q&s",
            "latitude": 15.143056,
            "longitude": 120.349444
        }
    ]

    number_of_items = len(images)

    # Define empty lists
    latitudes = []
    longitudes = []

    # Loop through the images list
    for image in images:
        latitudes.append(image['latitude'])
        longitudes.append(image['longitude'])

    # Now calculate the averages of latitudes and longitudes
    lat_average = sum(latitudes) / number_of_items
    lon_average = sum(longitudes) / number_of_items

    return  render_template("hello.html",
                            images=images,
                            latitude=lat_average,
                            longitude=lon_average)



