import json
from fedex.config import FedexConfig
from fedex.services.rate_service import FedexRateServiceRequest
from fedex.tools.conversion import sobject_to_dict

with open("app/access/creds/creds.json") as f:
    credentials = json.load(f)['fedex']

CONFIG_OBJ = FedexConfig(key=credentials['api_key'],
                         password=credentials['password'],
                         account_number=credentials['ship_num'],
                         use_test_server=True)

rate = FedexRateServiceRequest(CONFIG_OBJ)

rate.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
# STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER
rate.RequestedShipment.ServiceType = 'FEDEX_GROUND'
#  FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
rate.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

# Sender info
rate.RequestedShipment.Shipper.Address.PostalCode = '98007'
rate.RequestedShipment.Shipper.Address.CountryCode = 'US'
rate.RequestedShipment.Shipper.Address.Residential = False

# Recipient info
rate.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'NC'
rate.RequestedShipment.Recipient.Address.PostalCode = '27577'
rate.RequestedShipment.Recipient.Address.CountryCode = 'US'
rate.RequestedShipment.Recipient.Address.Residential = True

rate.RequestedShipment.EdtRequestType = 'NONE'
rate.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

package1_weight = rate.create_wsdl_object_of_type('Weight')
package1_weight.Value = 1.0
package1_weight.Units = "LB"
package1 = rate.create_wsdl_object_of_type('RequestedPackageLineItem')
package1.Weight = package1_weight
package1.PhysicalPackaging = 'BOX'
package1.GroupPackageCount = 1
rate.add_package(package1)

rate.send_request()


print(sobject_to_dict(rate.response))
