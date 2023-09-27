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
            "fee fragile": 0.35,
            "fee perishalbe": 0.35,
            "fee labeling": 0.18,
            
            "cost fragile": 0, 
            "cost perishable": 0, 
            "cost labeling": 0, 
            
            "fee storage per month": 0.13, 
            "cost per article": 1.3,
            "cost per delivery": 1.07, 
            "cost storage": 0.13, 
        }
    ),
        
    (
        Product(37.5, 26, 3, 2),
        Storage(),
        {
            "fee storage per month": 0.14, 
            "cost per article": 1.39,
            "cost per delivery": 1.63, 
            "cost storage": 0.14, 
        }
    ),
            
    (
        Product(37.5, 26, 5, 5),
        Storage(),
        {
            "fee storage per month": 0.23, 
            "cost per article": 1.58,
            "cost per delivery": 2.92, 
            "cost storage": 0.23, 
        }
    ),
                
    (
        Product(45, 30, 8, 5),
        Storage(),
        {
            "fee storage per month": 0.45, 
            "cost per article": 1.99,
            "cost per delivery": 3.38, 
            "cost storage": 0.45, 
        }
    ),
                    
    (
        Product(55, 35, 20, 8),
        Storage(),
        {
            "fee storage per month": 0.60, 
            "cost per article": 2.1,
            "cost per delivery": 3.42, 
            "cost storage": 0.60, 
        }
    ),
    
                        
    (
        Product(72, 30, 30, 15),
        Storage(),
        {
            "fee storage per month": 0.90, 
            "cost per article": 2.81,
            "cost per delivery": 3.73, 
            "cost storage": 0.90, 
        }
    ),
    
    # double duration
    (
        Product(72, 30, 30, 15),
        Storage(duration=2),
        {
            "fee storage per month": 0.90, 
            "cost per article": 2.81,
            "cost per delivery": 3.73, 
            "cost storage": 1.80, 
            "total logistics costs": 8.34,
        }
    ),
    
    # winter storage & persihable, fragile, labeling
        (
        Product(1, 1, 1, 1, labeling=True, fragile=True, perishable=True),
        Storage(winter=1),
        {

            "cost fragile": 0.35, 
            "cost perishable": 0.35, 
            "cost labeling": 0.18, 
            
            "fee storage per month": 0.18, 
            "cost per article": 1.3,
            "cost per delivery": 1.07, 
            "cost storage": 0.18, 
        }
    ),
        
    (
        Product(37.5, 26, 3, 2),
        Storage(winter=1),
        {
            "fee storage per month": 0.20, 
            "cost per article": 1.39,
            "cost per delivery": 1.63, 
            "cost storage": 0.20, 
        }
    ),
            
    (
        Product(37.5, 26, 5, 5),
        Storage(winter=1),
        {
            "fee storage per month": 0.32, 
            "cost per article": 1.58,
            "cost per delivery": 2.92, 
            "cost storage": 0.32, 
        }
    ),
                
    (
        Product(45, 30, 8, 5),
        Storage(winter=1),
        {
            "fee storage per month": 0.63, 
            "cost per article": 1.99,
            "cost per delivery": 3.38, 
            "cost storage": 0.63, 
        }
    ),
                    
    (
        Product(55, 35, 20, 8),
        Storage(winter=1),
        {
            "fee storage per month": 0.84, 
            "cost per article": 2.1,
            "cost per delivery": 3.42, 
            "cost storage": 0.84, 
        }
    ),
    
                        
    (
        Product(72, 30, 30, 15),
        Storage(winter=1, duration=10),
        {
            "fee storage per month": 1.26, 
            "cost per article": 2.81,
            "cost per delivery": 3.73, 
            "cost storage": 12.6, 
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
            
            "fee storage per month": 1.26, 
            "fee fragile": 0.35,
            "fee perishalbe": 0.35, 
            "fee labeling": 0.18,
            
            "cost per article": 2.81,
            "cost per delivery": 3.73, 
            "cost fragile": 0, 
            "cost perishable": 0, 
            "cost labeling": 0, 
            "cost storage": 12.60, 
            
            "total logistics costs": 19.14, 
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
            
            "fee storage per month": 1.26, 
            "fee fragile": 0.35,
            "fee perishalbe": 0.35, 
            "fee labeling": 0.18,
            
            "cost per article": 2.81,
            "cost per delivery": 3.73, 
            "cost fragile": 0.35, 
            "cost perishable": 0.35, 
            "cost labeling": 0.18, 
            "cost storage": 12.60, 
            
            "total logistics costs": round(19.14 + 0.18 + 0.35 + 0.35, 2), 
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
            "fee storage per month": None, 
            "fee fragile": 0.35,
            "fee perishalbe": 0.35, 
            "fee labeling": 0.18,
            "cost per article": None,
            "cost per delivery": None, 
            "cost fragile": None, 
            "cost perishable": None, 
            "cost labeling": None, 
            "cost storage": None, 
            "total logistics costs": None, 
        }
         
         
         
    ),
    
    
]
    
@pytest.mark.parametrize("product, storage, expected_dict", test_data)
def test_get_summary_dictionary(product, storage, expected_dict):
    estimator = LogisticsEstimator(product, storage)
    cCosts = estimator.get_logistic_costs() 
    
    for key, value in expected_dict.items():
        assert cCosts[key] == value