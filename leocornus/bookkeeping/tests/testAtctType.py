# testAtctType.py

"""
we will do the basic unit test for the new content types based on
ATContentTypes.
"""

import unittest

from Products.ATContentTypes.tests.atcttestcase import ATCTTypeTestCase
from Products.ATContentTypes.tests.test_atfolder import TestSiteATFolder
from Products.ATContentTypes.tests.test_atdocument import TestSiteATDocument

from leocornus.bookkeeping.content.BKFolder import BKFolder
from leocornus.bookkeeping.content.BKTransaction import BKTransaction

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# test cases list
tests = []

class TestBKFolder(TestSiteATFolder):
    """
    Testing basics about the AT Content Types within this product.
    """

    klass = BKFolder
    portal_type = "BKFolder"
    # the title in the types/BKFolder.xml file.
    title = 'Bookkeeping Folder'
    meta_type = 'BKFolder'
    icon = 'BKFolder_icon.gif'

tests.append(TestBKFolder)

class TestBKTransaction(ATCTTypeTestCase):
    """
    Testing basics about the AT Content Types within this product.
    """

    klass = BKTransaction
    portal_type = "BKTransaction"
    # the title in the types/BKFolder.xml file.
    title = 'Bookkeeping Transaction'
    meta_type = 'BKTransaction'
    icon = 'BKTransaction_icon.jpeg'

tests.append(TestBKTransaction)

# making test suite
def test_suite():

    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    return suite
