import pytest
from bol.CommissionEstimator import CommissionEstimator
from bol.Product import Product

productGroups = [
    ("Computer - Input Devices - A-brands****", 0),
    ("Computer - Supplies - Original brands *****", 0),
    ("Entertainment - Film (both new and second hand)***", 1),
    ("Entertainment - Music (both new and second hand **", 0),
    ("Entertainment*** - Film (both new and second hand)", 1), 
    ("Enter*t*ain**ment - Film (both new ***** and second hand)**", 0),
]


@pytest.mark.parametrize("productGroup, expected_surcharge", productGroups)
def test_commission_surcharge(productGroup, expected_surcharge):
    product = Product(
        price=100,
        vat=0.21,
        productGroup=productGroup
    )
    commission_estimator = CommissionEstimator(product)
    assert commission_estimator._get_surcharge() == expected_surcharge