import json

file_location = ""
file_location_write = ""


def add_lap_notation(x1, x2, y1, y2, start_stop):
    json_file = open(file_location, "r")
    data = json.load(json_file)
    json_file.close()
    p = (x1, y1)
    q = (x2, y2)
    prev = 0
    lap_counter = 1

    for dat in data['recording']['path']:
        if prev != 0:
            r = (dat['x'], dat['y'])
            s = (prev['x'], prev['y'])
            o1 = orientation(p, q, r)
            o2 = orientation(p, q, s)
            o3 = orientation(r, s, p)
            o4 = orientation(r, s, q)
            if (o1 != o2) & (o3 != o4):
                prev['PlaceHolder'] = start_stop
                lap_counter += 1
        prev = dat

    json_file = open(file_location_write, "w+")
    json_file.write(json.dumps(data, indent=1, sort_keys=True))
    json_file.close()


def orientation(p, q, r):
    val = (q[1]-p[1]) * (r[0]-q[0]) - (q[0]-p[0]) * (r[1]-q[1])
    return 1 if val > 0 else 2


def select_points(point_track):
    json_file = open(point_track, "r")
    point_track_data = json.load(json_file)
    json_file.close()

    x1 = point_track_data['recording']['path'][0]['x']
    x2 = 0
    y1 = point_track_data['recording']['path'][0]['y']
    y2 = 0

    for time in point_track_data['recording']['path']:
        x2 = time['x']
        y2 = time['y']

    return x1, x2, y1, y2


def clear_placeholders():
    json_file = open(file_location, "r")
    data = json.load(json_file)
    json_file.close()

    for time in data['recording']['path']:
        try:
            del time['PlaceHolder']
        except KeyError:
            continue

    json_file = open(file_location_write, "w+")
    json_file.write(json.dumps(data, indent=1, sort_keys=True))
    json_file.close()

    print("cleared files")


if __name__ == '__main__':
    file_location = "HH9.47.track.json"
    file_location_write = file_location
    clear_placeholders()
    X1, X2, Y1, Y2 = select_points("000020.track.json")
    add_lap_notation(X1, X2, Y1, Y2, "start")
    print("added start")
    # X1, X2, Y1, Y2 = select_points("000021.track.json")
    # add_lap_notation(X1, X2, Y1, Y2, "switch")
    # print("added switch")
    X1, X2, Y1, Y2 = select_points("000021.track.json")
    add_lap_notation(X1, X2, Y1, Y2, "stop")
    print("added stop")

    print("Done!")
