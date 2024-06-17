from flask import Flask, render_template
from flask import request, redirect, flash, url_for
from flask import send_from_directory
import exifread
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max-limit.
app.secret_key = 'some_secret_key_here'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_exif_data(image_path):
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        return tags

def get_geolocation(exif_data):
    def convert_to_degress(value):
        d = float(value[0].num) / float(value[0].den)
        m = float(value[1].num) / float(value[1].den)
        s = float(value[2].num) / float(value[2].den)

        return d + (m / 60.0) + (s / 3600.0)

    latitude = None
    longitude = None

    if 'GPS GPSLatitude' in exif_data and 'GPS GPSLongitude' in exif_data and \
       'GPS GPSLatitudeRef' in exif_data and 'GPS GPSLongitudeRef' in exif_data:
        lat_value = exif_data['GPS GPSLatitude'].values
        lat_ref = exif_data['GPS GPSLatitudeRef'].values[0]
        lon_value = exif_data['GPS GPSLongitude'].values
        lon_ref = exif_data['GPS GPSLongitudeRef'].values[0]

        latitude = convert_to_degress(lat_value)
        if lat_ref != 'N':
            latitude = -latitude

        longitude = convert_to_degress(lon_value)
        if lon_ref != 'E':
            longitude = -longitude

    return latitude, longitude


@app.route("/")
def index():
    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = []

    for img in image_files:
        if allowed_file(img):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], img)
            exif_data = get_exif_data(filename)
            lat, lon = get_geolocation(exif_data)
            if lat is not None:
                images.append({
                    'filename': filename,
                    'latitude': lat,
                    'longitude': lon,
                    'name': img
                })

    number_of_items = len(images)

    # Define empty lists
    latitudes = []
    longitudes = []

    # Loop through the images list
    for image in images:
        latitudes.append(image['latitude'])
        longitudes.append(image['longitude'])

    # Now calculate the averages of latitudes and longitudes
    lat_average = sum(latitudes) / number_of_items if number_of_items > 0 else 0
    lon_average = sum(longitudes) / number_of_items if number_of_items > 0 else 0

    return  render_template("hello.html",
                            images=images,
                            latitude=lat_average,
                            longitude=lon_average)


@app.route("/uploads/<filename>")
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/upload", methods=["POST"])
def upload():
    if 'files[]' not in request.files:
        flash("No images given.")
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    if not files:
        flash("No selected file.")
        return redirect(request.url)

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    flash("Photos uploaded successfully!")
    return redirect(url_for('index'))
