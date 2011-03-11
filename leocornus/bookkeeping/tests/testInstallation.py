# testInstallation.py

"""
testing installation of Bookkeeping
"""

import unittest

from Products.CMFCore.utils import getToolByName

from base import BookkeepingTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class InstallationTestCase(BookkeepingTestCase):

    """
    Try to verify that everything is ready after installation.  We suppose
    install the whole package on Zope application level in the base test case
    class, and then install the product in any Plone site by using the
    QuickInstaller tool.
    """

    # verify that we could find the leocornus bookkeeping product from Plone
    # QuickInstaller.
    def testInstall(self):

        installer = getToolByName(self.portal, 'portal_quickinstaller')
        # make sure bookkeeping is available for quick installer.
        self.assertTrue(installer.isProductAvailable('leocornus.bookkeeping'))

        # install bookkeeping...

        # check/verify after installation.

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstallationTestCase))
    return suite
