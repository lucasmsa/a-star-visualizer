import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

list_of_coordinates = [(40, 34), (41, 34), (42, 34), (43, 34), (44, 34), (45, 34), (46, 34)]
ims = []
grid = cv2.imread("./output/cell_image_with_initial_points.png")
im = ax.imshow(grid, animated=True)
for coordinate in list_of_coordinates:
    cv2.circle(grid, coordinate, 0, (230, 0, 126), -1)
    im = ax.imshow(grid, animated=True)
    ims.append([im])



# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()