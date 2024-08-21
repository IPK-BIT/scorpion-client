import requests
from . import models
from urllib.parse import urljoin
from pluggy import PluginManager
from .plugins import DataSourcePlugin

class ScorpionClient:
    """
    `ScorpionClient` is a client for the Scorpion API. It provides methods to interact with the API.
    """
    
    def __init__(self, base_url, api_key):
        """
        Initializes a new ScorpionClient instance.

        Parameters:
            base_url (str): Base URL of the Scorpion API.
            api_key (str): API key for authentication.
            
        Examples:
            >>> client = ScorpionClient(os.getenv('SCORPION_API_URL'), os.getenv('SCORPION_API_KEY'))
        """
        self.__session__ = __ServerSession__(base_url)
        self.__session__.headers.update({'X-API-KEY': api_key})

    def get_user_details(self) -> models.UserDetails:
        """
        Retrieves details about the current user.

        Returns:
            UserDetails: User details object.
        
        Examples:
            >>> client.get_user_details()
        """
        response = self.__session__.get('/aai/details')
        return models.UserDetails(**response)
    
    def get_service(self, abbreviation: str) -> models.Service:
        """
        Retrieves details about a service.
        
        Parameters:
            abbreviation (str): Abbreviation of the service.
        
        Returns:
            service (models.Service): Service object.
        
        Examples:
            >>> client.get_service('TEST')
        """
        params = {
            'service': abbreviation
        }
        response = self.__session__.get('/api/v1/services', params=params)
        return models.Service(**response['result'][0])
    
    def get_services(self) -> list[models.Service]:
        """
        Retrieves details about the services available to the user.
            
        Returns:
            services (list[models.Service]): List of service objects.
        
        Examples:
            >>> client.get_services()
        """
        params = {
            'provider': ','.join(self.get_user_details().providers)
        }
        response = self.__session__.get('/api/v1/services', params=params)
        return [models.Service(**service) for service in response['result']]
    
    def get_all_services(self) -> list[models.Service]:
        """
        Retrieves details about all services.
        
        Returns:
            services (list[models.Service]): List of service objects.
        
        Examples:
            >>> client.get_all_services()
        """
        response = self.__session__.get('/api/v1/services')
        return [models.Service(**service) for service in response['result']]

    def get_service_indicators(self, service: models.Service) -> list[models.Indicator]:
        """
        Retrieves indicators for a service.
        
        Parameters:
            service (models.Service): Service object.
        
        Returns:
            indicators (list[models.Indicator]): List of indicator objects.
        
        Examples:
            >>> client.get_service_indicators(service)
        """
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
        """
        Retrieves indicators for a category.
        
        Parameters:
            category (str): Category of the indicators.
            
        Returns:
            indicators (list[models.Indicator]): List of indicator objects.
        
        Examples:
            >>> client.get_category_indicators('Database')
        """
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
        """
        Prepares a form for submitting measurements.
        
        Parameters:
            service (models.Service): Service object.
            dates (list[str]): List of dates for the form.
            
        Returns:
            form (list[models.IndicatorValue]): List of indicator value objects.
        
        Examples:
            >>> client.prepare_indicator_form(service, ['2024-01-01', '2024-01-02'])
        """
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
        """
        Sends measurements to the API.
        
        Parameters:
            abbreviation (str): Abbreviation of the service.
            form (list[models.IndicatorValue]): List of indicator value objects.
            
        Examples:
            >>> client.send_measurements('service', form)
        """
        params = {
            'service': abbreviation
        }
        data = [indicator.model_dump() for indicator in form]
        self.__session__.post('/api/v1/measurements', json=data, params=params)
    
    def get_measurements(self, abbreviation: str, indicator: str|None, start_date: str, end_date: str) -> list[models.IndicatorValue]:
        """
        Retrieves measurements for a service.
        
        Parameters:
            abbreviation (str): Abbreviation of the service.
            indicator (str|None): Indicator name.
            start_date (str): Start date.
            end_date (str): End date.
            
        Returns:
            measurements (list[models.IndicatorValue]): List of indicator value objects.
        
        Examples:
            >>> client.get_measurements('service', 'indicator', '2021-01-01', '2021-12-31')
        """
        params = {
            'service': abbreviation,
            'start_date': start_date+'T00:00:00Z',
            'indicators': indicator,
            'end_date': end_date+'T23:59:59Z'
        }
        response = self.__session__.get('/api/v1/measurements', params=params)
        return [models.IndicatorValue(**indicator) for indicator in response['result']]

class DataSource:
    """
    `DataSource` is a class that provides a way to interact with data sources. It is used to extract and transform data from different sources.
    """
    
    def __init__(self, name: str, plugin: DataSourcePlugin):
        """
        Initializes a new DataSource instance.
        
        Parameters:
            name (str): Name of the data source.
            plugin (DataSourcePlugin): Plugin implementation for the data source.
        
        Examples:
            >>> data_source = DataSource('matomo', data_sources.matomo.Matomo('http://matomo.cloud', 'auth_token'))
        """
        self.__pm__ = PluginManager('data_source')
        self.__pm__.add_hookspecs(DataSourcePlugin)
        self.__name__ = name
        self.__pm__.register(plugin, name)
    
    def extract(self, config: dict):
        """
        Extracts data from the data source.
        
        Parameters:
            config (dict): Configuration for the data source.
            
        Returns:
            data (Any): Extracted data.
        
        Examples:
            >>> data_source.extract({'url': 'http://example.com', 'auth_token': 'auth_token'})
        """
        plugin_impl: DataSourcePlugin = self.__pm__.get_plugin(self.__name__)
        return plugin_impl.extract(config)
    
    def transform(self, data):
        """
        Transforms the extracted data.
        
        Parameters:
            data (Any): Extracted data.
            
        Returns:
            data (Any): Transformed data.
        
        Examples:
            >>> data_source.transform({'citations': 42})
        """
        plugin_impl: DataSourcePlugin = self.__pm__.get_plugin(self.__name__)
        return plugin_impl.transform(data)

class __ServerSession__(requests.Session):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *Parameters, **kwParameters):
        url = urljoin(self.base_url, url)
        response = super().request(method, url, *Parameters, **kwParameters)
        response.raise_for_status()
        return response.json()