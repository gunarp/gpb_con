import json
import xml.etree.ElementTree as ET
from zeep import Client, Settings
from zeep.exceptions import Fault, TransportError, XMLSyntaxError

def get_rates():
    # Set Connection
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client('app/access/ups/SCHEMA-WSDLs/RateWS.wsdl', settings=settings)
    with open('app/access/creds/ups.json', 'r') as f:
        credentials = json.load(f)['credentials']

    # Set SOAP headers
    headers = {

        'UPSSecurity': {
            'UsernameToken': {
                'Username': credentials['username'],
                'Password': credentials['password']
            },

            'ServiceAccessToken': {
                'AccessLicenseNumber': credentials['api_key']
            }

        }
    }

    # Create request dictionary
    requestDictionary = {

        "RequestOption": "Rate",
        "TransactionReference": {
            "CustomerContext": "Your Customer Context"
        }
    }

    # Create rate request dictionary
    rateRequestDictionary = {

        "Package": {
            "Dimensions": {
                "Height": "10",
                "Length": "5",
                "Width": "4",
                "UnitOfMeasurement": {
                    "Code": "IN",
                    "Description": "inches"
                }
            },
            "PackageWeight": {
                "UnitOfMeasurement": {
                    "Code": "Lbs",
                    "Description": "pounds"
                },
                "Weight": "1"
            },
            "PackagingType": {
                "Code": "02",
                "Description": "Rate"
            }
        },
        "Service": {
            "Code": "03",
            "Description": "Service Code"
        },
        "ShipFrom": {
            "Address": {
                "AddressLine": [
                    "14725 nE 20th St Ste D",
                ],
                "City": "Bellevue",
                "CountryCode": "US",
                "PostalCode": "98007",
                "StateProvinceCode": "WA"
            },
            "Name": "Name"
        },
        "ShipTo": {
            "Address": {
                "CountryCode": "US",
                "PostalCode": "91732",
                "StateProvinceCode": "CA"
            },
            "Name": "Ranc"
        },
        "Shipper": {
            "Address": {
                "AddressLine": [
                    "14725 NE 20th St Ste D",
                ],
                "City": "Bellevue",
                "CountryCode": "US",
                "PostalCode": "98007",
                "StateProvinceCode": "WA"
            },
            "ShipperNumber": credentials['ship_num']
        },
            "ShipmentRatingOptions": {
                "NegotiatedRatesIndicator": ""
        }
    }

    # Try operation
    try:
        response = client.service.ProcessRate(_soapheaders=headers, Request=requestDictionary,
                                            Shipment=rateRequestDictionary)
        return(response['RatedShipment'])

    except Fault as error:
        print(ET.tostring(error.detail))
