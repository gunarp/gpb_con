import json
import xml.etree.ElementTree as ET
from zeep import Client, Settings
from zeep.exceptions import Fault, TransportError, XMLSyntaxError

def get_rates(params, service_code):
    # Set Connection
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client('app/access/ups/SCHEMA-WSDLs/RateWS.wsdl', settings=settings)
    # client = Client('SCHEMA-WSDLs/RateWS.wsdl', settings=settings)

    # Get login info
    with open('app/access/creds/ups.json', 'r') as f:
    # with open('../creds/ups.json') as f:
        credentials = json.load(f)['credentials']

    # Get dimensions and location
    zipcode, weight, length, width, height = params

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
                "Height": height,
                "Length": length,
                "Width": width,
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
                "Weight": weight
            },
            "PackagingType": {
                "Code": "02",
                "Description": "Rate"
            }
        },
        "Service": {
            "Code": service_code,
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
                "PostalCode": zipcode,
            }
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
        # return(response['RatedShipment'][0])
        response = response['RatedShipment'][0]
        return([response['BillingWeight']['Weight'],
                response['NegotiatedRateCharges']['TotalCharge']['MonetaryValue'],
                response['RatedPackage'][0]['TotalCharges']['MonetaryValue']])

    except Fault as error:
        print(ET.tostring(error.detail))

if __name__ == "__main__":
    d = [98008, 1, 1, 1, 1]
    rates = get_rates(d, "59")
    print(rates)
