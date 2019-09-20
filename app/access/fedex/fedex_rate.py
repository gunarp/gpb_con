import json
import re
import xml.etree.ElementTree as ET
from zeep import Client, Settings
from zeep.exceptions import Fault, TransportError, XMLSyntaxError

import pandas as pd
from zeep.helpers import serialize_object

settings = Settings(strict=False, xml_huge_tree=False)
client = Client('RateService_v26.wsdl', settings=settings)

with open("../creds/creds.json", "r") as f:
    credentials = json.load(f)['fedex']

RateRequestDict = {
    "WebAuthenticationDetail": {
        "UserCredential": {
            "Key": credentials['api_key'],
            "Password": credentials['password']
        }
    },
    "ClientDetail": {
        "AccountNumber": credentials['ship_num'],
        "MeterNumber": credentials['meter_num']
    },
    "Version": {
        "ServiceId": "crs",
        "Major": 26,
        "Intermediate": 0,
        "Minor": 0
    },
    "RequestedShipment": {
        "DropoffType": "REGULAR_PICKUP",
        "PackagingType": "YOUR_PACKAGING",
        "TotalWeight": {
            "Units": "LB",
            "Value": 1.0
        },
        "Shipper": {
            "Contact": {
                "CompanyName": "GP"
            },
            "Address": {
                "PostalCode": 98007,
                "CountryCode": "US"
            }
        },
        "Recipient": {
            "Address": {
                "PostalCode": 98007,
                "CountryCode": "US"
            }
        },
        "ShippingChargesPayment": {
            "PaymentType": "SENDER",
            "Payor": {
                "ResponsibleParty": {
                    "AccountNumber": credentials['ship_num'] #TODO@@@
                }
            }
        },
        "RateRequestTypes": "LIST",
        "PackageCount": 1,
        "RequestedPackageLineItems": {
            "SequenceNumber": 1,
            "GroupNumber": 1,
            "GroupPackageCount": 1,
            "Weight": {
                "Units": "LB",
                "Value": 1
            },
            "Dimensions": {
                "Length": 1,
                "Width": 1,
                "Height": 1,
                "Units": "IN"
            }
        }
    }
}

# print(client.serivce)
try:
    # with open('output3.txt', 'w') as f:
    #     f.write(str(client.service.getRates(**RateRequestDict)))
    rates = (client.service.getRates(**RateRequestDict))['RateReplyDetails']
    # with open ('poop.txt', 'w') as f:
    #     pkg = rates[0]['RatedShipmentDetails']
    #     f.write(str(list(enumerate(pkg, 0))))
    
    for rate in rates:
        pkg = rate['RatedShipmentDetails'][0]['RatedPackages'][0]['PackageRateDetail']
        out = rate['ServiceType'] + ' '  + \
              str(pkg['NetCharge']['Amount']) + ' ' + \
              str(pkg['BillingWeight']['Value']) + ' ' + \
              str(pkg['TotalRebates']['Amount'])
        print(out)
    
except Fault as error:
    print(ET.tostring(error.detail))