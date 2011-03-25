
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
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes product
from Products.ATContentTypes.interface.folder import IATBTreeFolder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATBTreeFolder
from Products.ATContentTypes.atct import ATBTreeFolderSchema

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

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
            accessor = 'transactionTypes',
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
            accessor = 'transactionCategories',
            searchable = False,
            required = True,
            default = ('Income:ConsultingIncome', 'Income:ServiceIncome', 
                'Expense:Gas', 'Expense:Parking', 'Expense:Lunch',
                'Expense:Internet', 'Expense:OfficeSupply'
                ),
            widget = LinesWidget(
                label = 'Transaction Categories',
                description = 'Please specify the transaction categories, one per line',
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

    __implements__ = (ATBTreeFolder.__implements__)

    implements(IBKFolder, IATBTreeFolder, OFSIOrderedContainer)

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

    security.declareProtected(permissions.View, 'transactionTypes')
    def transactionTypes(self):
        # accessor for bk_transaction_types.
        trxTypes = self.getField('bk_transaction_types').get(self)
        return trxTypes

    security.declareProtected(permissions.View, 'transactionCategories')
    def transactionCategories(self):
        # accessor for bk_transaction_types.
        categories = self.getField('bk_transaction_categories').get(self)
        return categories

    security.declarePublic('getCategories')
    def getCategories(self, transactionType):
        """
        return categories as a list for the given transaction type.
        """

        categories = []
        for each in self.transactionCategories():
            try:
                tType, category = each.split(':')
            except ValueError:
                # this category has business percentage specified.
                tType, category, bp = each.split(':')

            if (tType == transactionType):
                categories.append(category) 

        return categories

    security.declareProtected(permissions.View, 'getCategoryBuzPercent')
    def getCategoryBuzPercent(self, transactionType, category):
        """
        return the business percentage for the given category.
        default is 100
        """

        theCategory = transactionType + ':' + category
        if theCategory in self.transactionCategories():
            # business percentage not specified, return default.
            bp = 100
        else:
            for each in self.transactionCategories():
                if each.startswith(theCategory + ':'):
                    a, bp = each.split(theCategory + ':')

        return int(bp)

    security.declarePublic('vocabularyTrxTypes')
    def vocabularyTrxTypes(self):
        """
        returns all transaction types as display list.
        """

        retList = []
        for aType in self.transactionTypes():
            retList.append((aType, aType))

        return DisplayList(retList)

    security.declarePublic(permissions.View, 'getBaseUrl')
    def getBaseUrl(self):
        """
        return the url for this folder.
        """
        return '/'.join(self.getPhysicalPath())

    security.declarePublic(permissions.View, 'searchTransactions')
    def searchTransactions(self, criteria=None, **kwargs):
        """
        returns the catalog search result based on the provided criteria
        or kwargs.
        """

        if criteria is None:
            criteria = kwargs
        else:
            criteria = dict(criteria)

        availableCriteria = {'id' : 'getId',
                             'portal_type' : 'portal_type',
                             'transactionDate' : 'transactionDate',
                             'transactionType' : 'transactionType',
                             'transactionCategory' : 'transactionCategory',
                             'sort_on' : 'sort_on',
                             'sort_order' : 'sort_order',
                             'sort_limit' : 'sort_limit',
                             }

        query = {}
        query['path'] = '/'.join(self.getPhysicalPath())
        query['portal_type'] = 'BKTransaction'

        for k, v in availableCriteria.items():
            if k in criteria:
                query[v] = criteria[k]
            elif v in criteria:
                query[v] = criteria[v]

        catalog = getToolByName(self, 'portal_catalog')

        return catalog.searchResults(query)

# register to the Plone add-on product.
registerType(BKFolder, PROJECTNAME)
