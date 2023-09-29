
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
                "fee fixed": 0.85,
                "fee percentage": 0.06 * 100,
                "fee surcharge": 0, 
                
            }
        ),
        (
            Product(vat=21, price=100, productGroup="Entertainment - Film (both new and second hand)***"),
            {
                "commission validity attr": True,
                "commission validity commission": True, 
                
                "vat" : 21,
                "fee fixed": 1.85,
                "fee percentage": 0.09 * 100,
                "fee surcharge": 1, 
                
            }
        ),
        (
            Product(vat=21, price=100, productGroup="Household Appliances - Household Appliances"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.08 * 100,                
            }
        ),
        (
            Product(vat=21, price=99.9, productGroup="Household Appliances - Household Appliances"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.08 * 99.9,                
            }
        ),
        (
            Product(vat=21, price=100.1, productGroup="Household Appliances - Household Appliances"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.06 * 100.1,                
            }
        ),
        
        (
            Product(vat=21, price=10, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed": 0.2,
                "fee percentage": 0.04 * 10,                
            }
        ),
        
        (
            Product(vat=21, price=15, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed": 0.4,
                "fee percentage": 0.04 * 15,                
            }
        ),
        
        (
            Product(vat=21, price=25, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.1 * 25,                
            }
        ),
        
        (
            Product(vat=21, price=50, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.1 *50,                
            }
        ),
        
        (
            Product(vat=21, price=51, productGroup="Fashion and Sports - Baby and Children's Clothing"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.13*51,                
            }
        ),
        
        (
            Product(vat=21, price=51, productGroup="Beauty and Care - Daily Care (except Contact Lenses and Lens Solution)"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.108*51,                
            }
        ),
        
        (
            Product(vat=21, price=20, productGroup="Beauty and Care - Daily Care (except Contact Lenses and Lens Solution)"),
            {
                
                "fee fixed": 0.4,
                "fee percentage": 0*20,                
            }
        ),
        
        (
            Product(vat=21, price=20, productGroup="Beauty and Care - Daily Care"),
            {
                
                "fee fixed": 0.4,
                "fee percentage": 0.05*20,                
            }
        ),        
        (
            Product(vat=21, price=21, productGroup="Beauty and Care - Daily Care"),
            {
                
                "fee fixed": 0.85,
                "fee percentage": 0.00*21,                
            }
        ),        
]



@pytest.mark.parametrize("product, expected_dict", products)
def test_commission_estimator(product, expected_dict):
    ce = CommissionEstimator(product)
    cCosts = ce.get_commission_fees()
    for key, value in expected_dict.items():
        assert cCosts[key] == value