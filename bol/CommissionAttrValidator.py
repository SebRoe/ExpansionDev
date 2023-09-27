from .enums import CommissionMessages
from .constants.commissions import PRODUCT_GROUPS

class CommissionAttrValidatior:
    
    def __init__(self):
        pass
    
    @classmethod
    def validate_attr_product(self, product):
        
        cValid = True
        error_messages = []
        
        if (product.vat is None 
            or product.vat < 0
            or product.vat > 100
            ):
            cValid = False
            error_messages.append("vat")
            
        if product.productGroup is None or product.productGroup not in PRODUCT_GROUPS:
            cValid = False
            error_messages.append("productGroup")
            
        if product.price is None or product.price < 0:
            cValid = False
            error_messages.append("price")
            
            
        if len(error_messages) == 0:
            error_message = CommissionMessages.SUCCESS.value
        else:
            error_message = CommissionMessages.INVALID_PRODUCT_ATTR.value
            
        return cValid, error_message
            
        