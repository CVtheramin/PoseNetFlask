from flask import Flask
from flask import request
from datetime import datetime
from flask import render_template
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from pydub.utils import make_chunks
import re
import os

app = Flask(__name__)

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route('/api/upload', methods = ['POST', 'GET'])
def api_message():
    if (request.method == 'POST'):
        r = request.files["audio_data"]
        r.save(secure_filename(r.filename) + ".wav")
    audio = AudioSegment.from_file("blob.wav")  #Gets the name of a wav file in current directory
    chunkLength = 1000 #of miliseconds in each file
    chunks = make_chunks(audio, chunkLength)   #Splits file into separate chunks each with length chunkLength
    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)
        print("exporting"), chunk_name
        chunk.export(chunk_name, format= "wav") #Exports to a wav file in the current path
    return 'file uploaded successfully'

@app.route('/practice/')
def practice():
    return render_template("practice.html")
