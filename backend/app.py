from flask import Flask, render_template, request
import numpy as np
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from pydub.utils import make_chunks
from .detect_movement import detect_motions
from .audio_generation import generate_remix
import os


# 17 parts, two coords, 3600 frames
# assumes 20 frames per second
FRAME_RATE = 20
SONG_TIME = 180 # in seconds
POSE_RECORD = np.empty([17, 2, FRAME_RATE*SONG_TIME]) # PART x POINT x FRAME
AUDIO_SAMPLE = None
FRAME_NUMBER = 0
MOVEMENT_THRESHOLD = .5
AUDIO_CHUNK_LENGTH = 1000

def create_app():
    app = Flask(__name__)


    @app.route('/')
    def sample():
        return render_template('practice.html')

    @app.route('/start', methods=['POST', 'GET'])
    def start():
        # set the global variables back to being empty
        global POSE_RECORD
        global AUDIO_SAMPLE
        global FRAME_NUMBER
        global MOVEMENT_THRESHOLD
        global FRAME_RATE
        global SONG_TIME
        POSE_RECORD = np.empty([17, 2, FRAME_RATE * SONG_TIME])
        AUDIO_SAMPLE = None
        FRAME_NUMBER = 0
        data = request.get_json()
        MOVEMENT_THRESHOLD = float(data['MOVEMENT_THRESHOLD'])
        FRAME_RATE = int(data['FRAME_RATE'])
        SONG_TIME = int(data['SONG_TIME'])
        print(f'Starting Log with threshold: {MOVEMENT_THRESHOLD}')
        return 'success!'

    @app.route("/log_pose", methods=['POST'])
    def log_pose():
        global FRAME_NUMBER
        pose = request.get_json()
        pose_map = {}
        for part_index, point in enumerate(pose):
            print(point['part'], point['score'])
            if point['score'] > MOVEMENT_THRESHOLD:
                POSE_RECORD[part_index][0][FRAME_NUMBER] = point['position']['x']
                POSE_RECORD[part_index][1][FRAME_NUMBER] = point['position']['y']
            else:
                POSE_RECORD[part_index][0][FRAME_NUMBER] = -1
                POSE_RECORD[part_index][1][FRAME_NUMBER] = -1
        FRAME_NUMBER += 1
        return 'success!'

    @app.route('/stop', methods=['POST'])
    def stop():
        audio_data = request.files['audio_data']
        chunk_length = AUDIO_CHUNK_LENGTH
        chunks = make_chunks(audio_data, chunk_length)
        chunk_index = np.random.randint(0, len(chunks), 17)
        chunks = [chunks[i] for i in chunk_index] # get rid of the extra chunks
        motions = detect_motions(POSE_RECORD, 1)
        remix = generate_remix(motions, chunks)

        # choose 17 random chunks
        # assign those random chunks to parts
        # use the parts to reassemble the chunks
        # return the new audio
        np.save('poses', POSE_RECORD)
        print('Saved to poses.npy')
        return 'success'

    # the route for uploading the music
    @app.route('/api/upload', methods=['POST', 'GET'])
    def api_message():
        if (request.method == 'POST'):
            r = request.files["audio_data"]
            r.save(secure_filename(r.filename) + ".wav")
        audio = AudioSegment.from_file("blob.wav")  # Gets the name of a wav file in current directory
        chunk_length = 1000  # of miliseconds in each file
        chunks = make_chunks(audio, chunk_length)   # Splits file into separate chunks each with length chunkLength
        for i, chunk in enumerate(chunks):
            chunk_name = "chunk{0}.wav".format(i)
            print("exporting", chunk_name)
            chunk.export(chunk_name, format="wav")  # Exports to a wav file in the current path
        return 'file uploaded successfully'

    return app
