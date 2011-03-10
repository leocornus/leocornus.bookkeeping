# Install.py

from Products.CMFCore.utils import getToolByName

# specify install and uninstall profiles for the product.
def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-leocornus.bookkeeping:default')
    return "Ran all import steps."

def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-leocornus.bookkeeping:uninstall')
    return "Ran all uninstall steps."
