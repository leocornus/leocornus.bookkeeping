# testInstallation.py

"""
testing installation of Bookkeeping
"""

import unittest

from Products.PloneTestCase import PloneTestCase

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

    def afterSetUp(self):
        # create a separate plone site to test the installation.
        self.newsite = getattr(self.app, 'emptysite')
        self.loginAsPortalOwner()

    # verify that we could find the leocornus bookkeeping product from Plone
    # QuickInstaller.
    def testInstall(self):

        installer = getToolByName(self.newsite, 'portal_quickinstaller')
        # make sure bookkeeping is available for quick installer.
        self.assertTrue(installer.isProductAvailable('leocornus.bookkeeping'))

        # install bookkeeping...

        # install by import the default profile.
        setup_tool = getattr(self.newsite, 'portal_setup')
        setup_tool.\
            runAllImportStepsFromProfile('profile-%s' % \
                                         'leocornus.bookkeeping:default')
        types_tool = getattr(self.newsite, 'portal_types')
        types = types_tool.listContentTypes()
        self.assertTrue('BKFolder' in  types)
        self.assertTrue('BKTransaction' in types)

        # after install, we should be able to crate BKFolder.
        id = self.newsite.invokeFactory('BKFolder', 'bk1')
        self.assertEquals(id, 'bk1')

        # get the bk folder
        bk = getattr(self.newsite, id)
        # create a transaction record.
        id = bk.invokeFactory('BKTransaction', 'tx1', None,
                              bk_transaction_subtotal = '12.23',
                              bk_transaction_gst = '0.451',
                              bk_transaction_pst = '0.23')
        self.assertEquals(id, 'tx1')
        tx = getattr(bk, id)
        self.assertEquals(tx.transactionTotal(), 12.23 + 0.45 + 0.23)
        self.assertEquals(tx.getBk_transaction_total(), 12.23 + 0.45 + 0.23)
        self.assertEquals(tx.pst(), 0.23)

        # check/verify after installation.

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstallationTestCase))
    return suite
