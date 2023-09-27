import enum 

class DestinationCountry(enum.Enum):
    BE = ["Belgium", "BE"]
    NL = ["Netherlands", "NL"]
    
    @classmethod
    def from_string(cls, s):
        for country in cls:
            if s in country.value:
                return country
        raise ValueError(f"{s} is not a valid DestinationCountry")


class LogisticMessages(enum.Enum):
    VOLUME_TO_LARGE = "Volume of product is too large for format L"
    NO_CALC_POSSIBLE = "Could not calculate logistics due to invalid product attributes"
    NO_FIT_FORMAT = "Product does not fit in any format"
    SUCCESS = "Success"
    INVALID_PRODUCT_ATTR = "Could not calculate logistics due to invalid product attributes. Check for None Values and or negative Values."
    
    
class CommissionMessages(enum.Enum):
    SUCCESS = "Success"
    WRONG_PRODUCT_GROUP = "Product group is not valid"
    INVALID_PRODUCT_ATTR = "Could not calculate commission due to invalid product attributes. Check for None Values and or negative Values and or missleading Product Group."
    FIXED_FEE_NOT_FOUND = "Fixed fee not found"
    PERCENTAGE_FEE_NOT_FOUND = "Percentage fee not found"
    FIXED_FEE_AND_COMMISSION_NOT_FOUND = "Fixed fee and percentage fee not found"
    
    
    
class ValidationMessages(enum.Enum):
    SUCCESS = "Success"
    COLUMNS_NOT_FOUND = lambda x: f"Columns {x} not found in uploaded file"
    
    INVALID_PRODUCT_GROUP = "Invalid product group"
    NEGATIVE_VALUE = "Negative value"
    NONE_VALUE = "None value are not allowed here. No default is used here."
    INVALID_VAT_RANGE = "Ungültiger VAT-Wert, muss im Bereich (0, 100) liegen."
    INVALID_SELLING_PRICE = "Selling price must be greater than buying price"