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
points that it can read. **Perhaps some contributor would like to integrate this
functionality into this script.**

### Getting the Google Maps URL
Simply map out our path in Google Maps. Choose the most optimal path, or whatever is the
safest for you. Once you are done, you should have something like the following:

![directions](https://i.imgur.com/WM4Jwg7.png)

Once you are satisfied, just copy the URL of the page (marked in the red box).

### Converting the URL to Latitude / Longitude Points
Follow [http://www.gpsvisualizer.com/convert_input](http://www.gpsvisualizer.com/convert_input)
to convert your Google Maps URL into a list of latitude / longitude. After following the
link, you should be greeted with the following form:

![form](https://i.imgur.com/46loKc2.png)

In the input labeled `1` in the image, this is where you are going to paste the **Google
Maps URL** of your directions. 

Change the drop down box for `Plain text delimiter` to be `comma` (labeled `2` in the image)

Now, click `convert`, and you should get the following text:

![form output](https://i.imgur.com/E7cgMwr.png)

With this output, **only copy the lines that start with `T`** and save that data into a text
file named `url` (no ending). An example `url` file has been included in this repository.

### Running the script
Once everything else has been taken care of, just run `python convert.py`. The following
flags can be passed:

| Flag    | Parameters | Effect |
| ------- | ---------- | ------ |
| `--url` | a filename | specify which file contains the lat/long data. Defaults to `url` |
| `--resistance_range` | a number | The maximum resistance on a bike. Defaults to 10 |
| `--flat_ground_resistance_level` | a number | The resistance that feels you are biking on level ground |
| `-t` | a number | How many threads you want the script to run on |
| `--resolution` | a number | How many lat / long points each "chunk" will hold. Defaults to 50 |
| `--accuracy` | a number |  How many decimal points the machine's resistance goes.  Defaults at 0. |
| `--miles` | None | Flag, if you want miles instead of km. Defaults to km. |

There are also some hyper parameters in the code:
* `max_grade` is the maximum slope of the average street in your area. Change it based on
  location.
* `min_grade` same as `max_grade`, but is the minimum slope.
* `distance_accuracy` is the number of decimal places you want your output to hold.

## Future Work
Depending on free time and how much attention this gets, I might get back to this. This a
list of things that I might try to implement:
* Merging the `gpsvisulizer` script with this one
* More multithreading
* Maybe a Google Chrome Extension front end to run this whenever you are on the Google Maps
  page.

## Note to potential contributors
If you are interesting in adding to this script, feel free to fork it and open a pull
request! I apologize for my code, it isn't my greatest. I whipped this up in a total of 10
hours.

