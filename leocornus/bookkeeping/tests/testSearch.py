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

    def testFixture(self):
        # make sure the conent is created after setup.
        self.assertEquals(self.trx.transactionDate(), DateTime(2009, 2, 23))
        self.assertEquals(self.trx.transactionType(), 'Expense')
        self.assertEquals(self.trx.transactionCategory(), 'Lunch')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCatalogSetup))
    suite.addTest(unittest.makeSuite(TestSearchIndexing))
    return suite
