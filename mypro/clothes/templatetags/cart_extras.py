from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        # Convert to Decimal with string conversion to avoid float precision issues
        if not isinstance(value, Decimal):
            value = Decimal(str(float(value)))
        if not isinstance(arg, Decimal):
            arg = Decimal(str(float(arg)))
        return value * arg
    except (ValueError, TypeError, InvalidOperation, ArithmeticError) as e:
        print(f"Error in multiply filter: {e}, value: {value}, arg: {arg}")
        return Decimal('0') 