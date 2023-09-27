import copy
import regex as re
from .constants.commissions import COMMISSIONS
from .constants.commissions import PRODUCT_GROUPS
from .Product import Product 
from .CommissionAttrValidator import CommissionAttrValidatior
from .enums import CommissionMessages

class CommissionEstimator:
    
    def __init__(self, product:Product ):
        
        self.attr_validity = None
        self.attr_message = None 
        
        self.commission_validity = None
        self.commission_message = None
        
        self.fixed_fee = None 
        self.percentage_fee = None
        
        self.product = product 

        self.COMMISSIONS = copy.deepcopy(COMMISSIONS)
        self.PRODUCT_GROUPS = copy.deepcopy(PRODUCT_GROUPS)
        
        self._validate_product()


    def _validate_product(self):
        self.attr_validity, self.attr_message = CommissionAttrValidatior.validate_attr_product(self.product)
        if self.attr_validity:
            self._set_fees()
        else:
            self.commission_validity = False
            self.commission_message = CommissionMessages.INVALID_PRODUCT_ATTR.value
            
            
    def _get_surcharge(self):
        pattern = r'(?<!\*)\*\*\*(?!\*)'
        if re.search( pattern, self.product.productGroup,):
            return 1
        else:
            return 0 
        
    def _set_fees(self):
        
        found_price_range = False
        found_percentage = False 
        
        groupCosts = self.COMMISSIONS[self.product.productGroup]
        
        if "percentage" in groupCosts.keys():
            found_percentage = True
            percentage_fee = groupCosts["percentage"]
        else:
            percentage_fee = 0
            found_percentage = True
        
        
        for price_range, fixed_fee in groupCosts.items():
            if price_range in ["conditions", "percentage"]:
                continue

            if isinstance(price_range, tuple):
                
                if price_range[0] == 0 and self.product.price <= price_range[1]:
                    found_price_range = True
                    break
                
                if price_range[0] < self.product.price <= price_range[1]:
                    found_price_range = True 
                    break
                
        
        
        if "conditions" in groupCosts:
            for condition, percentage in groupCosts["conditions"].items():
                numbers = [
                    float(num.replace("€", ""))
                    for num in condition.split()
                    if "€" in num
                ]

                if len(numbers) > 2 or len(numbers) == 0:
                    raise ValueError("Invalid condition: {}".format(condition))

                if (
                    "up to" in condition
                    and not "from" in condition
                    and self.product.price <= max(numbers)
                    
                ):
                    percentage_fee = percentage
                    found_percentage = True
                    break
                elif (
                    "from" in condition
                    and "up to" in condition
                    and min(numbers) < self.product.price <= max(numbers)
                ):
                    percentage_fee = percentage
                    found_percentage = True
                    break
                elif (
                    "from" in condition
                    and not "up to" in condition
                    and min(numbers) < self.product.price
                ):
                    percentage_fee = percentage
                    found_percentage = True
                    break


        if found_percentage and found_price_range:
            self.commission_validity = True
            self.commission_message = CommissionMessages.SUCCESS.value
            self.fixed_fee = fixed_fee
            self.percentage_fee = percentage_fee
        else:
            self.commission_validity = False
            if found_percentage and not found_price_range:
                self.commission_message = CommissionMessages.FIXED_FEE_NOT_FOUND.value
            elif not found_percentage and found_price_range:
                self.commission_message = CommissionMessages.PERCENTAGE_FEE_NOT_FOUND.value
            else:
                self.commission_message = CommissionMessages.FIXED_FEE_AND_COMMISSION_NOT_FOUND.value
                
            

    def _get_summary_dictionary(self):
        return {
            
            "commission validity attr": self.attr_validity,
            "commission message attr": self.attr_message,
            
            "commission validity commission": self.commission_validity,
            "commission message commission": self.commission_message,
            
            "product group": self.product.productGroup,
            "price": self.product.price,
            "vat": self.product.vat,
            
            "fee fixed excl. vat.": self.fixed_fee,
            "fee percentage excl. vat": self.percentage_fee,
            
            "cost fixed fee incl. vat": None, 
            "cost percentage fee incl. vat": None, 
            "cost surcharge": None, 
            
            "total commissions costs": None 
            
        }
        
    def _calculate_total_costs(self, cCosts:dict):
        if self.attr_validity and self.commission_validity:
            cCosts["total commissions costs"] = 0
            cCosts["total commissions costs"] += cCosts["cost fixed fee incl. vat"]
            cCosts["total commissions costs"] += cCosts["cost percentage fee incl. vat"]
            cCosts["total commissions costs"] += cCosts["cost surcharge"]
        else:
            cCosts["total commissions costs"] = None
            
        return cCosts
    
        
    def get_commission_costs(self):
        cCosts = self._get_summary_dictionary()
        
        if not self.attr_validity or not self.commission_validity:
            return cCosts
        else:
            cCosts["cost fixed fee incl. vat"] = self.fixed_fee * (1 + (self.product.vat / 100))
            cCosts["cost percentage fee incl. vat"] = self.percentage_fee * self.product.price * (1 + (self.product.vat / 100))
            cCosts["cost surcharge"] = self._get_surcharge() * (1 + (self.product.vat / 100))
            
            cCosts = self._calculate_total_costs(cCosts)
            
            return cCosts