import re
from django.core.exceptions import ValidationError
from django.test import TestCase

from .validators import (numeric_validation,
                         tipe_validator)


class CustomValidatorTest(TestCase):


    def test_numeric_phone_number_validation_without_numeric(self):
        self.assertRaises(ValidationError, 
                          numeric_validation, 
                          'ini bukan numeric')

    def test_tipe_validator_p_or_s(self):
        self.assertRaises(ValidationError,
                          tipe_validator,
                          "g")

    def test_tipe_validator_with_numeric(self):
        self.assertRaises(ValidationError,
                          tipe_validator,
                          '1233')

