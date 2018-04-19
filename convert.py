import googlemaps
import argparse
import json
import sys

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

with open('key', 'r') as fh:
    key = fh.readlines()[0].strip()

gmaps = googlemaps.Client(key=key)

elevation = gmaps.elevation((42.274720000,-71.806640000))[0]
print(elevation['elevation'])

coordinates = []
elevations = []

with open(args.url, "r") as fh:
    for line in fh.readlines():
        line = line.strip().split(",")

        coordinate = (float(line[1]), float(line[2]))
        elevation = gmaps.elevation(coordinate)[0]
        print(elevation)

        coordinates.append(coordinate)
        elevations.append(elevation['elevation'])

print(coordinates)
print(elevations)
