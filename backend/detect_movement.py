from numpy import array, empty, NaN, subtract, matmul, square, sqrt, isnan
from scipy.spatial import distance_matrix
"""
POSE_RECORD is PART x POINT x FRAME
"""
MOVEMENT_THRESHOLD = .1

def detect_motions(pose_record):
    """
    Top level function which drives the rest of the detection.

    takes in the full pose_record from the flask app
    """
    # log of all the motions
    motions = {} # part: [(start_index, end_index, distance)]
    for part in pose_record:
        # itterates through the parts
        dist, nan_index = get_distances(part, MOVEMENT_THRESHOLD)
        # find the individual motions
        motions[part] = get_part_motion(dist, nan_index)
    return motions


def get_part_motion(dists, nans):
    """
    Returns a list of tuples that describe motions of the part in the form
    (start_time, end_time, distance) where the times are frame indexes and distance
    is the total amount of distance that the part moved

    inputs:
    -------
    dists: array of distances with NaN values for minimum thresholds
    nans: an array of the indexes of the NaNs are
    """
    clusters = get_nan_clusters(nans)
    motions = []


def get_nan_clusters(nans):
    """
    Returns start and end indexes for all continuous blocks in the array NaNs

    inputs:
    -------
    nans: an array of indexes where nans occur in a distance array
    """
    clustered_data = np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
    clusters = [(cluster[0], cluster[-1], np.sum(cluster)) for cluster in clustered_data]
    return clusters


def get_distances(part, threshold):
    """
    Returns a distance matrix of how much each part moved between frames.
    Removes any distances that are less than THRESHOLD also returns indexes of NaNs

    part is a 2 x Num_Frames array of points
    threshold is  a float that will be used as a mask on the distances matrix
    """
    # move part one column to the left so distance_matrix can calculated inter-frame distance
    shift = part[:, [1, -1]]
    # Drop the last column of part because we won't need it
    part = part[:, [0, -2]]
    # get distances between points
    dists = euclidian_dist(part, shift)
    # replace distances below threshold with NaN
    dists[dists < threshold] = NaN
    # get NaN indexes
    nan_index = argwhere(isnan(dists))
    return dists, nan_index


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
    dist_2 = matmul(C_2.T, array([1, 1]))
    return sqrt(dist_2)

if __name__ == '__main__':
    toy = empty([2, 3, 5])
    print(toy)
    detect_movement(toy)
