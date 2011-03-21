
# catalog.py

"""
general utilities for portal_catalog search and indexing.
"""

# Zope package.
from DateTime import DateTime

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# return the year range query for portal_catalog.
def getYearQuery(year):

    yearQuery = {
        'query' : [DateTime(year,1,1,0,0,0), DateTime(year,12,31,23,59,59)],
        'range' : 'min:max'
        }
    return yearQuery 
