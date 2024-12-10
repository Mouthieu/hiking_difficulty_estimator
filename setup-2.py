import os

from Hike import Hike

if __name__ == '__main__':
    # for index in range(3001):
    #     hike = Hike(index)
    #     img_path = f'./screenshots/gpx-plot/gpx_plot_{index}.png'
    #     current_difficulty = hike.get_difficulty()[0]
    #     # if current_difficulty == "T3+":
    #     #     print(index)
    #     try:
    #         # print(hike.get_difficulty()[0])
    #         os.replace(img_path, f'img_dataset/{current_difficulty}/{index}.png')
    #     except Exception as e:
    #         print(e)
    for index in range(3001):
        hike = Hike(index)
        dest_path = f'./screenshots/gpx-plot/gpx_plot_{index}.png'
        current_difficulty = hike.get_difficulty()[0]
        img_path = f'./screenshots/gpx-plot/depth_gpx_plot_{index}.png'
        # if current_difficulty == "T3+":
        #     print(index)
        try:
            # print(hike.get_difficulty()[0])
            os.replace(dest_path, img_path)
        except Exception as e:
            print(e)