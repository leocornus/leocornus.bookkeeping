
# bkviews.py

"""
general view adapters for bookkeeping.
"""

from datetime import datetime

from Acquisition import aq_inner
from DateTime import DateTime

from Products.Five.browser import BrowserView

from leocornus.bookkeeping.util.catalog import getYearQuery

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the default view for bookkeeping base folder.
class DefaultView(BrowserView):
    """
    The default view for a bookkeeping, which will provide a quick
    summary for all transations by year and transaction type.
    """

    # we need adapt Request too.
    def __init__(self, context, request):

        self.context = context
        self.request = request
        # the root folder of bookkeeping.
        self.bkfolder = aq_inner(self.context)

    # return the years to display.
    def getYears(self):
        """
        preparing a list of years for showing the summary.  We will start
        from year 2010 and end at current year.
        """

        years = [2010]
        thisYear = datetime.today().year
        for i in range(thisYear - years[0]):
            years.append(years[0] + 1 + i)

        return years

    # get the subtotal amount for given transaction type and year.
    def getAmounts(self, trxType, year):
        """
        the smount for sutotal, gst, pst as tuple
        """

        query = {
            'transactionDate' : getYearQuery(year),
            'transactionType' : trxType
            }
        trxs = self.bkfolder.searchTransactions(query)
        subtotal = 0
        gst = 0
        pst = 0
        for trx in trxs:
            obj = trx.getObject()
            subtotal += obj.subtotal()
            gst += obj.gst()
            pst += obj.pst()

        return (subtotal, gst, pst)

# The year view.
class YearView(BrowserView):
    """
    This view will provide the summary by category for the specified year. 
    It will show one column for each transaction type.  For each category, 
    the subtotal, gst, pst and total will be list.
    """
    
    # initializing
    def __init__(self, context, request):
        """
        year will be passed by a HTTP Request param.
        """

        self.context = context
        self.request = request
        # the root folder of bookkeeping.
        self.bkfolder = aq_inner(self.context)

