import matplotlib.pyplot as plt
from PIL import Image
from playwright.sync_api import sync_playwright
from transformers import pipeline

from Hike import Hike

"""
class Hike:
    Attributes:
        number:        Int
        _id   :        String
        length_3d:     Float
        user:          String
        start_time:    String
        max_elevation: Float
        bounds:        String
        uphill:        Float
        moving_time:   Float
        end_time:      String
        max_speed:     Float
        gpx:           String
        difficulty:    String
        min_elevation: Float
        url:           String
        downhill:      Float
        name:          String
        length_2d:     Float
    ***
    Methods:
        get_coordinates: Returns the latitude and longitude of the hike
            -> Dict[
                "latitude": Float,
                "longitude": Float
            ]

        get_elevations: Returns a list of all elevations during the hike
            -> List[Float]

        get_times: Returns a list of all times during the hike
            -> List[String]

        get_relative_times: Returns a list of all relative times during the hike
            -> List[Tuple[Int, Int, Int]]

        get_cumulative_times: Returns a list of all cumulative times during the hike
            -> List[Tuple[Int, Int, Int]]

        get_path_coordinates: Returns a list of all coordinates of the path during the hike (latitude, longitude)
            -> List[Tuple[Float, Float]]
"""

MIN_DELAY = 250
GPX_FILE_NAME = "temp.gpx"
PNG_PATH = "./screenshots/temp.png"
HTML_PATH = "./screenshots/temp.html"
pipe = pipeline(task='depth-estimation', model='depth-anything/Depth-Anything-V2-Large-hf')

def run(hike_number):
    hike = Hike(hike_number)
    with sync_playwright() as playwright:
        # Starting the browser
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Recuperating the latitude and longitude of the hike
        lat, lng = hike.get_coordinates().values()

        # Go to the url
        page.goto(f"https://www.google.com/maps/search/?api=1&query={lat},{lng}")

        # Fetching and then clicking on the "Tout refuser" button as we have an opening pop-up when we launch Google Map
        # page.wait_for_timeout(250)
        page.get_by_role("button").nth(1).click()
        
        # Clicking on the "Réduire le panneau latéral" button that is on the left side of the screen
        lateral_panel_closed = False
        while not lateral_panel_closed:
            try:
                page.get_by_role("button").nth(14).click()
                lateral_panel_closed = True
                page.wait_for_timeout(MIN_DELAY * 2) # Time for panel to close and load the hidden map
            except:
                pass
        
        # # Moving the mouse to the center of the screen and make a zoom out from the position
        page.mouse.move(page.viewport_size["width"] / 2, page.viewport_size["height"] / 2 + 50)
        for _ in range(2):
            page.mouse.wheel(delta_x=0, delta_y=1)
            page.wait_for_timeout(MIN_DELAY)
        page.wait_for_timeout(MIN_DELAY * 4) # Time for loading the map after zooming out

        page.get_by_role("button").nth(8).click(force=True)
        page.wait_for_timeout(MIN_DELAY * 2)
        
        # for loc in page.get_by_role("menuitemcheckbox").all():
        #     print(loc.get_attribute("jsaction"))

        page.get_by_role("menuitemcheckbox").nth(0).click()
        page.keyboard.press("Escape")
        page.wait_for_timeout(MIN_DELAY * 8)
        # print(page.get_by_role("menuitemcheckbox").nth(0).click(delay=100))

        # page.get_by_role("menuitemcheckbox").nth(0).check()

        # for loc in page.get_by_role("list").nth(2).all():
        #     print(loc.all().get_attribute("role"))

        # Taking a screenshot of the map
        page.screenshot(path=PNG_PATH, full_page=True)

        browser.close()

def gps_visualizer(hike_number):
    hike = Hike(hike_number)
    with sync_playwright() as playwright:
        # Starting the browser
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Go to the url
        page.goto("https://www.gpsvisualizer.com")

        # Clicking on the "Autoriser tous les cookies" button
        page.get_by_role("button").nth(2).click()
        page.wait_for_timeout(MIN_DELAY)

        # Clicking on the "Choose File" button
        with open(GPX_FILE_NAME, "w") as file:
            file.write(hike.gpx)

        page.locator("input[type=file]").set_input_files(GPX_FILE_NAME)
        page.wait_for_timeout(MIN_DELAY)

        print(page.locator("#homepage_submit").click())
        page.wait_for_timeout(MIN_DELAY * 2)

        page.screenshot(path=PNG_PATH, full_page=True)

# TEST
from gpxplotter import add_segment_to_map, create_folium_map, read_gpx_file


def gpx_plot(hike_number, gpx):
    with open(GPX_FILE_NAME, "w") as file:
        file.write(gpx)

    the_map = create_folium_map(tiles='opentopomap')
    for track in read_gpx_file(GPX_FILE_NAME):
        for i, segment in enumerate(track['segments']):
            add_segment_to_map(the_map, segment, line_options={'color': 'violet', 'weight': 5})
    the_map.save(HTML_PATH)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://wsl.localhost/Ubuntu/home/mouthieu/ia-introduction/projet/" + HTML_PATH[2:])
        page.wait_for_timeout(MIN_DELAY * 2)
        page.screenshot(path=PNG_PATH, full_page=True)
        browser.close()

    img = Image.open(PNG_PATH)
    depth = pipe(img)['depth']
    plt.imshow(depth, cmap='inferno')
    plt.show()

    

if __name__ == '__main__':
    hike = Hike(2)
    gpx_plot(hike.number, hike.gpx)

    # add_all_tiles(the_map)
    # add_tiles_to_map(the_map, 'Stamen Terrain')
    # the_map.show_in_browser()
    # run(hike.number)
    # gps_visualizer(hike.number)
    # img = Image.open('./screenshots/example.png').show()
