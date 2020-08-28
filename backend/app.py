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
        global MOVEMENT_THRESHOLD
        global FRAME_RATE
        global SONG_TIME
        POSE_RECORD = np.empty([17, 2, 3600])
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
        np.save('poses', POSE_RECORD)
        print('Saved to poses.npy')
        return 'success'

    return app
