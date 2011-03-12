
# __init__.py

__doc__ = """initializing the whole package"""
__docformat__ = 'plaintext'

from Products.Archetypes.public import process_types
from Products.Archetypes.public import listTypes
from Products.CMFCore.utils import ContentInit

from permissions import initialize as initialize_permissions
from config import PROJECTNAME

#
def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    # import types from this project to register them.
    import content

    # get content type list, content constructor list, and file type
    # information (fti) list.
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    # initializing permissions.
    permissions = initialize_permissions()

    # make 'content type' and 'consturctor' tuples list to use easly
    # at next process.
    allTypes = zip(content_types, constructors)

    # Registration per content type.
    for atype, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, atype.archetype_name)
        # Call CMFCore.utils.ContentInit to register content types.
        ContentInit(
            # Name that display in ADD drop-down menu on ZMI is 
            # specified. This is used as meta_type in internal. However, 
            # there is no relation to meta_type set in each contents type 
            # implementation class.
            kind,

            # The tupple of the contents type implementation class object 
            # that can be added with kind(meta_type) is specified. The 
            # menu panel to select it is displayed to add the object of 
            # which contents type with ZMI when the plural is specified 
            # when the addition is executed.
            content_types = (atype,),

            # Permission information on the contents type that tries to 
            # be registered now is specified among information acquired 
            # with initialize_permissions().
            permission = permissions[atype.portal_type],

            # The constructor executed when the object is added is 
            # specified. Constructors of the same number as the number of 
            # elements set to the content_types argument are necessary.
            extra_constructors = (constructor,),

            # FileTypeInformation is specified.
            fti = ftis,

            # The initialization execution function of ContentInit is 
            # called. After necessary processing is done as CMFCore, the 
            # product registration function to Zope is called.
            ).initialize(context)
