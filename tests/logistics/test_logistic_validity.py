import pytest 
from bol.Product import Product
from bol.Storage import Storage
from bol.LogisticsEstimator import LogisticsEstimator
from bol.LogisticsAttrValidator import LogisticsAttrValidator


### Testing Attr Validation and Logistics Validation ###

test_data = [
    # Valid Cases
    (Product(1, 1, 1, 1), True, True),
    (Product(25.5, 16.5, 3, 1), True, True),
    (Product(37.5, 26, 3, 2), True, True),
    (Product(37.5, 26, 5, 5), True, True),
    (Product(45, 30, 8, 5), True, True),
    (Product(55, 35, 20, 8), True, True),
    (Product(72, 30, 30, 15), True, True),
    
    # Borderline cases - just within limit
    (Product(25.49, 16.49, 2.99, 0.99), True, True),
    (Product(37.49, 25.99, 2.99, 1.99), True, True),
    (Product(37.49, 25.99, 4.99, 4.99), True, True),
    (Product(44.99, 29.99, 7.99, 4.99), True, True),
    (Product(54.99, 34.99, 19.99, 7.99), True, True),
    
    # Cases slightly exceeding limits
    (Product(25.51, 16.51, 3.01, 1.01), True, True),
    (Product(37.51, 26.01, 3.01, 2.01), True, True),
    (Product(37.51, 26.01, 5.01, 5.01), True, True),
    (Product(45.01, 30.01, 8.01, 5.01), True, True),
    (Product(55.01, 35.01, 20.01, 8.01), True, True),
    
    # Volume too large or Oversized
    (Product(72, 50, 41, 15), True, False),
    (Product(45, 115, 8, 5), True, False),
    (Product(100, 100, 100, 100), True, False),
    (Product(72.01, 50.01, 41.01, 15.01), True, False), 
    
    # Negative and None cases
    (Product(-1, 16.5, 3, 1), False, False),
    (Product(25.5, None, 3, 1), False, False),
    (Product(None, None, None, None), False, False),
    (Product(37.5, -1, 3, 2), False, False),
]



@pytest.mark.parametrize("product, attr_validity, logistic_validity", test_data)
def test_set_format(product, attr_validity, logistic_validity):
    estimator = LogisticsEstimator(product, Storage())
    assert estimator.attr_validity == attr_validity
    assert estimator.logistics_validity == logistic_validity