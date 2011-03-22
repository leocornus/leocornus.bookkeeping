# testSearch.py

"""
testing catalog and search on bookkeeping
"""

import unittest

# zope DateTime package.
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

from base import BookkeepingTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestCatalogSetup(BookkeepingTestCase):
    """
    We will set up some indexes through the catalog.xml file. This test
    case is to make sure that the indexes are set up properly.
    """

    def afterSetUp(self):
        # get the portal_catalog tool
        self.catalog = self.portal.portal_catalog

    def testTransactionDateIndex(self):
        # transactionDate should be DateIndex
        itype = self.catalog.Indexes['transactionDate'].__class__.__name__
        self.assertEquals(itype, 'DateIndex')

    def testTransactionTypeIndex(self):
        # transactionDate should be DateIndex
        itype = self.catalog.Indexes['transactionType'].__class__.__name__
        self.assertEquals(itype, 'FieldIndex')

    def testTransactionCategoryIndex(self):
        # transactionDate should be DateIndex
        itype = self.catalog.Indexes['transactionCategory'].__class__.__name__
        self.assertEquals(itype, 'FieldIndex')

class TestSearchIndexing(BookkeepingTestCase):
    """
    the new index should searable after create a new transaction.
    """

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.loginAsPortalOwner()
        # create a bookkeeping root folder.
        self.portal.invokeFactory('BKFolder', id='bk')
        bk = getattr(self.portal, 'bk')
        bk.invokeFactory('BKTransaction', id='trx1',
                         bk_transaction_date = DateTime(2009, 2, 23),
                         bk_transaction_type = 'Expense',
                         bk_transaction_category = 'Lunch')
        self.trx = getattr(bk, 'trx1')
        bk.invokeFactory('BKTransaction', id='trx2',
                         bk_transaction_date = DateTime(2008, 2, 23),
                         bk_transaction_type = 'Expense',
                         bk_transaction_category = 'Lunch')
 
    def testFixture(self):
        # make sure the conent is created after setup.
        self.assertEquals(self.trx.transactionDate(), DateTime(2009, 2, 23))
        self.assertEquals(self.trx.transactionType(), 'Expense')
        self.assertEquals(self.trx.transactionCategory(), 'Lunch')

    def testBasicSearch(self):
        self.assertEquals(len(self.catalog(transactionDate=DateTime(2009, 2, 23))), 1)
        self.assertEquals(len(self.catalog(transactionDate=DateTime(2009, 2, 22))), 0)
        self.assertEquals(len(self.catalog(transactionDate=DateTime(2008, 2, 23))), 1)

        self.assertEquals(len(self.catalog(transactionType='Expense')), 2)
        self.assertEquals(len(self.catalog(transactionType='Ex')), 0)
        self.assertEquals(len(self.catalog(transactionCategory='Lunch')), 2)
        # index is case sensitive
        self.assertEquals(len(self.catalog(transactionCategory='lunch')), 0)
        self.assertEquals(len(self.catalog(transactionCategory='Gas')), 0)

    def testTrxDateRangeSearch(self):
        # testing search by date range.
        year2009 = {'query' : [DateTime(2009,1,1,0,0,0), DateTime(2009,12,31,23,59,59)],
                    'range' : 'min:max'
                   }
        m200901 = {'query' : [DateTime(2009,1,1,0,0,0), DateTime(2009,1,31,23,59,59)],
                   'range' : 'min:max'
                  }
        m200902 = {'query' : [DateTime(2009,2,1,0,0,0), DateTime(2009,2,28,23,59,59)],
                   'range' : 'min:max'
                  }
        self.assertEquals(len(self.catalog(transactionDate=year2009)), 1)
        self.assertEquals(len(self.catalog(transactionDate=m200901)), 0)
        self.assertEquals(len(self.catalog(transactionDate=m200902)), 1)

    def testAdvanceSearch(self):
        # testing combined search
        year2009 = {'query' : [DateTime(2009,1,1,0,0,0), DateTime(2009,12,31,23,59,59)],
                    'range' : 'min:max'
                   }
        self.assertEquals(len(self.catalog(transactionDate=year2009,
                                           transactionType='Expense'))
                          , 1)

    def testSearchInterface(self):
        # testing the BKFolder's searching interface.
        bk = getattr(self.portal, 'bk')
        query = {
            'transactionType' : 'Expense'
            }
        self.assertEquals(len(bk.searchTransactions(query)), 2)
        year2009 = {'query' : [DateTime(2009,1,1,0,0,0), DateTime(2009,12,31,23,59,59)],
                    'range' : 'min:max'
                   }
        query = {
            'transactionDate' : year2009,
            'transactionType' : 'Expense'
            }
        self.assertEquals(len(bk.searchTransactions(query)), 1)

        query = {
            'transactionDate' : year2009,
            'transactionType' : 'Expense',
            'transactionCategory' : 'Lunch'
            }
        self.assertEquals(len(bk.searchTransactions(query)), 1)

        query = {
            'transactionDate' : year2009,
            'transactionType' : 'Expense',
            'transactionCategory' : 'Gas'
            }
        self.assertEquals(len(bk.searchTransactions(query)), 0)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCatalogSetup))
    suite.addTest(unittest.makeSuite(TestSearchIndexing))
    return suite
