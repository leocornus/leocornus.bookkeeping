
# BKFolder.py

__doc__ = """The base folder for bookkeeping"""
__docformat__ = 'plaintext'

import logging

from zope.interface import implements

from AccessControl import ClassSecurityInfo
# from ATContentTypes product
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATBTreeFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.configuration import zconf

from leocornus.bookkeeping.config import PROJECTNAME
from leocornus.bookkeeping.interface import IBKFolder

__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

# define the class
class BKFolder(ATBTreeFolder):
    """
    This is the base folder for all bookkeeping transactions: income and
    expense.
    """

    schema = BKFolderSchema

    __implements__ = (ATBTreeFolder.__implements__, )

    implements(IBKFolder)

    # type, name
    meta_type = 'LeocornBKFolder'
    portal_type = 'LeocornBKFolder'
    archetype_name = 'LeocornBKFolder'

    _at_rename_after_creation = True

    # the logger.
    log = logging.getLogger("Leocornus Bookkeeping")

    # preparing class security info for methods.
    security = ClassSecurityInfo()

    security.declarePublic('getNextUniqueId')
    def getNextUniqueId(self):
        """
        Return the next value from the unique sequence and than update the
        sequence itself by increase 1
        """

        newId = self.xppm_unique_sequence + 1
        self.setXppm_unique_sequence(newId)
        return newId

# register to the Plone add-on product.
registerType(BKFolder, PROJECTNAME)

# define a PPMProject as a folder in plone site.
BKFolderSchema = ATBTreeFolderSchema.copy() + Schema((

        # modules
        LinesField(
            'bk_transaction_types',
            searchable = False,
            required = True,
            default = ('Expense', 'Income'),
            widget = LinesWidget(
                label = 'Transaction Types',
                description = 'Please specify the transaction types, one per line',
                cols = 40,
                ),
            ),

        # the unique sequence will serve
        IntegerField(
            'bk_unique_sequence',
            default = 0,
            # hide for view mode.
            widget = IntegerWidget(
                label = 'Unique Sequence',
                description = 'This sequence will generate unique ids for all artifacts in this folder.',
                ),
            ),
        )
    )

finalizeATCTSchema(BKFolderSchema)

# customizing the schema here, set visible of some fields, location of
# some fields.
BKFolderSchema.changeSchemataForField('bk_unique_sequence', 'settings')
