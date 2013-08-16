"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

class Sign(object):
    """ Sign of convex optimization expressions. """
    POSITIVE_KEY = 'POSITIVE'
    NEGATIVE_KEY = 'NEGATIVE'
    UNKNOWN_KEY = 'UNKNOWN'
    ZERO_KEY = 'ZERO'

    # List of valid sign strings.
    SIGN_STRINGS = [POSITIVE_KEY, NEGATIVE_KEY, UNKNOWN_KEY, ZERO_KEY]
    
    def __init__(self,sign_str):
        sign_str = sign_str.upper()
        if sign_str in Sign.SIGN_STRINGS:
            self.sign_str = sign_str
        else:
            raise Exception("No such sign %s exists." % str(sign_str))

    # Converts a number to a sign.
    @staticmethod
    def val_to_sign(val):
        if val > 0:
            return Sign.POSITIVE
        elif val == 0:
            return Sign.ZERO
        else:
            return Sign.NEGATIVE

    # Zero is both positive and negative.
    def is_zero(self):
        return self == Sign.ZERO

    def is_positive(self):
        return self.is_zero() or self == Sign.POSITIVE

    def is_negative(self):
        return self.is_zero() or self == Sign.NEGATIVE
    
    # Arithmetic operators
    """
    Handles logic of sign addition:
        ZERO + ANYTHING = ANYTHING
        UNKNOWN + ANYTHING = UNKNOWN
        POSITIVE + NEGATIVE = UNKNOWN
        SAME + SAME = SAME
    """
    def __add__(self, other):
        if self.is_zero():
            return other
        elif self == Sign.POSITIVE and other.is_positive():
            return self
        elif self == Sign.NEGATIVE and other.is_negative():
            return self
        else:
            return Sign.UNKNOWN
    
    def __sub__(self, other):
        return self + -other
       
    def __mul__(self, other):
        if self == Sign.ZERO or other == Sign.ZERO:
            return Sign.ZERO
        elif self == Sign.UNKNOWN or other == Sign.UNKNOWN:
            return Sign.UNKNOWN
        elif self != other:
            return Sign.NEGATIVE
        else:
            return Sign.POSITIVE
        
    def __neg__(self):
        return self * Sign.NEGATIVE
    
    # Boolean operators
    def __eq__(self,other):
        return self.sign_str == other.sign_str

    # To string methods.
    def __repr__(self):
        return "Sign('%s')" % self.sign_str
    
    def __str__(self):
        return self.sign_str

# Class constants for all sign types.
Sign.POSITIVE = Sign(Sign.POSITIVE_KEY)
Sign.NEGATIVE = Sign(Sign.NEGATIVE_KEY)
Sign.ZERO = Sign(Sign.ZERO_KEY)
Sign.UNKNOWN = Sign(Sign.UNKNOWN_KEY)