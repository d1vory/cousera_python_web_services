import requests
from decimal import Decimal
from currency import convert

if __name__ == '__main__':
    correct = Decimal('3754.8057')
    result = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)
    if result == correct:
        print("Correct")
    else:
        print("Incorrect: %s != %s" % (result, correct))
