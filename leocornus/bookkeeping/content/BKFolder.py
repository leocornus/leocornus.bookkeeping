
# BKFolder.py

__doc__ = """The base folder for bookkeeping"""
__docformat__ = 'plaintext'

import logging

from zope.interface import implements

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import registerType
# from ATContentTypes product
from Products.ATContentTypes.interface.folder import IATFolder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATBTreeFolder
from Products.ATContentTypes.atct import ATBTreeFolderSchema

from OFS.interfaces import IOrderedContainer as OFSIOrderedContainer

from leocornus.bookkeeping.config import PROJECTNAME
from leocornus.bookkeeping.interface import IBKFolder

__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

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

        # this is a field to save the transaction categories.
        # TODO: this field should be invisable!
        LinesField(
            'bk_transaction_categories',
            searchable = False,
            required = True,
            default = ('Income:ConsultingIncome', 'Income:ServiceIncome', 
                'Expense:Gas', 'Expense:Parking', 'Expense:Lunch',
                'Expense:Internet', 'Expense:OfficeSupply'
                ),
            widget = LinesWidget(
                label = 'Transaction Types',
                description = 'Please specify the transaction types, one per line',
                cols = 40,
                ),
            ),
        )
    )

finalizeATCTSchema(BKFolderSchema)

# customizing the schema here, set visible of some fields, location of
# some fields.
BKFolderSchema.changeSchemataForField('bk_unique_sequence', 'settings')

# define the class
class BKFolder(ATBTreeFolder):
    """
    This is the base folder for all bookkeeping transactions: income and
    expense.
    """

    schema = BKFolderSchema

    __implements__ = (ATBTreeFolder.__implements__, 
        ATFolder.__implements__)

    implements(IBKFolder, IATFolder, OFSIOrderedContainer)

    # type, name
    meta_type = 'BKFolder'
    portal_type = 'BKFolder'
    archetype_name = 'BKFolder'

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

        newId = self.bk_unique_sequence + 1
        self.setBk_unique_sequence(newId)
        return newId

    security.declarePublic('getCategories')
    def getCategories(self, transactionType):
        """
        return categories as a list for the given transaction type.
        """

        categories = []
        for each in self.bk_transaction_categories:
            tType, category = each.split(':')
            if (tType == transactionType):
                categories.append(category) 

        return categories

# register to the Plone add-on product.
registerType(BKFolder, PROJECTNAME)
