from .Product import Product
from .Storage import Storage
from .enums import DestinationCountry, LogisticMessages


class LogisticsAttrValidator():
    
    def __init__(self):
        pass
    
    
    @classmethod
    def validate_attr_product(cls, product:Product, storage:Storage):
        
        cValid = True
        error_messages = []
        
        if product.length is None or product.length < 0:
            cValid = False
            error_messages.append("length")
            
        if product.width is None or product.width < 0:
            cValid = False
            error_messages.append("width")
            
        if product.height is None or product.height < 0:
            cValid = False
            error_messages.append("height")
            
        if product.weight is None or product.weight < 0:
            cValid = False
            error_messages.append("weight")
            
        if product.perishable is None:
            cValid = False
            error_messages.append("perishable")
            
        if product.fragile is None:
            cValid = False
            error_messages.append("fragile")
            
        if product.labeling is None:
            cValid = False
            error_messages.append("labeling")
            
        if storage.winter is None:
            cValid = False
            error_messages.append("winterStorage")
            
        if storage.duration is None or storage.duration < 0:
            cValid = False
            error_messages.append("duration")    
        
        if len(error_messages) == 0:
            error_message = LogisticMessages.SUCCESS.value
        else:
            error_message = LogisticMessages.INVALID_PRODUCT_ATTR.value
            
        return cValid, error_message
    