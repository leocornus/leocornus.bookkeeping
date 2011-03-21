
# base.py

"""
The base unit test cases for leocornus bookkeeping
"""

from Testing import ZopeTestCase

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

import leocornus.bookkeeping

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

@onsetup
def setup_product():
    """
    we need install our product so the testing zope server know it.
    """

    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', leocornus.bookkeeping)
    ZopeTestCase.installPackage('leocornus.bookkeeping')

setup_product()
# we need a Plone site for some of the module.
PloneTestCase.setupPloneSite(products=['leocornus.bookkeeping', 
                                       'Products.MasterSelectWidget'])

# now we will have Zope application server and a Plone site set up.
# Zope application server can be accessed by using self.app
# the plone site can be accessed by using self.portal.

# we could set up more plone site just give different id.
# try to setup one more plone site for testing.
# NOTICE: looks like we have to do it here
PloneTestCase.setupPloneSite(id='emptysite')

class BookkeepingTestUtils(object):
    """
    Some facility functions for testing.
    """


# base test case for our product.
class BookkeepingTestCase(PloneTestCase.PloneTestCase, BookkeepingTestUtils):
    """
    General steps for all test cases.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()
        self.acl_users = self.portal.acl_users

class BookkeepingFunctionalTestCase(PloneTestCase.FunctionalTestCase,
                                    BookkeepingTestUtils):
    """
    base test case class for functional test case.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()
