from icecream import ic

import requests
from pluggy import HookimplMarker

hookimpl = HookimplMarker("data_source")

class NocoDB:
    """Plugin for Matomo data source."""

    def __init__(self, base_url, auth_token, mapping=None):
        self.base_url = base_url
        self.auth_token = auth_token
        if mapping:
            self.mapping = mapping
        else:
            self.mapping = {
                'Visits': 'Visits',
            }
    
    @hookimpl
    def extract(self, config: dict):
        """Extract data from Matomo."""
        url = f"{self.base_url}tables/muok9y2gaj515xy/records"

        headers = {"xc-token": self.auth_token}

        response = requests.request("GET", url, headers=headers, params=config)

        return response.json()
    
    @hookimpl
    def transform(self, data):
        """Transform the data."""
        
        result = {}
        for record in data['list']:
            for key in self.mapping:
                result[self.mapping[key]] = record['Value']
            
        return result