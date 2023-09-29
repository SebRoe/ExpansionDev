import copy
from .enums import DestinationCountry, LogisticMessages
from .Product import Product
from .Storage import Storage
from .LogisticsAttrValidator import LogisticsAttrValidator
from .constants.logistics import FORMATS
from .constants.logistics import COSTS_PER_FORMAT
from .constants.logistics import STORAGE_COSTS_WINTER_HOLIDAYS
from .constants.logistics import ADDITIONAL_COSTS
from .constants.logistics import RETRIEVAL_AND_SHIPPING_COSTS

class LogisticsEstimator():
    
    def __init__(self, product:Product, storage:Storage, destination:DestinationCountry = DestinationCountry.NL):
        
        self.product = product
        self.storage = storage
        
        self.format = None        
        self.volume = None 
        
        self.attr_validity = None
        self.attr_message = None 
        
        self.logistics_validity = None 
        self.logistics_message = None 
        
        self.destination = destination
        
        self.ADDITIONAL_COSTS = copy.deepcopy(ADDITIONAL_COSTS)
        self.RETRIEVAL_AND_SHIPPING_COSTS = copy.deepcopy(RETRIEVAL_AND_SHIPPING_COSTS)
        self.STORAGE_COSTS_WINTER_HOLIDAYS = copy.deepcopy(STORAGE_COSTS_WINTER_HOLIDAYS)
        self.COSTS_PER_FORMAT = copy.deepcopy(COSTS_PER_FORMAT)
        self.FORMATS = copy.deepcopy(FORMATS)
        
        self._validate_product()
        

    def _validate_product(self):
        
        self.attr_validity, self.attr_message = LogisticsAttrValidator.validate_attr_product(self.product, self.storage)
        if not self.attr_validity:
            self.logistics_validity = False
            self.logistics_message = LogisticMessages.NO_CALC_POSSIBLE.value
        else:
            self._set_format()

    def _calculate_volume(self):
        return (self.product.length * self.product.width * self.product.height) / 1000
    
    def _set_format(self):
        sorted_formats = sorted(
            self.FORMATS.items(),
            key=lambda x: (
                x[1]["length"],
                x[1]["width"],
                x[1]["height"],
                x[1]["weight"],
            ),
        )

        for format, dimensions in sorted_formats:
            vLength = dimensions["length"] >= self.product.length
            vWidth = dimensions["width"] >= self.product.width
            vHeight = dimensions["height"] >= self.product.height
            vWeight = dimensions["weight"] >= self.product.weight

            if vLength and vWidth and vHeight and vWeight:
                if format == "L":
                    cVol = self._calculate_volume()
                    if cVol > 70:
                        self.logistics_validity = False
                        self.logistics_message = LogisticMessages.VOLUME_TO_LARGE.value
                        return
                    
                if self.destination == DestinationCountry.BE:
                    if format == "XXXS" or format == "XXS":
                        format = "XS"
                    
                self.format = format
                self.logistics_validity = True
                self.logistics_message = "Success"
                return
            
        self.logistics_validity = False
        self.logistics_message = LogisticMessages.NO_FIT_FORMAT.value
        
        

    def _calculate_storage_fees(self):
        if self.attr_validity and self.logistics_validity:
            if self.storage.winter:
                return self.STORAGE_COSTS_WINTER_HOLIDAYS[self.format] * self.storage.duration
            else:
                return self.COSTS_PER_FORMAT[self.format]["storage_cost_per_month"] * self.storage.duration
        else:
            return None 

    def _get_storage_fee(self):
        if self.attr_validity and self.logistics_validity:
            if self.storage.winter:
                return self.STORAGE_COSTS_WINTER_HOLIDAYS[self.format]
            else:
                return self.COSTS_PER_FORMAT[self.format]["storage_cost_per_month"]
        else:
            return None 
        
    def _get_summary_dictionary(self):
        return {
            "logistic validity attr": self.attr_validity,
            "logistic message attr": self.attr_message, 
            
            "logistic validity logistics": self.logistics_validity,
            "logistic message logistics": self.logistics_message,    
            
            "format": self.format, 
            "storage winter": self.storage.winter, 
            "storage duration": self.storage.duration,
            
            "fee per article": None,
            "fee per delivery": None, 
            "fee fragile": None, 
            "fee perishable": None, 
            "fee labeling": None, 
            "fee storage": None, 
            
            "total logistics fee": None, 
        }
        
        
    def _calculate_total_fees(self, cCosts:dict):
        if self.attr_validity and self.logistics_validity:
            cCosts["total logistics fee"] = 0
            cCosts["total logistics fee"] += cCosts["fee per article"]
            cCosts["total logistics fee"] += cCosts["fee per delivery"]
            cCosts["total logistics fee"] += cCosts["fee fragile"]
            cCosts["total logistics fee"] += cCosts["fee perishable"]
            cCosts["total logistics fee"] += cCosts["fee labeling"]
            cCosts["total logistics fee"] += cCosts["fee storage"]

        else:
            cCosts["total logistics fee"] = None
            
        return cCosts
    
    
        
    def get_logistic_fees(self):
        
        cCosts = self._get_summary_dictionary()
        
        if not self.attr_validity or not self.logistics_validity:
            return cCosts
        else:
            cCosts["fee per article"] = self.COSTS_PER_FORMAT[self.format]["cost_per_article"]
            cCosts["fee per delivery"] = self.COSTS_PER_FORMAT[self.format]["cost_per_delivery"]
            
            if self.product.fragile:
                cCosts["fee fragile"] = self.ADDITIONAL_COSTS["fragile"]
            else:
                cCosts["fee fragile"] = 0
                
            if self.product.perishable:
                cCosts["fee perishable"] = self.ADDITIONAL_COSTS["perishable"]
            else:
                cCosts["fee perishable"] = 0
                
            if self.product.labeling:
                cCosts["fee labeling"] = self.ADDITIONAL_COSTS["label"]
            else:
                cCosts["fee labeling"] = 0
                
            cCosts["fee storage"] = self._calculate_storage_fees()
            
            cCosts = self._calculate_total_fees(cCosts)
            
            return cCosts
            
        