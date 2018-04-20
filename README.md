# Google Maps Path Simulator
Are you thinking of biking to work, school, or something else? However, are you like me and
don't want to go on a 21-mile round trip after not working out for a year? 

This script will take your trip from Google Maps and convert into a format that you can take
to a stationary bike to give your path a "test round". It's a lot better to find out that
you aren't cut out for the workout in the gym rather than on the side of the road 6 miles
from home.

## Requirements
This script uses the Google Maps API for python. Follow 
[this](https://github.com/googlemaps/google-maps-services-python#installation) to install
the requirements to run it. 

You will also need an API key to run this script. Follow 
[this](https://github.com/googlemaps/google-maps-services-python#api-keys) to get your
credentials. You will need the Elevation API in particular. Once you have your key, save it
in a file named `key` in the root folder.

## Running the script
This script uses an outside source to convert the Google Maps URL into a list of lat / long
points that it can read. *Perhaps some contributor would like to integrate this
functionality into this script*. 

Follow [http://www.gpsvisualizer.com/convert_input](http://www.gpsvisualizer.com/convert_input)
