from numpy import array, NaN, subtract, matmul, square, sqrt, isnan, \
    split, diff, where, argwhere, reshape, negative, absolute
from scipy.spatial import distance_matrix
"""
POSE_RECORD is PART x POINT x FRAME
"""
PART_MAP = {0: 'nose',
            1: 'leftEye',
            2: 'rightEye',
            3: 'leftEar',
            4: 'rightEar',
            5: 'leftShoulder',
            6: 'rightShoulder',
            7: 'leftElbow',
            8: 'rightElbow',
            9: 'leftWrist',
            10: 'rightWrist',
            11: 'leftHip',
            12: 'rightHip',
            13: 'leftKnee',
            14: 'rightKnee',
            15: 'leftAnkle',
            16: 'rightAnkle'}


def detect_motions(pose_record, movement_threshold):
    """
    Top level function which drives the rest of the detection.

    takes in the full pose_record from the flask app
    """
    # log of all the motions
    motions = []  # part: [(start_index, end_index, distance)]
    for part_index, part in enumerate(pose_record):
        # preprocess part
        processed_part = preprocess_part(part)
        # itterates through the parts
        dists = get_distances(processed_part, movement_threshold)
        clusters = get_part_clusters(dists)
        # find the individual motions
        # motions[PART_MAP[part_index]] = convert_clusters(dists, clusters[0]) \
        #     + convert_clusters(dists, clusters[1])
        motions += convert_clusters(dists, clusters[0])
        motions += convert_clusters(dists, clusters[1])
        # sort so that the motions are in the right order
        motions.sort(key=lambda x: x[0])
    return motions

def preprocess_part(part):
    """The API processes information as it comes in and if the score of a part
    is below the threshold it replaces the index with -1. These need to be
    swapped out for the average of the coordinates on either side (if they
    exist) if they don't exist replace with NaN """
    missing = where(part[0] == -1)
    miss_clusters = split(missing, where(diff(missing) != 1)[0]+1)
    for miss in miss_clusters:
        if len(miss) > 1:
            part[0][miss] = NaN
            part[1][miss] = NaN
        elif len(miss) == 1:
            left = miss[0] - 1
            right = miss[0] + 1
            x = (part[0][left] + part[0][right]) / 2
            y = (part[1][left] + part[1][right]) / 2
            part[0][miss] = x
            part[1][miss] = y
    return part

def get_part_clusters(dists):
    pos = where(dists > 0)
    neg = where(dists < 0)
    pos_clusters = split(pos[0], where(diff(pos[0]) != 1)[0]+1)
    neg_clusters = split(neg[0], where(diff(neg[0]) != 1)[0]+1)
    return pos_clusters, neg_clusters


def convert_clusters(dists, clusters):
    motions = []
    for cluster in clusters:
        if len(cluster) > 0:
            start = cluster[0]
            end = cluster[-1] + 1
            distance = absolute(sum(dists[start: end]))
            motions.append((start, end, int(distance)))
    return motions


def get_distances(part, threshold):
    """
    Returns a distance matrix of how much each part moved between frames.
    Removes any distances that are less than THRESHOLD also returns indexes of NaNs

    part is a 2 x Num_Frames array of points
    threshold is  a float that will be used as a mask on the distances matrix
    """
    # move part one column to the left so distance_matrix can calculated inter-frame distance
    shift = part[:, 1: -1]
    # Drop the last column of part because we won't need it
    part = part[:, 0: -2]
    # get distances between points
    dists = euclidian_dist(part, shift)
    # replace distances below threshold with NaN
    dists[absolute(dists) < threshold] = NaN
    return dists


def euclidian_dist(A, B):
    """
    Helper function which calculates the euclidian distance between all x, y points in a matrix

    runs in O(log n) time

    Input:
    -------
    A, B np.arrays of dimension [2, n]
    """
    C = subtract(B, A)
    C_2 = square(C)
    C_2_neg = where(C < 0, negative(C_2), C_2)
    dist_2 = matmul(C_2.T, array([1, 1]))
    dist_2_neg = matmul(C_2_neg.T, array([1, 1]))
    dist = sqrt(dist_2)
    return where(dist_2_neg < 0, negative(dist), dist)
