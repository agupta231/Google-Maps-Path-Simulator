FROM python:3

RUN pip install -U googlemaps

WORKDIR /app

CMD python convert.py --resistance_range 25 --flat_ground_resistance 5 --accuracy 2 --miles -t 8
