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
    motions = {}  # part: [(start_index, end_index, distance)]
    for part_index, part in enumerate(pose_record):
        # itterates through the parts
        dists = get_distances(part, movement_threshold)
        clusters = get_part_clusters(dists)
        # find the individual motions
        motions[PART_MAP[part_index]] = convert_clusters(dists, clusters[0]) \
            + convert_clusters(dists, clusters[1])
        motions[PART_MAP[part_index]].sort(key=lambda x: x[0])
    return motions


def get_part_clusters(dists):
    pos = where(dists > 0)
    neg = where(dists < 0)
    pos_clusters = split(pos[0], where(diff(pos[0]) != 1)[0]+1)
    neg_clusters = split(neg[0], where(diff(neg[0]) != 1)[0]+1)
    return pos_clusters, neg_clusters


def convert_clusters(dists, clusters):
    motions = []
    for cluster in clusters:
        start = cluster[0]
        end = cluster[-1] + 1
        distance = absolute(sum(dists[start: end]))
        motions.append((start, end, distance))
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
