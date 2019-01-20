import pandas as pd
import numpy as np
data = pd.read_csv("data.csv")

boxA = data.filter(like = "label", axis = 1)
boxB = data.filter(like = 'prediction', axis = 1)
boxB = boxB.fillna(0)

def clip(subject_polygon: list, clip_polygon: list) -> np.array:

    def inside(point: tuple) -> bool:
        cond1 = (clip_vertex_point[0]-clip_polygon_last_point[0])*(point[1]-clip_polygon_last_point[1])
        cond2 = (clip_vertex_point[1]-clip_polygon_last_point[1])*(point[0]-clip_polygon_last_point[0])
        return cond1 > cond2

    def computeIntersection() -> np.array:
        dc = [ clip_polygon_last_point[0] - clip_vertex_point[0], clip_polygon_last_point[1] - clip_vertex_point[1] ]
        dp = [point_s[0] -point_e[0], point_s[1] -point_e[1] ]
        n1 = clip_polygon_last_point[0] * clip_vertex_point[1] - clip_polygon_last_point[1] * clip_vertex_point[0]
        n2 = point_s[0] *point_e[1] - point_s[1] *point_e[0] 
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return np.array([(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3])

    outputList = subject_polygon
    clip_polygon_last_point = clip_polygon[-1]

    for clipVertex in clip_polygon:
        clip_vertex_point = clipVertex
        inputList = outputList
        outputList = []
        try:
            point_s= inputList[-1]
        except IndexError:
            break

        for subjectVertex in inputList:
            point_e = subjectVertex
            if inside(point_e):
                if not inside(point_s):
                    outputList.append(computeIntersection())
                outputList.append(point_e)
            elif inside(point_s):
                outputList.append(computeIntersection())
            point_s=point_e
        clip_polygon_last_point = clip_vertex_point
    return(list(map(list, zip(*outputList))))

def shoelace_formula_area(x: list,y: list) -> float:
    """
    x,y - coordinates
    """
    main_area = np.dot(x[:-1],y[1:]) - np.dot(x[1:], y[:-1])
    edge_terms = x[-1]*y[0] - y[-1]*x[0]
    return 0.5*abs(main_area + edge_terms)


if __name__ == "__main__":

	results = []
	for x,y in zip(boxA.values,boxB.values):
	    points_label = list(zip(x[::2], x[1::2]))
	    points_prediction = list(zip(y[::2], y[1::2]))
	    intersection = clip(points_label, points_prediction)
	    label_area = shoelace_formula_area(x[::2], x[1::2])
	    prediction_area = shoelace_formula_area(y[::2], y[1::2])
	    try:
	        intersection_area = shoelace_formula_area(intersection[0], intersection[1])
	    except IndexError:
	        results.append(0)
	        continue
	    results.append(intersection_area/(label_area + prediction_area - intersection_area))











