from multiprocessing.dummy import Pool as ThreadPool
import googlemaps
import argparse
import math
import json
import sys

with open('key', 'r') as fh:
    key = fh.readlines()[0].strip()

gmaps = googlemaps.Client(key=key)

def get_elevation(location):
    elevation = gmaps.elevation(location)[0]
    return elevation['elevation']

def distance_between_points(source, destination):
    # Using the Haversine formula
    # [0] is latitude
    # [1] is longitude

    def to_radians(deg):
        return deg * math.pi / 180

    earth_radius = 6371 # in km
    
    lat_differential = to_radians(destination[0] - source[0])
    long_differential = to_radians(destination[1] - source[1])
    initial_lat = to_radians(source[0])
    final_lat = to_radians(source[1])

    a = math.sin(lat_differential / 2) ** 2 + \
        math.sin(long_differential / 2) ** 2 * \
        math.cos(initial_lat) * \
        math.cos(final_lat)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius * c * 1000

def init_args():
    parser = argparse.ArgumentParser(description="""Google Maps Path Simulators: a utility to
            help simulate bike paths on stationary bikes.""")

    parser.add_argument("--url", 
                        help="""The file name holds the URL for the Google Maps path. 
                                Defaults to a file named 'url'.""",
                        default="url")

    parser.add_argument("--resistance_range",
                        help="The max resistance value for the bike",
                        default=10)

    parser.add_argument("--flat_ground_resistance_level",
                        help="""The resistance level on the bike that is most similar to 
                                flat ground.""",
                        default=5)

    # TODO: Add resolution arguement
    # TODO: Add threads argument

    return parser.parse_args()

# ==== Begin Script

args = init_args()

coordinates = []

with open(args.url, "r") as fh:
    for line in fh.readlines():
        line = line.strip().split(",")

        coordinate = (float(line[1]), float(line[2]))
        coordinates.append(coordinate)

# pool = ThreadPool(8)
# 
# elevations = pool.map(get_elevation, coordinates)
# 
# pool.close()
# pool.join()

distances = gmaps.distance_matrix([(42.274720000,-71.806640000),
                                   (42.274760000,-71.806640000)],
                                  [(42.274760000,-71.806640000),
                                   (42.274820000,-71.806670000)])

# print(coordinates)
# print(elevations)
# print(distances['rows'][0]['elements'][0]['distance']['value'])
# print(distances)

for i in range(3):
    print("{} -> {}".format(coordinates[i], coordinates[i + 1]))
    print(distance_between_points(coordinates[i], coordinates[i + 1]))

# for row in distances['rows']:
#     print(row['elements'][0]['distance']['value'])
