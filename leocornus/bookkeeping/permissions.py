# permission.py

__doc__ = """set up permissions for new content types of bookkeeping."""
__docformat__ = 'plaintext'

import logging

from AccessControl import ModuleSecurityInfo
from AccessControl import Permissions

# we require Plone 3.x using the new class.
from Products.CMFCore import permissions as CMFCorePermissions
from Products.Archetypes.public import listTypes

from leocornus.bookkeeping.config import PROJECTNAME

__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

log = logging.getLogger('Leocornus Bookkeeping permissions')

# The setting of the permission and the roll is made. This function is 
# called from __ init__.py.
def initialize():
    # Container that stores permission according to contents type finally 
    # output.
    permissions = {}

    # The list of the contents type registered to Archetype is acquired.
    types = listTypes(PROJECTNAME)

    # The permission setting of each contents type is added.
    for atype in  types:
        # The permission name displayed in the permission tab of ZMI is 
        # made.
        permission = "%s: Add %s" % (PROJECTNAME, atype['portal_type'])
        log.debug("Adding permission - > " + permission)

        # The permission made for the dictionary of the contents type is 
        # preserved.
        permissions[atype['portal_type']] = permission

        # The permission name and the access permit at each roll 
        # corresponding to the permission name is set to CMFCore.
        CMFCorePermissions.setDefaultRoles(permission, ('Manager','Owner'))

    return permissions
