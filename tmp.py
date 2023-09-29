from bol.CommissionEstimator import CommissionEstimator
from bol.LogisticsEstimator import LogisticsEstimator
from bol.Product import Product
from bol.Storage import Storage
from bol.enums import DestinationCountry, LogisticMessages

product = Product(vat=21, price=100, productGroup="Animal - Cat litter")
storage = Storage(duration=1, winter=False)

estimator = CommissionEstimator(product)
estimator_log = LogisticsEstimator(product, storage, destination=DestinationCountry.BE)


print(estimator.get_commission_fees())
print(estimator_log.get_logistic_fees())


