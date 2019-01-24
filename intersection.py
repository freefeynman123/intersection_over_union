import pandas as pd
import numpy as np
import time


def clip(subject_polygon: list, clip_polygon: list) -> np.array:
    """
    Calculates nodes' coordinates of the intersection of input polygons
    The approach is based on Sutherland–Hodgman algorithm

    Parameters
    ----------
    subject_polygon:
    list of tuples with Nx2 dimension
    clip_polygon:
    list of tuples with Nx2 dimension

    Returns
    -------
    output_list:
    list of lists containing x and y coordinates of the intersection polygon
    """

    def inside(point: tuple) -> bool:
        """
        Finds whether given point is inside clipping polygon

        Parameters
        ----------
        point:
        A tuple with points' coordinates

        Returns
        -------
        Boolean value indicating whether given point is inside the clipping polygon
        """
        cond1 = (clip_vertex_point[0] - clip_polygon_last_point[0]) * (point[1] - clip_polygon_last_point[1])
        cond2 = (clip_vertex_point[1] - clip_polygon_last_point[1]) * (point[0] - clip_polygon_last_point[0])
        return cond1 > cond2

    def compute_intersection(last_point: tuple, vertex_point: tuple, point_s: tuple,
                             point_e: tuple) -> np.array:
        """
        Computes intersection between a line segment and an infinite edge
        It is only called if such an intersection is known to exist

        Parameters
        ------------
        last_point:
        A tuple containing coordinates of one of the clipped polygon points,
        initiated with last point of this polygon, afterwards contains information
        about previously used vertex_point
        vertex_point:
        A tuple containing coordinates of one of the clipped polygon points
        point_s:
        A tuple containing coordinates of one of the subject polygon points
        initiated with last point of this polygon, afterwards contains information
        about previously used point_e
        point_e:
        A tuple containing coordinates of one of the subject polygon points

        Returns
        --------
        Coordinates of intersection point
        """
        polygon_difference = [last_point[0] - vertex_point[0], last_point[1] - vertex_point[1]]
        points_difference = [point_s[0] - point_e[0], point_s[1] - point_e[1]]
        n1 = last_point[0] * vertex_point[1] - last_point[1] * vertex_point[0]
        n2 = point_s[0] * point_e[1] - point_s[1] * point_e[0]
        n3 = 1.0 / (polygon_difference[0] * points_difference[1] - polygon_difference[1] * points_difference[0])
        return np.array([(n1 * points_difference[0] - n2 * polygon_difference[0]) * n3,
                         (n1 * points_difference[1] - n2 * polygon_difference[1]) * n3])

    output_list = subject_polygon
    clip_polygon_last_point = clip_polygon[-1]

    for clip_vertex in clip_polygon:
        clip_vertex_point = clip_vertex
        input_list = output_list
        output_list = []
        try:
            point_s = input_list[-1]
        except IndexError:
            # breaking in case of missing values in predictions
            break

        for subject_vertex in input_list:
            point_e = subject_vertex
            if inside(point_e):
                if not inside(point_s):
                    output_list.append(compute_intersection(clip_polygon_last_point, clip_vertex_point,
                                                            point_s, point_e))
                output_list.append(point_e)
            elif inside(point_s):
                output_list.append(compute_intersection(clip_polygon_last_point, clip_vertex_point,
                                                        point_s, point_e))
            point_s = point_e
        clip_polygon_last_point = clip_vertex_point
    return list(map(list, zip(*output_list)))


def shoelace_formula_area(x: list, y: list) -> float:
    """
    Calculates area of the simple polygon bsed on the shoelace algorithm

    Parameters
    -----------
    x:
    list contaning all x coordinates
    y:
    list containing all y coordinates

    Returns
    --------
    Area of a polygon with given coordinates
    """
    main_area = np.dot(x[:-1], y[1:]) - np.dot(x[1:], y[:-1])
    edge_terms = x[-1] * y[0] - y[-1] * x[0]
    return 0.5 * abs(main_area + edge_terms)


def intersection_over_union(coordinates: pd.DataFrame, label_a: str, label_b: str) -> np.array:
    """
    Calculates intersection over union for given data frame

    Parameters
    -----------
    coordinates:
    Pandas DataFrame containing points' coordinates grouped in rows

    label_a:
    String containing label for box_a in columns' names

    label_b:
    String containing label for box_a in columns' names

    Returns
    --------
    Numpy array with calculated intersection for each row given
    """
    box_a = data.filter(like=label_a, axis=1)
    box_b = data.filter(like=label_b, axis=1)
    results = []
    for coord_x, coord_y in zip(box_a.values, box_b.values):
        points_label = list(zip(coord_x[::2], coord_x[1::2]))
        points_prediction = list(zip(coord_y[::2], coord_y[1::2]))
        intersection = clip(points_label, points_prediction)
        label_area = shoelace_formula_area(coord_x[::2], coord_x[1::2])
        prediction_area = shoelace_formula_area(coord_y[::2], coord_y[1::2])
        try:
            intersection_area = shoelace_formula_area(intersection[0], intersection[1])
        except IndexError:
            # appending zero in case of missing values in predictions
            results.append(0)
            continue
        results.append(intersection_area / (label_area + prediction_area - intersection_area))
    return np.asarray(results)

