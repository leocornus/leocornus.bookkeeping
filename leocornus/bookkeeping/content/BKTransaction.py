
# BKTransaction.py

__doc__ = """The document to save transaction record"""
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
from leocornus.bookkeeping.interface import IBKTransaction

__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

# define a PPMProject as a folder in plone site.
BKTransactionSchema = 
