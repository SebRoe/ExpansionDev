
class Product:
    
    def __init__(self, length: float = None, width: float = None, height: float = None,
                 weight: float = None, perishable: bool = False, fragile: bool = False,
                 labeling: bool = False, price:float = None, vat:float = None,
                 productGroup:str = None, productName:str = None):
                
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.perishable = perishable
        self.fragile = fragile
        self.labeling = labeling
        
        self.price = price
        self.vat = vat
        self.productGroup = productGroup
        self.productName = productName
        
        
