import re
from app.models import UPS, Fedex
import pandas as pd
from app.access.ups.ups_rate import get_rates as ups
from app.access.fedex.fedex_rate import get_rates as fed

def ups_rates(user, params):
    user = UPS.query.filter_by(user_id=user.id).first_or_404()
    acct = (user.username, user.password, user.api_key, user.ship_num)
    ups_dom = {
        "UPS Ground": "03",
        "UPS 3 Day Select": "12",
        "UPS 2nd Air AM": "59",
        "UPS 2nd Air": "02",
        "UPS Next Day Air Early": "14",
        "UPS Next Day Air": "01",
        "UPS Next Day Air Saver": "13"
    }
    
    rates = pd.DataFrame(columns=["Carrier", "Service", "Billable Weight",
                                  "Our Rate", "Published Rate"])
    for service_code in ups_dom:
        rate_info = ups(acct, params, ups_dom[service_code])
        # If something bad happens to the request, stop
        if not isinstance(rate_info, list):
            return rate_info
        
        rates.loc[service_code] = \
            pd.Series({'Carrier': 'UPS', 'Service':re.sub('UPS ', '', service_code),
                       'Billable Weight': rate_info[0],
                       'Our Rate': rate_info[1], 'Published Rate': rate_info[2]})

    return rates.set_index(['Carrier', 'Service'])

def fedex_rates(user, params):
    user = Fedex.query.filter_by(user_id=user.id).first_or_404()
    acct = (user.password, user.api_key, user.ship_num, user.meter_num)
    rates = fed(acct, params)
    
    def format(service):
        tmp = re.sub('_', ' ', service).title()
        tmp = re.sub('Am', 'AM', tmp)
        return re.sub('Fedex ', '', tmp)
    
    rates['Service'] = rates['Service'].apply(format)
    
    return rates[::-1].set_index(['Carrier', 'Service'])
