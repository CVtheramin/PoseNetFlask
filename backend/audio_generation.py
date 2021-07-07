""" This file has been made obsolete """


import pydub
from detect_movement import *
import numpy as np

FRAME_LENGTH = 1000 / 20

def generate_remix(motions, audio_chunks):
    parts = []
    for index, audio in enumerate(audio_chunks):
        part = generate_part(motions[PART_MAP[index]], audio)
    return None


def generate_part(part_motions, audio_segment):
    part_mix = None
    silence = pydub.AudioSegment.silent(duration=FRAME_LENGTH)
    for index, motion in enumerate(part_motions):
        audio_time = motion[1] - motion[0]
        if part_mix:
            part_mix += audio_segment[:audio_time]
        else:
            part_mix = audio_segment[:audio_time]
        if index < len(part_motions) - 2:
            next_sound = part_motions[index + 1][0]
            gap = next_sound - motion[1]
            if gap > 0:
                part_mix += silence * gap

    part_mix.export('part.mp3', format='mp3')


if __name__ == '__main__':
    music = pydub.AudioSegment.from_file('Checkie_Brown_-_09_-_Mary_Roose_CB_36.mp3', 'mp3')
    poses = np.load('poses.npy')
    motions = detect_motions(poses, 1)
    generate_part(motions['leftEar'], music)
