# sqlalchemy-challenge

This project contains a number of different apps. First we created an app that calls our
SQLite database to collect weather data from a variety of Hawaiian weather stations over
the past year. Next we collected this data and visualized the amount of precipitation per day
over the entire year. Next we sorted out the weather observatory and determined which station had
created the most observations and we observed the data from this station alone.
We then created two trips, one in June and one in December and reviewed the average temperature for
our desired date ranges. Unsurprisingly we found that the two ranges were remarkably similar.
We then sorted all of our weather stations by precipitation and reviewed their position and elevation data.
Finally we calculated the normal values for minimum, average, and maximum temperature for all instances
of a given day through our dataset. For example we took the data for January first for every year on record.
We plotted this data to observe the average temperature change throughout the year in Hawaii. Unsurprisingly
again, the weather seems like it would be lovely almost all of the year.

Finally we created a Flask app to allow users to pull their own data from our analyses. The app is available
with the following Routes:
'''
Available Routes:

The Precipitation Module returns all of the precipitation values along with their recorded dates
Route: /api/v1.0/precipitation

The Stations Module returns the names of all of the stations available in our dataset
/api/v1.0/stations

The following date module returns a list of the Minimum, Average, and Maximum Temperatures recorded over the given date range
If no end date is given the end date is assumed to be the last datapoint available in the dataset.
/api/v1.0/start
/api/v1.0/start/end

*Start and End in the above routes represent start and end dates* 
''''