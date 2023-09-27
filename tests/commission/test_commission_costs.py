import pytest
from bol.CommissionEstimator import CommissionEstimator
from bol.Product import Product


products = [
        (
            Product(vat=21, price=10, productGroup="something unmatchable"),
            {
                "commission validity attr": False,
                "commission validity commission": False, 
                
            }
        ), 
        
        (
            Product(vat=101, price=10, productGroup="Animal - Cat litter"),
            {
                "commission validity attr": False,
                "commission validity commission": False, 
                
            }
        ),
        (
            Product(vat=-1, price=1000, productGroup="Animal - Cat litter"),
            {
                "commission validity attr": False,
                "commission validity commission": False, 
                
            }
        ),
        (
            Product(vat=21, price=100, productGroup="Animal - Cat litter"),
            {
                "commission validity attr": True,
                "commission validity commission": True, 
                
                "vat" : 21,
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.06,
                
                "cost fixed fee incl. vat": 0.85 * 1.21, 
                "cost percentage fee incl. vat": 100 * 0.06 * 1.21, 
                "cost surcharge": 0, 
                
            }
        ),
        (
            Product(vat=21, price=100, productGroup="Entertainment - Film (both new and second hand)***"),
            {
                "commission validity attr": True,
                "commission validity commission": True, 
                
                "vat" : 21,
                "fee fixed excl. vat.": 1.85,
                "fee percentage excl. vat": 0.09,
                
                "cost fixed fee incl. vat": 1.85 * 1.21, 
                "cost percentage fee incl. vat": 100 * 0.09 * 1.21, 
                "cost surcharge": 1 * 1.21, 
                
            }
        ),
        (
            Product(vat=21, price=100, productGroup="Household Appliances - Household Appliances"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.08,                
            }
        ),
        (
            Product(vat=21, price=99.9, productGroup="Household Appliances - Household Appliances"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.08,                
            }
        ),
        (
            Product(vat=21, price=100.1, productGroup="Household Appliances - Household Appliances"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.06,                
            }
        ),
        
        (
            Product(vat=21, price=10, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed excl. vat.": 0.2,
                "fee percentage excl. vat": 0.04,                
            }
        ),
        
        (
            Product(vat=21, price=15, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed excl. vat.": 0.4,
                "fee percentage excl. vat": 0.04,                
            }
        ),
        
        (
            Product(vat=21, price=25, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.1,                
            }
        ),
        
        (
            Product(vat=21, price=50, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.1,                
            }
        ),
        
        (
            Product(vat=21, price=51, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.13,                
            }
        ),
        
        (
            Product(vat=21, price=51, productGroup="Beauty and Care - Daily Care (except Contact Lenses and Lens Solution)"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.108,                
            }
        ),
        
        (
            Product(vat=21, price=20, productGroup="Beauty and Care - Daily Care (except Contact Lenses and Lens Solution)"),
            {
                
                "fee fixed excl. vat.": 0.4,
                "fee percentage excl. vat": 0,                
            }
        ),
        
        (
            Product(vat=21, price=20, productGroup="Beauty and Care - Daily Care"),
            {
                
                "fee fixed excl. vat.": 0.4,
                "fee percentage excl. vat": 0.05,                
            }
        ),        
        (
            Product(vat=21, price=21, productGroup="Beauty and Care - Daily Care"),
            {
                
                "fee fixed excl. vat.": 0.85,
                "fee percentage excl. vat": 0.00,                
            }
        ),        
]



@pytest.mark.parametrize("product, expected_dict", products)
def test_commission_estimator(product, expected_dict):
    ce = CommissionEstimator(product)
    cCosts = ce.get_commission_costs()
    for key, value in expected_dict.items():
        assert cCosts[key] == value