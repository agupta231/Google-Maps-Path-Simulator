from multiprocessing.dummy import Pool as ThreadPool
import googlemaps
import argparse
import json
import sys

with open('key', 'r') as fh:
    key = fh.readlines()[0].strip()

gmaps = googlemaps.Client(key=key)

def get_elevation(location):
    elevation = gmaps.elevation(location)[0]
    return elevation['elevation']

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


args = parser.parse_args()

elevation = gmaps.elevation((42.274720000,-71.806640000))[0]
print(elevation['elevation'])

coordinates = []

with open(args.url, "r") as fh:
    for line in fh.readlines():
        line = line.strip().split(",")

        coordinate = (float(line[1]), float(line[2]))
        coordinates.append(coordinate)

pool = ThreadPool(8)

elevations = pool.map(get_elevation, coordinates)

pool.close()
pool.join()

print(coordinates)
print(elevations)
