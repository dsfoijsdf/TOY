# import numpy as np

# x = np.array([[1,2,3], [4, 5, 6]])

# x[x==1] = 0
# print(x)

# # z = [True, False, True]
# # print(all(z))

# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# # from matplotlib import colors

# # print(colors.CSS4_COLORS)


        
# fig, ax = plt.subplots()
# rect = patches.Rectangle((0.1, 0.2), 0.2, 0.5, label="ABC")
# ax.add_patch(rect)

# plt.legend()
# plt.show()


import imageio
import os

img_dir = "./result/"

img_list = sorted(os.listdir(img_dir), key=lambda x : int(x.split('.')[0][5:]))
images = [imageio.imread(img_dir + img_name) for img_name in img_list]
imageio.mimwrite("result.gif", images, duration=0.5)