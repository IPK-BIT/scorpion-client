from pluggy import HookspecMarker

hookspec = HookspecMarker("data_source")

class DataSourcePlugin:
    """Base class for all data source plugins."""

    @hookspec
    def extract(self, config: dict):
        """Extract data from the data source."""
        raise NotImplementedError

    @hookspec
    def transform(self, data):
        """Transform the data."""
        raise NotImplementedError