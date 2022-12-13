from flask import Flask, render_template, request, url_for
import cv2
import os
import platform
import sys


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data="HELLO")


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    img = request.files['img']
    img.save('static/img.jpg')

    img = cv2.imread('static/img.jpg')

    tmp = img
    tmp = cv2.resize(tmp, (416, 416))
    cv2.imwrite('static/img.jpg', tmp)

    os.system(
        'python detect.py --weights best.pt --project results --name results --source static/img.jpg --save-txt --save-conf')

    class_names = ['MONKEY', 'NO MONKEY']

    img = cv2.imread('static/img.jpg')
    cv2.imwrite('static/ans.jpg', img)

    with open('results/results/labels/img.txt', 'r') as f:
        line = f.readlines()[0].split()
        data = class_names[int(line[0])]

        bbox = [float(line[1]), float(line[2]), float(line[3]), float(line[4])]

        confidence = float(line[5])
        confidence = round(confidence, 2)
        confidence = str(confidence*100) + '%'

    if (platform.system() == 'Windows'):
        os.system('mkdir /s /q results')
    else:
        os.system('rm -rf results')

    return render_template('prediction.html', data=data, bbox=bbox, confidence=confidence)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
