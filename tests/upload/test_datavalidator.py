import pytest
import pandas as pd



from upload.DataValidator import DataValidator  
from bol.enums import ValidationMessages

@pytest.fixture
def validator():
    return DataValidator() 

"""

    df = pd.DataFrame(
        {
            "length": [1, 2, 3],
            "width": [1, 2, 3],
            "height": [1, 2, 3],
            "weight": [1, 2, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            "vat": [1, 2, 3],
            "perishable": [True, False, True],
            "fragile": [True, False, True],
            "labeling": [True, False, True],
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": "TV and Audio - Television",
        }
    )   




"""


def test_valid_setup(validator):
    df = pd.DataFrame(
        {
            "length": [1, 2, 3],
            "width": [1, 2, 3],
            "height": [1, 2, 3],
            "weight": [1, 2, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            "vat": [1, 2, 3],
            "perishable": [True, False, True],
            "fragile": [True, False, True],
            "labeling": [True, False, True],
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": "TV and Audio - Television",
        }
    )   
    dfVal, logs = validator.validate_uploaded_file(df)
    assert dfVal.to_json() == df.to_json()
    
    

def test_missing_not_required_column(validator):
    
    df = pd.DataFrame(
        {
            "length": [1, 2, 3],
            "width": [1, 2, 3],
            "height": [1, 2, 3],
            "weight": [1, 2, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            "vat": [1, 2, 3],
            "perishable": [True, False, True],
            "fragile": [True, False, True],
            "labeling": [True, False, True],
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": "TV and Audio - Television",
        }
    )   
    
    
    
    dfVal, _ = validator.validate_uploaded_file(df)
    assert dfVal.to_json() == df.to_json()
    
def test_setting_defaults(validator):
    
    df = pd.DataFrame(
        {
            "length": [1, 2, 3],
            "width": [1, 2, 3],
            "height": [1, 2, 3],
            "weight": [1, 2, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            # Default fragile 
            # Default labeling
            # Default persihable
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": "TV and Audio - Television",
        }
    )   
    
    dfVal, logs = validator.validate_uploaded_file(df)
    assert (~dfVal["fragile"]).all()
    assert (~dfVal["perishable"]).all()
    assert (~dfVal["labeling"]).all()
    assert (dfVal["vat"] == 21).all()
    assert len(logs["changes"]) == 6
    assert len(logs["attr_mismatch"]) == 0
    assert len(logs["excluded_rows"]) == 0
    assert len(logs["column_not_found"]) == 0
    assert len(logs["column_not_transformable"]) == 0

def test_missing_required_column(validator):
    df = pd.DataFrame(
        {
            # missing length 
            # missing width
            "height": [1, 2, 3],
            "weight": [1, 2, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": "TV and Audio - Television",
        }
    )   
    
    cDf, logs = validator.validate_uploaded_file(df)
    assert len(logs["column_not_found"]) == 2
    
    
def test_negative_values(validator):
    df = pd.DataFrame(
        {
            "length": [-1, 2, -3],
            "width": [1, 2, 3],
            "height": [1, 2, 3],
            "weight": [1, -2, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            "vat": [1, 2, -3],
            "perishable": [True, False, True],
            "fragile": [True, False, True],
            "labeling": [True, True, True],
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": "TV and Audio - Television",
        }
    )   
    dfVal, logs = validator.validate_uploaded_file(df)
    assert len(logs["attr_mismatch"]) == 5
    assert len(logs["excluded_rows"]) == 3
    
        

def test_not_transformable_values(validator):
    df = pd.DataFrame(
        {
            "length": [1, 2, 3],
            "width": [1, 2, 3],
            "height": [1, 2, 3],
            "weight": [1, 2, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            "vat": [1, 2, 3],
            "perishable": [True, False, True],
            "fragile": [True, False, True],
            "labeling": [True, False, True],
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": ["TV and Audio - Television","TV and Audio - Television2","TV and Audio - Television"],
        }
    )   
    dfVal, logs = validator.validate_uploaded_file(df)    
    assert len(logs["excluded_rows"]) == 1
    assert logs["excluded_rows"] == {1}
    assert logs["attr_mismatch"] == [("product group", 1, ValidationMessages.INVALID_PRODUCT_GROUP.value)]
    
    
    
def test_none_values(validator):
    df = pd.DataFrame(
        {
            "length": [1, 2, 3],
            "width": [1, 2, 3],
            "height": [1, 2, 3],
            "weight": [1, None, 3],
            "selling price incl. vat": [1, 2, 3],
            "buying price excl. vat": [1, 2, 3],
            "vat": [1, 2, 3],
            "perishable": [True, False, True],
            "fragile": [True, False, True],
            "labeling": [True, False, True],
            "storage winter": [True, False, True],
            "product name": "Television",
            "product group": ["TV and Audio - Television","TV and Audio - Television","TV and Audio - Television"],
        }
    )   
    dfVal, logs = validator.validate_uploaded_file(df)    
    assert len(logs["excluded_rows"]) == 1
    assert logs["excluded_rows"] == {1}
    #assert logs["attr_mismatch"] == [("weight", 1, ValidationMessages.NONE_VALUE.value)]