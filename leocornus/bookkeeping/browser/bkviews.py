
# bkviews.py

"""
general view adapters for bookkeeping.

preparing some data for testing... Suppose the there is a default Plone
site is binding to self.portal
 
create a BKFolder object as the context.
>>> self.portal.invokeFactory('BKFolder', id='bk',
...     title='doctesting in python code',
...     bk_transaction_types=('Expense'),
...     bk_transaction_categories=(
...         'Expense:Parking', 'Expense:Lunch:50', 'Expense:Gas:80'
...     )
... )
'bk'
>>> self.bk = getattr(self.portal, 'bk')
>>> self.bk.title
u'doctesting in python code'
 
"""

from datetime import datetime

from Acquisition import aq_inner
from DateTime import DateTime

from leocornus.bookkeeping.browser.base import BaseView

from leocornus.bookkeeping.util.catalog import getYearQuery

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the default view for bookkeeping base folder.
class DefaultView(BaseView):
    """
    The default view for a bookkeeping, which will provide a quick
    summary for all transations by year and transaction type.

    >>> from leocornus.bookkeeping.browser.bkviews import DefaultView

    >>> self.defaultView = DefaultView(self.bk, 'request')
    >>> self.defaultView.bkfolder.title == self.bk.title
    True
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

        >>> self.defaultView.getYears()
        [2010, 2011]
        """

        years = [2010]
        thisYear = datetime.today().year
        for i in range(thisYear - years[0]):
            years.append(years[0] + 1 + i)

        return years

    # retrun the the url for year view.
    def getYearViewUrl(self, year):
        """
        This URL will load the year view for all transactions.

        >>> self.defaultView.getYearViewUrl(2010)
        'bk_year_view?year=2010'
        >>> self.defaultView.getYearViewUrl(2011)
        'bk_year_view?year=2011'
        """

        return 'bk_year_view?year=' + str(year)

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
class YearView(BaseView):
    """
    This view will provide the summary by category for the specified year. 
    It will show one column for each transaction type.  For each category, 
    the subtotal, gst, pst and total will be list.

    we should be able to use the object from the doc string in class
    level.

    Can NOT understand why we need import YearView?
    >>> from leocornus.bookkeeping.browser.bkviews import YearView
    >>> from zope.publisher.browser import TestRequest

    Preparing a testing request with year parameter.

    >>> request = TestRequest(year='2010')
    >>> self.yearView = YearView(self.bk, request)
    >>> self.yearView.bkfolder.title
    u'doctesting in python code'
 
    """

    # initializing
    def __init__(self, context, request):
        """
        year will be passed by a HTTP Request param.
        """

        self.context = context
        self.request = request
        self.year = request['year']
        # the root folder of bookkeeping.
        self.bkfolder = aq_inner(self.context)

        self.yearSummary = {}
        # load year summary.
        #self.loadYearSummary()

    # retrun the the url for category view.
    def getCategoryViewUrl(self, trxType, category):
        """
        This URL will load the category view for all transactions.

        >>> self.yearView.getCategoryViewUrl('TestType', 'TestCategory')
        'bk_category_view?year=2010&category=TestCategory&trxtype=TestType'

        """

        return 'bk_category_view?year=' + self.year + '&category=' + category + '&trxtype=' + trxType

    # load year amounts.
    def loadYearSummary(self):
        """
        load amounts for each transaction type,

        can we use the yearView directly? -- Yes!

        When we try to load year amount from doctest, we alway got 
        ConnectionStateError from method searchTransactions.  The error is 
        raised when we try to get the physical path for the bkfolder.  We 
        need test this in a functional doctest text file.

        #>>> self.yearView.loadYearSummary()
        #>>> len(self.yearView.yearSummary)
        #2

        """

        for trxType in self.bkfolder.transactionTypes():
            typeSummary = {}
            # the summary for business business percentage.
            typeSummaryBp = {}
            # go throught each category under this type.
            for category in self.bkfolder.getCategories(trxType):
                # set the initial value here to hold the spot for no 
                # transaction catetories.
                categorySummary = {'subtotal' : 0.0, 'gst' : 0.0, 'pst' : 0.0}
                categoryBp = self.getCategoryBuzPercent(trxType, category)

                # search for all transaction under this category.
                query = {
                    'transactionDate' : getYearQuery(int(self.year)),
                    'transactionType' : trxType,
                    'transactionCategory' : category
                    }
                trxs = self.bkfolder.searchTransactions(query)
                # calculate the summary.
                for trx in trxs:
                    transaction = trx.getObject()
                    categorySummary['subtotal'] += transaction.subtotal()
                    categorySummary['gst'] += transaction.gst()
                    categorySummary['pst'] += transaction.pst()

                # add to type summary.
                typeSummary[category] = categorySummary
                # preparing the BP summary.
                categorySummaryBp = {}
                categorySummaryBp['subtotal'] = categorySummary['subtotal'] * categoryBp / 100
                categorySummaryBp['gst'] = categorySummary['gst'] * categoryBp / 100
                categorySummaryBp['pst'] = categorySummary['pst'] * categoryBp / 100
                typeSummaryBp[category] = categorySummaryBp
            # add to year summary.
            self.yearSummary[trxType] = typeSummary
            self.yearSummary[trxType + 'bp'] = typeSummaryBp

    # return the category business percentage.
    def getCategoryBuzPercent(self, trxType, category):
        """
        return the business percentage for ghe given type and category.

        testing with the BKFolder created on top of this file (package).

        >>> self.yearView.getCategoryBuzPercent('Expense', 'Lunch')
        50
        >>> self.yearView.getCategoryBuzPercent('Expense', 'Gas')
        80
        >>> self.yearView.getCategoryBuzPercent('Expense', 'Parking')
        100

        """

        return self.bkfolder.getCategoryBuzPercent(trxType, category)

    # return type summary for this year.
    def getTypeSummary(self, trxType):
        """
        type summary includes subtotal, gst, pst.
        """

        self.loadYearSummary()

        summary = {'subtotal':0.0, 'gst':0.0, 'pst':0.0}
        for categorySummary in self.yearSummary[trxType].values():
           summary['subtotal'] += categorySummary['subtotal']
           summary['gst'] += categorySummary['gst']
           summary['pst'] += categorySummary['pst']

        return summary

    # return type summary for this year.
    def getTypeBpSummary(self, trxType):
        """
        type summary includes subtotal, gst, pst.
        """

        summary = {'subtotal':0.0, 'gst':0.0, 'pst':0.0}
        for categorySummary in self.yearSummary[trxType + 'bp'].values():
           summary['subtotal'] += categorySummary['subtotal']
           summary['gst'] += categorySummary['gst']
           summary['pst'] += categorySummary['pst']

        return summary

   # return category summary for the type and category.
    def getCategorySummary(self, trxType, category):
        """
        category summary
        """

        return self.yearSummary[trxType][category]

    # return category summary for the type and category.
    def getCategoryBpSummary(self, trxType, category):
        """
        category summary business percentage
        """

        return self.yearSummary[trxType + 'bp'][category]

# The year view.
class CategoryView(BaseView):
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
        self.year = request['year']
        self.category = request['category']
        self.trxType = request['trxtype']
        # the root folder of bookkeeping.
        self.bkfolder = aq_inner(self.context)
        self.categoryTotal = {'subtotal':0.0, 'gst':0.0, 'pst':0.0}
        self.categoryBp = self.bkfolder.getCategoryBuzPercent(self.trxType, self.category)
        self.categoryBpTotal = {'subtotal':0.0, 'gst':0.0, 'pst':0.0}

    # return all transactions for this category.
    def getTransactions(self):

        query = {
            'transactionDate' : getYearQuery(int(self.year)),
            'transactionType' : self.trxType,
            'transactionCategory' : self.category
            }
        transactions = []

        trxs = self.bkfolder.searchTransactions(query)
        for trx in trxs:
            transaction = {}
            obj = trx.getObject()
            transaction['id'] = obj.id
            transaction['title'] = obj.title
            transaction['date'] = obj.transactionDate().strftime('%Y-%m-%d')
            transaction['description'] = obj.description
            transaction['editUrl'] = '/'.join(obj.getPhysicalPath()) + '/edit'
            summary = {
                'subtotal' : obj.subtotal(), 
                'gst' : obj.gst(),
                'pst' : obj.pst()}
            transaction['summary'] = summary

            self.categoryTotal['subtotal'] += obj.subtotal()
            self.categoryTotal['gst'] += obj.gst()
            self.categoryTotal['pst'] += obj.pst()
            # calculate BP total.
            self.categoryBpTotal['subtotal'] = self.categoryTotal['subtotal'] * self.categoryBp / 100
            self.categoryBpTotal['gst'] = self.categoryTotal['gst'] * self.categoryBp / 100
            self.categoryBpTotal['pst'] = self.categoryTotal['pst'] * self.categoryBp / 100

            # add to transactions.
            transactions.append(transaction)

        return transactions
