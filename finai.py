def clip(subject_polygon, clip_polygon):
   def inside(point):
      return(clip_vertex_point[0]-clip_polygon_last_point[0])*(point[1]-clip_polygon_last_point[1]) > (clip_vertex_point[1]-clip_polygon_last_point[1])*(point[0]-clip_polygon_last_point[0])
 
   def computeIntersection():
      dc = [ clip_polygon_last_point[0] - clip_vertex_point[0], clip_polygon_last_point[1] - clip_vertex_point[1] ]
      dp = [point_s[0] -point_e[0], s[1] -point_e[1] ]
      n1 = clip_polygon_last_point[0] * clip_vertex_point[1] - clip_polygon_last_point[1] * clip_vertex_point[0]
      n2 = point_s[0] *point_e[1] - s[1] *point_e[0] 
      n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
      return [(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3]
 
   outputList = subject_polygon
   clip_polygon_last_point = clip_polygon[-1]
 
   for clipVertex in clip_polygon:
      clip_vertex_point = clipVertex
      inputList = outputList
      outputList = []
     point_s= inputList[-1]
 
      for subjectVertex in inputList:
        point_e = subjectVertex
         if inside(point_e):
            if not inside(point_s):
               outputList.append(computeIntersection())
            outputList.append(point_e)
        point_elif inside(point_s):
            outputList.append(computeIntersection())
        point_s=point_e
      clip_polygon_last_point = clip_vertex_point
   return(outputList)