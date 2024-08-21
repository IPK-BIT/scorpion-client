import requests
from pluggy import HookimplMarker

hookimpl = HookimplMarker("data_source")

class Dimensions:
    """
    Plugin for Dimensions data source.
    """
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
    
    @hookimpl
    def extract(self, config: dict):
        """
        Extract data from Dimensions.
        
        Parameters:
            config (dict): Configuration for the data source.
        
        Returns:
            data (Any): Extracted data
        """
        return {'citations': 42}

    @hookimpl
    def transform(self, data):
        """
        Transform the data.
        
        Parameters:
            data (Any): Extracted data.
        
        Returns:
            data (Any): Transformed data.
        """
        return {'Citations': 42}
                            