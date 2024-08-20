import requests
from . import models
from urllib.parse import urljoin
from pluggy import PluginManager
from .plugins import DataSourcePlugin

class DataSource:
    def __init__(self, name: str, plugin: DataSourcePlugin):
        self.__pm__ = PluginManager('data_source')
        self.__pm__.add_hookspecs(DataSourcePlugin)
        self.__name__ = name
        self.__pm__.register(plugin, name)
    
    def extract(self, config: dict):
        plugin_impl: DataSourcePlugin = self.__pm__.get_plugin(self.__name__)
        return plugin_impl.extract(config)
    
    def transform(self, data):
        plugin_impl: DataSourcePlugin = self.__pm__.get_plugin(self.__name__)
        return plugin_impl.transform(data)

class ScorpionClient:
    def __init__(self, base_url, api_key):
        self.__session__ = __ServerSession__(base_url)
        self.__session__.headers.update({'X-API-KEY': api_key})

    def get_user_details(self) -> models.UserDetails:
        response = self.__session__.get('/aai/details')
        return models.UserDetails(**response)
    
    def get_service(self, abbreviation: str) -> models.Service:
        params = {
            'service': abbreviation
        }
        response = self.__session__.get('/api/v1/services', params=params)
        return models.Service(**response['result'][0])
    
    def get_services(self) -> list[models.Service]:
        params = {
            'provider': ','.join(self.get_user_details().providers)
        }
        response = self.__session__.get('/api/v1/services', params=params)
        return [models.Service(**service) for service in response['result']]
    
    def get_all_services(self) -> list[models.Service]:
        response = self.__session__.get('/api/v1/services')
        return [models.Service(**service) for service in response['result']]

    def get_service_indicators(self, service: models.Service) -> list[models.Indicator]:
        params = {
            'service': service.abbreviation
        }
        response = self.__session__.get('/api/v1/indicators', params=params)
        indicator_set = []
        for indicator in [indicator for indicator in response['result'] if indicator['selected']]:
            for category in [category for category in indicator['categories'] if category['name'] == service.category]:
                indicator_set.append(models.Indicator(
                    name=indicator['name'],
                    necessity=category['necessity'] if category['necessity'] else 'optional',
                    description=indicator['description']
                ))
        return indicator_set

    def get_category_indicators(self, category: str) -> list[models.Indicator]:
        params = {
            'category': category
        }
        response = self.__session__.get('/api/v1/indicators', params=params)
        indicator_set = []
        for indicator in [indicator for indicator in response['result'] if indicator['selected']]:
            indicator_set.append(models.Indicator(
                name=indicator['name'],
                necessity=indicator['categories'][0]['necessity'],
                description=indicator['description']
            ))
        return indicator_set
        
    def prepare_indicator_form(self, service: models.Service, dates: list[str]) -> list[models.IndicatorValue]:
        form = []
        indicators = self.get_service_indicators(service)
        for date in dates:
            for indicator in indicators:
                form.append(models.IndicatorValue(
                    kpi=indicator.name,
                    date=date,
                    value=None
                ))
        return form
    
    def send_measurements(self, abbreviation: str, form: list[models.IndicatorValue]):
        params = {
            'service': abbreviation
        }
        data = [indicator.model_dump() for indicator in form]
        self.__session__.post('/api/v1/measurements', json=data, params=params)
    
    def get_measurements(self, abbreviation: str, indicator: str|None, start_date: str, end_date: str) -> list[models.IndicatorValue]:
        params = {
            'service': abbreviation,
            'start_date': start_date+'T00:00:00Z',
            'indicators': indicator,
            'end_date': end_date+'T23:59:59Z'
        }
        response = self.__session__.get('/api/v1/measurements', params=params)
        return [models.IndicatorValue(**indicator) for indicator in response['result']]

class __ServerSession__(requests.Session):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        response = super().request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response.json()