from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import re
import random
import string
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Directory to save uploaded files and images
UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'static/cow_pics'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Utility function to ensure text only has alphanumeric characters and spaces
def validate_text(text):
    return re.match(r'^[a-zA-Z0-9 ]*$', text) is not None

# Function to call cowsay from the OS
def generate_cowsay_output(text):
    command = f'cowsay -r {text}'
    output = os.popen(command).read()
    return output

# Generate a random filename for storing user-submitted text and images
def generate_random_filename(extension="txt"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '.' + extension

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle text input for cowsay
        user_text = request.form['user_text']
        if validate_text(user_text) and user_text.strip():
            random_filename = generate_random_filename()

            # Save the user-submitted text in the 'uploads' directory
            file_path = os.path.join(UPLOAD_FOLDER, random_filename)
            with open(file_path, 'w') as file:
                file.write(user_text)

            return redirect(url_for('result', file=random_filename))
        else:
            return render_template('index.html', error="Invalid input! Only alphanumeric characters and spaces are allowed.")
    return render_template('index.html')

@app.route('/result')
def result():
    # Get the filename from the query parameter
    filename = request.args.get('file', '')
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        # Read the user-submitted text from the file
        with open(file_path, 'r') as file:
            user_text = file.read()

        # Generate cowsay output from the user-submitted text
        cowsay_output = generate_cowsay_output(user_text)
        return render_template('result.html', cowsay_output=cowsay_output)
    else:
        return "File not found", 404

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        # Handle image upload (cow picture)
        if 'cow_image' in request.files:
            cow_image = request.files['cow_image']
            if cow_image.filename != '':
                # Save the image to the IMAGE_FOLDER
                image_filename = secure_filename(cow_image.filename)
                image_path = os.path.join(IMAGE_FOLDER, image_filename)
                cow_image.save(image_path)

                # Optionally scale down the image using PIL (Pillow)
                img = Image.open(image_path)
                img.thumbnail((300, 300))  # Scale down image to medium size (300x300 max)
                img.save(image_path)

        return redirect(url_for('gallery'))

    # Get a list of all uploaded cow images in the IMAGE_FOLDER
    images = os.listdir(IMAGE_FOLDER)
    def is_image_file(s):
        exts = [".png", ".jpg", ".webp", ".gif", ".jpeg", ".tiff", ".bmp"]
        return any(s.endswith(e) for e in exts)
    images = [url_for('static', filename=f'cow_pics/{image}') for image in filter(is_image_file, images)]

    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")

