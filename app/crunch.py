import pandas as pd
from app.access.ups.SoapRate import get_rates

def ups_rates(params):
    ups_dom = {
        "UPS Ground": "03",
        "UPS 3 Day Select": "12",
        "UPS 2nd Air AM": "59",
        "UPS 2nd Air": "02",
        "UPS Next Day Air Early": "14",
        "UPS Next Day Air": "01",
        "UPS Next Day Air Saver": "13"
    }
    
    rates = pd.DataFrame(columns=["Service", "Billable Weight",
                                  "Our Rate", "Published Rate"])
    for service_code in ups_dom:
        rate_info = get_rates(params, ups_dom[service_code])
        rates.loc[service_code] = \
            pd.Series({'Service':service_code, 'Billable Weight': rate_info[0],
                       'Our Rate': rate_info[1], 'Published Rate': rate_info[2]})

    return rates
