"""
This file is used to organize the images taken in the folder 'screenshots' into the dataset folder 'img_dataset'.
We just have to specify the type of image we want to classify and the script will move the images to the correct folder.
"""

import os

from Hike import Hike

IMAGE_TYPES = ["google_map", "gpx_plot", "gps_visualizer", "depth_gpx_plot"]
NUMBER_OF_IMAGES = 501

def classify(image_type, hike):
    img_path  = f'./screenshots/{image_type}/{image_type}_{hike.number}.png'
    dest_path = f'img_dataset/{hike.get_difficulty()[0]}/{image_type}_{hike.number}.png'
    try:
        os.replace(img_path, dest_path)
    except Exception as e:
        print(e)

def remove_image_from_dataset(image_type, hike):
    dest_path = f'./screenshots/{image_type}/{image_type}_{hike.number}.png'
    img_path  = f'img_dataset/{hike.get_difficulty()[0]}/{image_type}_{hike.number}.png'
    try:
        os.replace(img_path, dest_path)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # direc = os.DirEntry('./screenshots/gpx_plot/')
    for file in os.listdir('./screenshots/gpx_plot/'):
        hike_number = int(file[9:12])
        hike = Hike(hike_number)

        # Choose what type of images will be in the dataset (google_map, gpx_plot, gps_visualizer, depth_gpx_plot)
        # Here we choose the type of image
        classify(IMAGE_TYPES[1], hike)