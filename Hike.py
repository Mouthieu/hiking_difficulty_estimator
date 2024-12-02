import json

with open('hikes.json') as f:
    dict_data = json.load(f)

class Hike():
    def __init__(self, number):
        self.number        = number
        self._id           = dict_data["_id"][f"{number}"]
        self.length_3d     = dict_data["length_3d"][f"{number}"]
        self.user          = dict_data["user"][f"{number}"]
        self.start_time    = dict_data["start_time"][f"{number}"]
        self.max_elevation = dict_data["max_elevation"][f"{number}"]
        self.bounds        = dict_data["bounds"][f"{number}"]
        self.uphill        = dict_data["uphill"][f"{number}"]
        self.moving_time   = dict_data["moving_time"][f"{number}"]
        self.end_time      = dict_data["end_time"][f"{number}"]
        self.max_speed     = dict_data["max_speed"][f"{number}"]
        self.gpx           = dict_data["gpx"][f"{number}"]
        self.difficulty    = dict_data["difficulty"][f"{number}"]
        self.min_elevation = dict_data["min_elevation"][f"{number}"]
        self.url           = dict_data["url"][f"{number}"]
        self.downhill      = dict_data["downhill"][f"{number}"]
        self.name          = dict_data["name"][f"{number}"]
        self.length_2d     = dict_data["length_2d"][f"{number}"]

    def get_coordinates(self):
        two_str = self.bounds.split("]")
        left_str, right_str = two_str[0], two_str[1]
        min_coordinates = left_str.split("[")[1]
        max_coordinates = right_str.split("[")[1]

        min_long, min_lat = min_coordinates.split(",")
        max_long, max_lat = max_coordinates.split(",")

        latitude = (float(min_lat) + float(max_lat)) / 2
        longitude = (float(min_long) + float(max_long)) / 2

        return {
            "latitude": latitude,
            "longitude": longitude
        }
    
    def get_elevations(self):
        elev_list = self.gpx.split("ele")
        return_list = []
        for i in range(1, len(elev_list), 2):
            return_list.append(float(elev_list[i][1:-2]))
        return return_list
    
    def get_times(self):
        time__list = self.gpx.split("time")
        return_list = []
        for i in range(1, len(time__list), 2):
            return_list.append(time__list[i][12:-3])
        return return_list[1:]
    
    def get_relative_times(self):
        time_list = self.get_times()
        return_list = []
        for i in range(1, len(time_list)):
            return_list.append(self._substract_times(self._compute_time(time_list[i]), self._compute_time(time_list[i-1])))
        return [(0, 0, 0)] + return_list
    
    def get_cumulative_times(self):
        start_time = self._compute_time(self.get_times()[0])
        return_list = []
        for time in self.get_times():
            return_list.append(self._substract_times(self._compute_time(time), start_time))
        return return_list
    
    def get_path_coordinates(self):
        path_list = self.gpx.split("trkpt")
        return_list = []
        for i in range(1, len(path_list), 2):
            double_split = path_list[i].split('"')
            return_list.append((float(double_split[1]), float(double_split[3])))
        return return_list
    
    def _compute_time(self, string):
        return int(string.split(":")[0]), int(string.split(":")[1]), int(string.split(":")[2])
    
    def _substract_times(self, time1, time2):
        seconds = time1[2] - time2[2]
        minutes = time1[1] - time2[1]
        hours   = time1[0] - time2[0]
        if seconds < 0:
            seconds += 60
            minutes -= 1
        if minutes < 0:
            minutes += 60
            hours -= 1
        return (hours, minutes, seconds)