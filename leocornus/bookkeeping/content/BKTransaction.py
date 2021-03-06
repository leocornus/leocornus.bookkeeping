
# BKTransaction.py

__doc__ = """The document to save transaction record"""
__docformat__ = 'plaintext'

import logging
import transaction

from zope.interface import implements

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import FixedPointField
from Products.Archetypes.public import DecimalWidget
from Products.Archetypes.public import ComputedField
from Products.Archetypes.public import ComputedWidget
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes product
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.CMFCore import permissions

from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

from leocornus.bookkeeping.config import PROJECTNAME
from leocornus.bookkeeping.interface import IBKTransaction

__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

# define a PPMProject as a folder in plone site.
BKTransactionSchema = ATContentTypeSchema.copy() + Schema((

        # transaction date.
        DateTimeField(
            'bk_transaction_date',
            accessor = 'transactionDate',
            searchable = False,
            required = True,
            widget = CalendarWidget(
                label = 'Transaction Date',
                description = 'Please select the transaction date.',
                # available format: flex, select, radio
                format = '%Y-%m-%d',
                show_hm = False,
                starting_year = 2010,
                ),
            ),

        # transaction type.
        StringField(
            'bk_transaction_type',
            accessor = 'transactionType',
            searchable = False,
            required = True,
            default = 'Expense',
            vocabulary = 'vocabularyTrxTypes',
            widget = MasterSelectWidget(
                label = 'Transaction Type',
                description = 'Please select the transaction type.',
                # available format: flex, select, radio
                format = 'select',
                slave_fields = (
                    {'name' : 'bk_transaction_category',
                     'action' : 'vocabulary',
                     'vocab_method' : 'vocabularyTrxCategories',
                     'control_param' : 'masterType',
                    },
                    ),
                ),
            ),

        # transaction type.
        StringField(
            'bk_transaction_category',
            accessor = 'transactionCategory',
            searchable = False,
            required = True,
            vocabulary = 'vocabularyTrxCategories',
            widget = SelectionWidget(
                label = 'Transaction Category',
                description = 'Please select the transaction category.',
                # available format: flex, select, radio
                format = 'select',
                ),
            ),

        # transaction subtotal.
        FixedPointField(
            'bk_transaction_subtotal',
            searchable = False,
            required = True,
            # the type for default value is string.
            default = '0.00',
            precision = 2,
            widget = DecimalWidget(
                label = 'Transaction Subtotal',
                description = 'Please input the transaction subtotal.',
                size = 16,
                thousands_commas = True,
                dollars_and_cents = True,
                ),
            ),

        # transaction GST/HST
        FixedPointField(
            'bk_transaction_gst',
            searchable = False,
            required = False,
            default = '0.00',
            precision = 2,
            widget = DecimalWidget(
                label = 'Transaction GST/HST',
                description = 'Please input the transaction GST/HST.',
                size = 8,
                thousands_commas = True,
                dollars_and_cents = True,
                ),
            ),
        
        # transaction PST
        FixedPointField(
            'bk_transaction_pst',
            searchable = False,
            required = False,
            default = '0.00',
            precision = 2,
            widget = DecimalWidget(
                label = 'Transaction PST',
                description = 'Please input the transaction PST. (NOT available after July, 2010)',
                size = 8,
                thousands_commas = True,
                dollars_and_cents = True,
                ),
            ),

        # transaction total
        ComputedField(
            'bk_transaction_total',
            searchable = False,
            required = False,
            expression = 'context.transactionTotal()',
            widget = ComputedWidget(
                label = 'Transaction Total',
                description = 'Please input the transaction PST. (NOT available after July, 2010)',
                ),
            ),

        # TODO: image field for the receipt / invoice
        )
    )

finalizeATCTSchema(BKTransactionSchema)

# move around the fields.

# define the content type class.
class BKTransaction(ATCTContent):
    """
    a transaction record.
    """

    schema = BKTransactionSchema

    __implements__ = (ATCTContent.__implements__)

    implements(IBKTransaction)

    # type, name
    meta_type = 'BKTransaction'
    portal_type = 'BKTransaction'
    archetype_name = 'BKTransaction'

    _at_rename_after_creation = True

    bk_id_prefix = 'tx'

    # preparing class security info for methods.
    security = ClassSecurityInfo()

    # override renameAfterCreation to generate the unique id for
    # contact. This method is defined in Archetypes.BaseObject.py.
    # The method getNextUniqueId should be defined in the root content of
    # BKFolder
    def _renameAfterCreation(self, check_auto_id=False):

        # Can't rename without a subtransaction commit when using
        # portal_factory!
        transaction.savepoint(optimistic=True)
        newId = str(self.getNextUniqueId())
        self.log.info('the next value for leocornus bookkeeping sequence: %s',
                      newId)
        self.setId(self.bk_id_prefix + newId)

    security.declarePublic('vocabularyTrxTypes')
    def vocabularyTrxCategories(self, masterType=None):
        """
        returns all transaction types as display list.
        """

        categories = (masterType == None and
                      self.getCategories(self.transactionType())
                      or self.getCategories(masterType))
        retList = []
        for aType in categories:
            retList.append((aType, aType))

        return DisplayList(retList)

    security.declarePublic('transactionTotal')
    def transactionTotal(self):
        """
        calculate the total for transaction total.
        """
        return self.subtotal() + self.gst() + self.pst()

    security.declarePublic('pst')
    def pst(self):
        """
        return the pst fixed point as a float.
        """
        return float(self.getBk_transaction_pst())

    security.declarePublic('gst')
    def gst(self):
        """
        return the gst/hst for this transaction.
        """
        return float(self.getBk_transaction_gst())

    security.declarePublic('subtotal')
    def subtotal(self):
        """
        return the subtotal for this transaction.
        """
        return float(self.getBk_transaction_subtotal())

    security.declareProtected(permissions.View, 'transactionDate')
    def transactionDate(self):
        """
        accessor for field transaction date, return as DateTime
        """
        txDate = self.getField('bk_transaction_date').get(self)
        return txDate

    security.declareProtected(permissions.View, 'transactionType')
    def transactionType(self):
        """
        accessor for field transaction date, return as DateTime
        """
        trxType = self.getField('bk_transaction_type').get(self)
        return trxType

    security.declareProtected(permissions.View, 'transactionCategory')
    def transactionCategory(self):
        """
        accessor for field transaction date, return as DateTime
        """
        category = self.getField('bk_transaction_category').get(self)
        return category

# register the content type.
registerType(BKTransaction, PROJECTNAME)
