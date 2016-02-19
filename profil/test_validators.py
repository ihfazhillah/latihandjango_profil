import re
from django.core.exceptions import ValidationError
from django.test import TestCase

from .validators import (numeric_validation,)


class CustomValidatorTest(TestCase):


    def test_numeric_phone_number_validation_without_numeric(self):
        self.assertRaises(ValidationError, 
                          numeric_validation, 
                          'ini bukan numeric')

    

