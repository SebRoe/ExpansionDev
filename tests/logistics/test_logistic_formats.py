import pytest 
from bol.Product import Product
from bol.Storage import Storage
from bol.LogisticsEstimator import LogisticsEstimator
from bol.LogisticsAttrValidator import LogisticsAttrValidator
from bol.enums import DestinationCountry

### Testing Attr Validation and Logistics Validation ###

test_data = [
    
    # Valid Cases
    (Product(1, 1, 1, 1), "XXXS"),
    (Product(25.5, 16.5, 3, 1), "XXXS"),
    (Product(37.5, 26, 3, 2), "XXS"),
    (Product(37.5, 26, 5, 5), "XS"),
    (Product(45, 30, 8, 5), "S"),
    (Product(55, 35, 20, 8), "M"),
    (Product(72, 30, 30, 15), "L"),
    
    # Borderline cases - just within limit
    (Product(25.49, 16.49, 2.99, 0.99), "XXXS"),
    (Product(37.49, 25.99, 2.99, 1.99), "XXS"),
    (Product(37.49, 25.99, 4.99, 4.99), "XS"),
    (Product(44.99, 29.99, 7.99, 4.99), "S"),
    (Product(54.99, 34.99, 19.99, 7.99), "M"),
    
    # Cases slightly exceeding limits
    (Product(25.51, 16.51, 3.01, 1.01), "XS"),
    (Product(37.51, 26.01, 3.01, 2.01), "S"),
    (Product(37.51, 26.01, 5.01, 5.01), "M"),
    (Product(45.01, 30.01, 8.01, 5.01), "M"),
    (Product(55.01, 35.01, 20.01, 8.01), "L"),

    
    # Negative and None cases
    (Product(-1, 16.5, 3, 1), None),
    (Product(25.5, None, 3, 1), None),
    (Product(None, None, None, None), None),
    (Product(37.5, -1, 3, 2), None),
    
    # Volume too large or Oversized
    (Product(72, 50, 41, 15), None),
    (Product(45, 115, 8, 5), None),
    (Product(100, 100, 100, 100), None),
    (Product(72.01, 50.01, 41.01, 15.01), None),  
]


@pytest.mark.parametrize("product, expected_format", test_data)
def test_set_format(product, expected_format):
    estimator = LogisticsEstimator(product, Storage())
    assert estimator.format == expected_format
    
    
    
@pytest.mark.parametrize("product, expected_format", test_data)
def test_set_format(product, expected_format):
    estimator = LogisticsEstimator(product, Storage(), DestinationCountry.BE)
    if expected_format == "XXXS" or expected_format == "XXS":
        expected_format = "XS"
    
    assert estimator.format == expected_format