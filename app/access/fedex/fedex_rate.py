import json
import re
import os
import xml.etree.ElementTree as ET
from zeep import Client, Settings
from zeep.exceptions import Fault, TransportError, XMLSyntaxError

import pandas as pd
from zeep.helpers import serialize_object

def get_rates(acct, params):
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)

    settings = Settings(strict=False, xml_huge_tree=False)
    client = Client(basedir + '/RateService_v26.wsdl', settings=settings)

    password, api_key, ship_num, meter_num = acct
    zipcode, weight, length, width, height = params

    with open(basedir + "/../creds/creds.json", "r") as f:
        credentials = json.load(f)['fedex']

    RateRequestDict = {
        "WebAuthenticationDetail": {
            "UserCredential": {
                "Key": api_key,
                "Password": password
            }
        },
        "ClientDetail": {
            "AccountNumber": ship_num,
            "MeterNumber": meter_num
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
                    "PostalCode": zipcode,
                    "CountryCode": "US"
                }
            },
            "ShippingChargesPayment": {
                "PaymentType": "SENDER",
                "Payor": {
                    "ResponsibleParty": {
                        "AccountNumber": ship_num #TODO: Change in production
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
                    "Value": weight
                },
                "Dimensions": {
                    "Length": length,
                    "Width": width,
                    "Height": height,
                    "Units": "IN"
                }
            }
        }
    }

    # print(client.serivce)
    try:
        rates = (client.service.getRates(**RateRequestDict))['RateReplyDetails']

        rate_details = pd.DataFrame(columns=["Carrier", "Service", "Billable Weight",
                                             "Our Rate", "Published Rate"])
        
        for rate in rates:
            pkg = rate['RatedShipmentDetails'][0]['RatedPackages'][0]['PackageRateDetail']
            rate = pd.Series({"Carrier": "FedEx",
                              "Service": rate['ServiceType'],
                              "Billable Weight": pkg['BillingWeight']['Value'],
                              "Our Rate": pkg['NetCharge']['Amount'] - pkg['TotalRebates']['Amount'],
                              "Published Rate": pkg['NetCharge']['Amount']})
            rate_details.loc[rate['Service']] = rate
        
        return rate_details

    except Fault as error:
        print(ET.tostring(error.detail))