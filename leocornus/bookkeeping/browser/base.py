
# base.py

"""
The base view class for all browser views in bookkeeping.
"""

import locale
from datetime import datetime

from Acquisition import aq_inner
from DateTime import DateTime

from Products.Five.browser import BrowserView

from leocornus.bookkeeping.util.catalog import getYearQuery

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class BaseView(BrowserView):
    """
    providing some utilities for browser view.
    """

    def monetary(self, number, place=2):
        """
        format the given number to monetary format

        a bit testing.
        >>> view = BaseView('context', 'request')
        >>> view.monetary(12345.56)
        '12,345.56'
        >>> view.monetary(123.45)
        '123.45'
        """

        # set to locale to en_CA for monetary.
        #locale.setlocale(locale.LC_MONETARY, 'en_CA.UTF-8')
        #return locale.format('%.*f', (place, number), True)
        return self.splitThousands(number)

    def splitThousands(self, s, tSep=',', dSep='.'):
        """
        Splits a general float on thousands. GIGO on general input

        let's write some doctest,

        First we need a view instance, reference the doctest in 
        file zope/publisher/browser.py
        >>> view = BaseView('context', 'request')
        >>> view.splitThousands(12345.67)
        '12,345.67'

        >>> view.splitThousands(23.45)
        '23.45'

        >>> view.splitThousands(0.56)
        '0.56'

        let's try some nagtive number:
        >>> view.splitThousands(-123467.78)
        '-123,467.78'
        >>> view.splitThousands(-1.23)
        '-1.23'

        some large number
        >>> view.splitThousands(-1234567890.12)
        '-1,234,567,890.12'

        """

        if s == None:
            return 0
        if not isinstance( s, str ):
            s = str( s )
    
        cnt=0
        numChars=dSep+'0123456789'
        ls=len(s)
        while cnt < ls and s[cnt] not in numChars: cnt += 1
    
        lhs = s[ 0:cnt ]
        s = s[ cnt: ]
        if dSep == '':
            cnt = -1
        else:
            cnt = s.rfind( dSep )
        if cnt > 0:
            rhs = dSep + s[ cnt+1: ]
            s = s[ :cnt ]
        else:
            rhs = ''
    
        splt=''
        while s != '':
            splt= s[ -3: ] + tSep + splt
            s = s[ :-3 ]
    
        return lhs + splt[ :-1 ] + rhs
