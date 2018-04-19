import googlemaps
import argparse

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

args = parser.parse_args()
