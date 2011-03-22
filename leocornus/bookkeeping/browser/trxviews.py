
# trxviews.py

"""
general view adapters for transaction.
"""

from Acquisition import aq_inner

from Products.Five.browser import BrowserView

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
        self.transaction = aq_inner(self.context)

    # return the year of transaction date..
    def getYear(self):
        """
        return as a string.
        """

        year = self.transaction.transactionDate().year()
        return str(year)

    def getBaseUrl(self):
        
        return '/'.join(self.transaction.getParentNode().getPhysicalPath())

    # retrun the the url for year view.
    def getYearViewUrl(self):
        """
        This URL will load the year view for all transactions.
        """

        return self.getBaseUrl() + '/bk_year_view?year=' + self.getYear() 

    def getCategoryViewUrl(self):

        url = self.getBaseUrl()
        url += '/bk_category_view?year=' + self.getYear() + '&category=' 
        url += self.transaction.transactionCategory() + '&trxtype='
        url += self.transaction.transactionType()
        return url 
