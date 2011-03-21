
# testFunctionalDoctest.py

"""
The first step to use doctest for unit testing.
"""

import unittest
import doctest

from Testing import ZopeTestCase

from base import BookkeepingFunctionalTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def test_suite():

    return unittest.TestSuite([

        ZopeTestCase.ZopeDocFileSuite('README.txt',
                                      package='leocornus.bookkeeping',
                                      test_class=BookkeepingFunctionalTestCase),

        ZopeTestCase.ZopeDocFileSuite('tests/simpleTry.txt',
                                      package='leocornus.bookkeeping',
                                      test_class=BookkeepingFunctionalTestCase),

        ZopeTestCase.ZopeDocFileSuite('tests/testBookkeepingViews.txt',
                                      package='leocornus.bookkeeping',
                                      test_class=BookkeepingFunctionalTestCase),
        # other text files.
        ])
