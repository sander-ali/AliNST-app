#First try for developing web server
from flask import Flask, request, render_template, send_from_directory, redirect, send_file
import os
import test
import neuralStyleProcess
import cv2

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	print("TARGET", target)

	if not os.path.isdir(target):
		os.mkdir(target)
	else:
		print("Couldn't create upload directory: {}".format(target))

	data = request.form.get("style")

	myFiles = []

	for file in request.files.getlist("file"):
		filename = file.filename
		destination = "".join([target, filename])
		file.save(destination)
		myFiles.append(filename)

	return render_template("complete.html", image_names=myFiles, selected_style=data)

@app.route('/upload/<filename>')
def send_original_image(filename):
    return send_from_directory("images", filename)

@app.route('/complete/<filename>/<selected_style>')
def send_processed_image(filename, selected_style):
    directoryName = os.path.join(APP_ROOT, 'images/')
    
    newImg = neuralStyleProcess.neuralStyleTransfer(directoryName, filename, selected_style)
    
    return send_from_directory("images", newImg)

if __name__ == "__main__":
    app.run(host='0.0.0.0')