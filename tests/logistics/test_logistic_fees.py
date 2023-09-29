import pytest 
from bol.Product import Product
from bol.Storage import Storage
from bol.LogisticsEstimator import LogisticsEstimator
from bol.LogisticsAttrValidator import LogisticsAttrValidator



test_data = [
    
    (
        Product(1, 1, 1, 1),
        Storage(),
        {           
            "fee fragile": 0, 
            "fee perishable": 0, 
            "fee labeling": 0, 
            
            "fee per article": 1.3,
            "fee per delivery": 1.07, 
            "fee storage": 0.13, 
        }
    ),
        
    (
        Product(37.5, 26, 3, 2),
        Storage(),
        {

            "fee per article": 1.39,
            "fee per delivery": 1.63, 
            "fee storage": 0.14, 
        }
    ),
            
    (
        Product(37.5, 26, 5, 5),
        Storage(),
        {

            "fee per article": 1.58,
            "fee per delivery": 2.92, 
            "fee storage": 0.23, 
        }
    ),
                
    (
        Product(45, 30, 8, 5),
        Storage(),
        {

            "fee per article": 1.99,
            "fee per delivery": 3.38, 
            "fee storage": 0.45, 
        }
    ),
                    
    (
        Product(55, 35, 20, 8),
        Storage(),
        {
            "fee per article": 2.1,
            "fee per delivery": 3.42, 
            "fee storage": 0.60, 
        }
    ),
    
                        
    (
        Product(72, 30, 30, 15),
        Storage(),
        {
            "fee per article": 2.81,
            "fee per delivery": 3.73, 
            "fee storage": 0.90, 
        }
    ),
    
    # double duration
    (
        Product(72, 30, 30, 15),
        Storage(duration=2),
        {
            "fee per article": 2.81,
            "fee per delivery": 3.73, 
            "fee storage": 1.80, 
            "total logistics fee": 8.34,
        }
    ),
    
    # winter storage & persihable, fragile, labeling
        (
        Product(1, 1, 1, 1, labeling=True, fragile=True, perishable=True),
        Storage(winter=1),
        {

            "fee fragile": 0.35, 
            "fee perishable": 0.35, 
            "fee labeling": 0.18, 
            
            "fee per article": 1.3,
            "fee per delivery": 1.07, 
            "fee storage": 0.18, 
        }
    ),
        
    (
        Product(37.5, 26, 3, 2),
        Storage(winter=1),
        {

            "fee per article": 1.39,
            "fee per delivery": 1.63, 
            "fee storage": 0.20, 
        }
    ),
            
    (
        Product(37.5, 26, 5, 5),
        Storage(winter=1),
        {

            "fee per article": 1.58,
            "fee per delivery": 2.92, 
            "fee storage": 0.32, 
        }
    ),
                
    (
        Product(45, 30, 8, 5),
        Storage(winter=1),
        {

            "fee per article": 1.99,
            "fee per delivery": 3.38, 
            "fee storage": 0.63, 
        }
    ),
                    
    (
        Product(55, 35, 20, 8),
        Storage(winter=1),
        {

            "fee per article": 2.1,
            "fee per delivery": 3.42, 
            "fee storage": 0.84, 
        }
    ),
    
                        
    (
        Product(72, 30, 30, 15),
        Storage(winter=1, duration=10),
        {
            "fee per article": 2.81,
            "fee per delivery": 3.73, 
            "fee storage": 12.6, 
        }
    ),
    
    
    # Total costs
    (
        Product(72, 30, 30, 15),
        Storage(winter=1, duration=10),
        {
            "logistic validity attr": True,
            "logistic message attr": "Success", 
            
            "logistic validity logistics": True,
            "logistic message logistics": "Success",    
            
            "format": "L", 
            "storage winter": True, 
            "storage duration": 10,
            
            
            "fee per article": 2.81,
            "fee per delivery": 3.73, 
            "fee fragile": 0, 
            "fee perishable": 0, 
            "fee labeling": 0, 
            "fee storage": 12.60, 
            
            "total logistics fee": 19.14, 
        }
    ), 
    
    (
        Product(72, 30, 30, 15, labeling=True, fragile=True, perishable=True),
        Storage(winter=1, duration=10),
        {
            "logistic validity attr": True,
            "logistic message attr": "Success", 
            
            "logistic validity logistics": True,
            "logistic message logistics": "Success",    
            
            "format": "L", 
            "storage winter": True, 
            "storage duration": 10,
                        
            "fee per article": 2.81,
            "fee per delivery": 3.73, 
            "fee fragile": 0.35, 
            "fee perishable": 0.35, 
            "fee labeling": 0.18, 
            "fee storage": 12.60, 
            
            "total logistics fee": round(19.14 + 0.18 + 0.35 + 0.35, 2), 
        }
    ), 
    (
        
        Product(-1, 16.5, 3, 1),
        Storage(winter=1, duration=10),
        {
            "logistic validity attr": False,
            "logistic validity logistics": False,
            "format": None, 
            "storage winter": True, 
            "storage duration": 10,
            "fee per article": None,
            "fee per delivery": None, 
            "fee fragile": None, 
            "fee perishable": None, 
            "fee labeling": None, 
            "fee storage": None, 
            "total logistics fee": None, 
        }
         
         
         
    ),
    
    
]
    
@pytest.mark.parametrize("product, storage, expected_dict", test_data)
def test_get_summary_dictionary(product, storage, expected_dict):
    estimator = LogisticsEstimator(product, storage)
    cCosts = estimator.get_logistic_fees() 
    
    for key, value in expected_dict.items():
        assert cCosts[key] == value