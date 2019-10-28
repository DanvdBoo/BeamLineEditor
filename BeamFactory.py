import json


class BeamFactory:
    def __init__(self, input_file_location, output_file_location):
        self.output_file_location = output_file_location
        json_file = open(input_file_location, "r")
        self.file_data = json.load(json_file)
        json_file.close()
        self.global_speedup = 0
        self.local_speedup = 0
        self.start_ind, self.end_ind = 0, 0
        self.data = []

    def set_speedup_global(self, value):
        self.global_speedup = float(value)

    def set_speedup_local(self, value, start_ind, end_ind):
        self.local_speedup = value
        self.start_ind = start_ind
        self.end_ind = end_ind

    def set_data(self, data):
        self.data = data

    def save_changes(self):
        json_file = open(self.output_file_location, "w+")
        json_file.write(json.dumps(self.data, indent=1, sort_keys=True))
        json_file.close()
