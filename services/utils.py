from decimal import Decimal


def truncate_number(number, digits):
    split_number = str(number).split('.')
    if len(split_number) == 1:
        return Decimal(str(split_number[0]))
    return Decimal(str(split_number[0] + '.' + split_number[1][:digits]))
