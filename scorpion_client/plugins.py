from pluggy import HookspecMarker

hookspec = HookspecMarker("data_source")

class DataSourcePlugin:
    """
    Base class for all data source plugins.
    """
    @hookspec
    def extract(self, config: dict):
        """
        Extract data from the data source.
        
        Parameters:
            config (dict): Configuration for the data source.
        
        Returns:
            data (Any): Extracted data
        """
        raise NotImplementedError

    @hookspec
    def transform(self, data):
        """
        Transform the data.
        
        Parameters:
            data (Any): Extracted data.
        
        Returns:
            data (Any): Transformed data.
        """
        raise NotImplementedError