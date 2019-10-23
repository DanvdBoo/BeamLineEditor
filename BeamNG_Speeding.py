import json


def speedup_time(percent_quicker, input_file_location, output_file_location):
    json_file = open(input_file_location, "r")
    data = json.load(json_file)
    json_file.close()
    previous_time = 0
    previous_old_time = 0
    spd = 1 - percent_quicker/100

    for time in data['recording']['path']:
        try:
            if time['PlaceHolder'] == "start":
                spd = 1 - percent_quicker/100
            elif time['PlaceHolder'] == "stop":
                spd = 1
        except KeyError:
            spd = spd
        old_time = time['t']
        if old_time < previous_old_time:
            previous_old_time = old_time/2
        time['t'] = previous_time + (min(old_time - previous_old_time, 2) * spd)
        previous_time = time['t']
        previous_old_time = old_time

    json_file = open(output_file_location, "w+")
    json_file.write(json.dumps(data, indent=1, sort_keys=True))
    json_file.close()
    return


def speedup_time2(percent_quicker, percent_quicker2, input_file_location, output_file_location):
    json_file = open(input_file_location, "r")
    data = json.load(json_file)
    json_file.close()
    previous_time = 0
    previous_old_time = 0
    spd = 1

    for time in data['recording']['path']:
        try:
            if time['PlaceHolder'] == "start":
                spd = 1 - percent_quicker/100
            elif time['PlaceHolder'] == "switch":
                spd = 1 - percent_quicker2/100
            elif time['PlaceHolder'] == "stop":
                spd = 1
        except KeyError:
            spd = spd
        old_time = time['t']
        if old_time < previous_old_time:
            previous_old_time = old_time/2
        time['t'] = previous_time + (min(old_time - previous_old_time, 2) * spd)
        previous_time = time['t']
        previous_old_time = old_time

    json_file = open(output_file_location, "w+")
    json_file.write(json.dumps(data, indent=1, sort_keys=True))
    json_file.close()


# if __name__ == '__main__':
#     file_location = "autolong2.track.json"
#     file_location_write = "autolong2.4.track.json"
#
#     speedup_time(-40)
#     # speedup_time2(-13, 0)
#     print("Done!")

