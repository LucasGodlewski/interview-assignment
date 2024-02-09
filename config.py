import pandas as pd

# For debugging; shows more info during execution of the app
DEBUG = True

# Cache Time To Live in seconds
CACHE_TTL = 5

# Definition of the columns from the input file
HEADER_NAMES = ['instrument', 'date', 'value']

# According to task, this is the current date
END_DATE = pd.Timestamp(2014, 12, 19)

# The day of the week with Monday=0, Sunday=6
BUSINESS_DAYS = tuple(range(0, 5))

# Set desired precision for the mean calculation
PRECISION = 50

# Define name for instruments with custom logic
INSTRUMENT1 = 'INSTRUMENT1'
INSTRUMENT2 = 'INSTRUMENT2'
INSTRUMENT3 = 'INSTRUMENT3'

# Year and month criteria for instrument2
INSTRUMENT2_YEAR = 2014
INSTRUMENT2_MONTH = 11
