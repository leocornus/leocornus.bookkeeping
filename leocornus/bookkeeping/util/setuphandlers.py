
# setuphandlers.py

"""
miscellaneous set up steps that are not handled by GS import/export
handlers.
"""

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def importVarious(context):
    """
    empty for now, reserve for future use...
    """

    if context.readDataFile('leocornus.bookkeeping_various.txt') is None:
        # we have nothing to do.
        return
