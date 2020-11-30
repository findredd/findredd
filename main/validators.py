from datetime import date

from django.utils.deconstruct import deconstructible

from django.utils.translation import ugettext_lazy as _

from django.core.validators import BaseValidator


def calculate_age(born):
    today = date.today()
    return today.year - born.year - \
           ((today.month, today.day) < (born.month, born.day))


@deconstructible
class MinAgeValidator(BaseValidator):
    compare = lambda self, a, b: calculate_age(a) < b
    message = _("Age should be at least %(limit_value)d.")
    code = 'min_age'
