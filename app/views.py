# Important imports
from app import app
from flask import request, render_template
import os
import cv2
import numpy as np
from PIL import Image

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Route to home page


def get_logo():
    logo_upload = request.files['logo_upload']
    logoname = logo_upload.filename
    logo = Image.open(logo_upload)
    logo = np.array(logo.convert('RGB'))
    return cv2.resize(logo, (250, 250))


def get_coordinates(h_logo, w_logo, h_image, w_image):
    # center_y = int(h_image/2)
    # center_x = int(w_image/2)
    # top_y = center_y - int(h_logo / 2)
    # left_x = center_x - int(w_logo / 2)
    # bottom_y = top_y + h_logo
    # right_x = left_x + w_logo

    bottom_y = int(h_image - (0.01 * h_image))
    top_y = int(bottom_y - h_logo)
    right_x = int(w_image - 0.01*w_image)
    left_x = int(right_x - w_logo)
    return top_y, bottom_y, left_x, right_x


@app.route("/", methods=["GET", "POST"])
def index():

    # Execute if request is get
    if request.method == "GET":
        return render_template("index.html")

    # Execute if reuqest is post
    if request.method == "POST":
        option = request.form['options']
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)
        image_logow = np.array(image.convert('RGB'))
        h_image, w_image, _ = image_logow.shape

        if option == 'logo_watermark':
            logo = get_logo()
            h_logo, w_logo, _ = logo.shape

            top_y, bottom_y, left_x, right_x = get_coordinates(
                h_logo, w_logo, h_image, w_image)

            aoi = image_logow[top_y: bottom_y, left_x: right_x]
            image_logow[top_y: bottom_y, left_x: right_x] = cv2.addWeighted(
                aoi, 1, logo, 0.5, 0)

            # center_y = int(h_image / 2)
            # cv2.line(image_logow, (0, center_y),
            #          (left_x, center_y), (255, 255, 255), 10)
            # cv2.line(image_logow, (right_x, center_y),
            #          (w_image, center_y), (255, 255, 255), 10)

            img = Image.fromarray(image_logow, 'RGB')
            img.save(os.path.join(
                app.config['INITIAL_FILE_UPLOADS'], 'image.png'))
            full_filename = 'static/uploads/image.png'
            return render_template('index.html', full_filename=full_filename)
        else:
            text_mark = request.form['text_mark']

            cv2.putText(image_logow, text=text_mark, org=(w_image - 250, h_image - 40), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=2,
                        color=(255, 255, 255), thickness=2, lineType=cv2.LINE_4)
            timg = Image.fromarray(image_logow, 'RGB')
            timg.save(os.path.join(
                app.config['INITIAL_FILE_UPLOADS'], 'image1.png'))
            full_filename = 'static/uploads/image1.png'
            return render_template('index.html', full_filename=full_filename)


# Main function
if __name__ == '__main__':
    app.run(debug=True)
