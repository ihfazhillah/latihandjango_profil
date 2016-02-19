import re
from django.core.exceptions import ValidationError

def numeric_validation(value):
    """
    Validasi string harus numeric, bila value bukan
    string, maka akan mengembalikan validation error
    """
    if not re.match(pattern='[\d+]', string=value):
        raise ValidationError("'{}' bukan numeric.".format(value))

def tipe_validator(value):
    """
    Validasi pilihan tipe, harus antara 'p' yang berarti primary
    atau 's' yaitu sekunder.
    """
    if value not in ('p', 's'):
        raise ValidationError("{} bukan pilihan tipe yang valid".format(value))

