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
    return earth_radius * c * 1000 # Convert to meters

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

    parser.add_argument("-t", "--threads",
                        help="The number of threads to run this program. Defaults at 4.",
                        default=4)

    parser.add_argument("-r", "--resolution",
                        help="""How many lat/long points each 'chunk' will hold. 
                                Defaults at 10.""",
                        default=50)

    return parser.parse_args()

# ==== Begin Script

args = init_args()

coordinates = []

with open(args.url, "r") as fh:
    for line in fh.readlines():
        line = line.strip().split(",")

        coordinate = (float(line[1]), float(line[2]))
        coordinates.append(coordinate)

elevations_raw = []
distance_sums = []

distance_sum = 0
for i in range(len(coordinates)):
    if i % args.resolution == 0 or i == len(coordinates) - 1:
        elevations_raw.append(coordinates[i])

    if i == 0:
        continue

    distance_sum += distance_between_points(coordinates[i - 1], coordinates[i])

    if i % args.resolution == 0 or i == len(coordinates) - 1:
        distance_sums.append(distance_sum)
        distance_sum = 0

pool = ThreadPool(args.threads)

elevations = pool.map(get_elevation, elevations_raw)

pool.close()
pool.join()
