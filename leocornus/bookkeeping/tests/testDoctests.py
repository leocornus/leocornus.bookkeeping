
# testDoctests.py

"""
This is the entry point to execute doctest cases in Python source code file.
it is following the way that how CMFPlone is running doctest cases...
"""

from unittest import TestSuite
from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite, DocFileSuite

from Products.CMFPlone.tests import PloneTestCase
from Testing.ZopeTestCase import ZopeDocTestSuite

from leocornus.bookkeeping.tests.base import BookkeepingFunctionalTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def test_suite():
    suites = (
        DocTestSuite('leocornus.bookkeeping.browser.base'),
        ZopeDocTestSuite('leocornus.bookkeeping.browser.bkviews',
                         test_class=BookkeepingFunctionalTestCase),
        #ZopeDocTestSuite('Products.CMFPlone.PloneTool',
        #                 test_class=PloneTestCase.FunctionalTestCase),
        #DocTestSuite('Products.CMFPlone.TranslationServiceTool'),
        #DocTestSuite('Products.CMFPlone.utils'),
        #DocTestSuite('Products.CMFPlone.workflow'),
        )

    return TestSuite(suites)
