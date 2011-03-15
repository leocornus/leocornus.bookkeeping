
# bookkeeping.py

"""
define the interfaces about bookkeeping.
"""

from zope.interface import Interface

__author__ = "Sean Chen"
__email__ = 'sean.chen@leocorn.com'
__docformat__ = 'plaintext'

# the bookkeeping folder interface
class IBKFolder(Interface):
    """
    defines the interfaces for a bookkeeping folder, which will store all
    transactions.
    """
    pass

# the transaction interface.
class IBKTransaction(Interface):
    """
    defines the interfaces for a transaction.
    """
    pass

# the category interface
class IBKCategoryOperator(Interface):
    """
    defines the interfaces for a transaction category.
    """
    def getCategories(transactionType):
        """
        return all categories for the given transaction type as a list.
        """

    def addCategory(transactionType, category):
        """
        add a new category for the transaction type.
        """  
