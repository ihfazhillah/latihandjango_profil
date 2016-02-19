import re
from django.core.exceptions import ValidationError

def numeric_validation(value):
    """
    Validasi string harus numeric, bila value bukan
    string, maka akan mengembalikan validation error
    """
    if not re.match(pattern='[\d+]', string=value):
        raise ValidationError("'{}' bukan numeric.".format(value), 
                              code='invalid input')


