from flask import Flask, render_template, request, Response
import numpy as np

# 17 parts, two coords, 3600 frames
# assumes 20 frames per second
FRAME_RATE = 20
SONG_TIME = 180 # in seconds
POSE_RECORD = np.empty([17, 2, FRAME_RATE*SONG_TIME]) # PART x POINT x FRAME
AUDIO_SAMPLE = None
FRAME_NUMBER = 0
MOVEMENT_THRESHOLD = .5

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
        POSE_RECORD = np.empty([17, 2, 3600])
        AUDIO_SAMPLE = None
        FRAME_NUMBER = 0

    @app.route("/log_pose", methods=['POST'])
    def log_pose():
        global FRAME_NUMBER
        print('started detect_movement')
        pose = request.get_json()
        for part_index, point in enumerate(pose):
            POSE_RECORD[part_index][0][FRAME_NUMBER] = point['position']['x']
            POSE_RECORD[part_index][1][FRAME_NUMBER] = point['position']['y']
        FRAME_NUMBER += 1
        return 'success!'



    return app
