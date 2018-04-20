# Imports
from multiprocessing.dummy import Pool as ThreadPool
import googlemaps
import argparse
from math import *
import json
import sys

# Key Verification
with open('key', 'r') as fh:
    key = fh.readlines()[0].strip()

# Hyper Parameters
gmaps = googlemaps.Client(key=key)
max_grade = 0.1 # Maximum slope of an average street. If your location has steeper raods,
                # change this value accordingly.
min_grade = -0.1 # Maximum downwards slope on an average street. This is basically the
                 # point at which you aren't putting in effort to bike
distance_accuracy = 2 # Number of decimal places to output for the distance

# Helper functions
def get_elevation(location):
    elevation = gmaps.elevation(location)[0]
    return elevation['elevation']

def distance_between_points(source, destination):
    # Using the Haversine formula
    # [0] is latitude
    # [1] is longitude

    R = 6373.0

    lat1 = radians(source[0])
    lon1 = radians(source[1])
    lat2 = radians(destination[0])
    lon2 = radians(destination[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c * 1000

def distance_between_points_(source, destination):

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

def km_to_miles(km):
    return km * 0.621371

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

    parser.add_argument('-a', '--accuracy',
                        help="How many decimal points the machine's resistance goes to. \
                              Defaults to 0.",
                        default=0)

    parser.add_argument('--miles',
                        help="Flag if you want miles instead of km",
                        action='store_true')

    return parser.parse_args()

# ==== Begin Script

# Get user arguments
args = init_args()

# Get the coordinates along the path
coordinates = []

with open(args.url, "r") as fh:
    for line in fh.readlines():
        line = line.strip().split(",")

        coordinate = (float(line[1]), float(line[2]))
        coordinates.append(coordinate)


# Split the coordinates into chunks based on user specifications
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

print(sum(distance_sums))
# Evaluate the elevations
pool = ThreadPool(args.threads)

elevations = pool.map(get_elevation, elevations_raw)

pool.close()
pool.join()

# Determine d_elevation / d_distance for each chunk
deltas = []
for i, summation in enumerate(distance_sums):
    deltas.append((elevations[i + 1] - elevations[i]) / summation)


# Normalize over the bike resistance values
normalized_deltas = []
for delta in deltas:
    if delta > 0:
        value = (delta / max_grade) * \
                (args.resistance_range - args.flat_ground_resistance_level) + \
                args.flat_ground_resistance_level

        if value > args.resistance_range:
            value = args.resistance_range

    elif delta == 0:
        value = args.flat_ground_resistance_level
    else:
        value = args.flat_ground_resistance_level * \
                (1 - (delta / min_grade))

        if value < 0:
            value = 0

    normalized_deltas.append(round(value, args.accuracy))

print(normalized_deltas)
print(sum(distance_sums))

# Print the values
running_total = 0
for i, resistance in enumerate(normalized_deltas):
    running_total += distance_sums[i] / 1000

    if i == len(normalized_deltas) - 1 or resistance != normalized_deltas[i + 1]:
        if args.miles:
            print("Bike at resistance {} for {} miles".format(resistance, 
                round(km_to_miles(running_total), distance_accuracy)))
        else:
            print("Bike at resistance {} for {} km".format(resistance, 
                round(running_total, distance_accuracy)))

        running_total = 0

print("dab")

for i in range(len(normalized_deltas)):
    print("Bike at resistance {} for {} km".format(normalized_deltas[i], 
                round(distance_sums[i] / 1000, distance_accuracy)))

