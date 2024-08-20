import requests
from pluggy import HookimplMarker

hookimpl = HookimplMarker("data_source")

class Matomo:
    """Plugin for Matomo data source."""

    def __init__(self, base_url, auth_token, mapping=None):
        self.base_url = base_url
        self.auth_token = auth_token
        if mapping:
            self.mapping = mapping
        else:
            self.mapping = {
                'avg_time_on_site': 'Visits Duration',
                'bounce_count': None,
                'bounce_rate': None,
                'max_actions': None,
                'nb_actions': 'Actions',
                'nb_actions_per_visit': 'Actions per Visit',
                'nb_uniq_visitors': 'Visitors',
                'nb_users': None,
                'nb_visits': 'Visits',
                'nb_visits_converted': None,
                'sum_visit_length': None
            }
    
    @hookimpl
    def extract(self, config: dict):
        """Extract data from Matomo."""
        params = {
            'module': 'API',
            'method': 'VisitsSummary.get',
            'idSite': config['site_id'],
            'period': config['period'],
            'date': config['date'],
            'format': 'json'
        }
        response = requests.post(f'{self.base_url}', params=params, data={
            'token_auth': self.auth_token
        })
        response.raise_for_status()       
        return response.json()
    
    @hookimpl
    def transform(self, data):
        """Transform the data."""
        result = {}
        for key, value in data.items():
            if key in self.mapping:
                if self.mapping[key]:
                    result[self.mapping[key]] = round(value)
        return result