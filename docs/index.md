# Welcome to the Documentation of the Scorpion Client!

Welcome to the documentation for the Scorpion Client, a Python package designed to facilitate interaction with the Scorpion API. This high-level interface simplifies accessing and utilizing the functionalities of the Scorpion API, including the extraction of key performance indicators (KPIs) from various monitoring systems through plugins.

## Installation
To get started with Scorpion Client, you can install it using pip. You have two options for installation:

### From Release
If you prefer to install from a release, download the package from the GitHub releases page and install it using pip:

```bash
pip install /path/to/package.tar.gz
```
or

```bash
pip install /path/to/package.whl
```

### From Source
Alternatively, you can clone the repository and install it from source:

```bash
git clone https://github.com/IPK-BIT/scorpion-client.git
cd scorpion-client
pip install .
```

## Basic Usage
Here's how you can start interacting with the Scorpion API using the Scorpion Client:

```py title="main.py"
from scorpion_client import ScorpionClient

client = ScorpionClient(os.getenv('BASE_URL'), os.getenv('API_KEY'))
services = client.getServices()

print(services)
```

This example demonstrates creating a ScorpionClient instance with your base URL and API key, then fetching and printing the available services.

### Data Sources
Scorpion Client also supports interaction with various data sources through its plugin interface. Here's an example of how to use it with Matomo:

```py title="main.py"
from scorpion_client import DataSource
from scorpion_client.data_sources.matomo import Matomo

matomo = DataSource('matomo', Matomo(os.getenv('MATOMO_BASE_URL'), os.getenv('MATOMO_AUTH_TOKEN')))
web_stat_data = matomo.extract({'site_id': os.getenv('MATOMO_SITE_ID'), 'period': 'month', 'date': 'today'})
web_stats = matomo.transform(web_stat_data)
```

This snippet shows how to set up a data source for Matomo, extract web statistics, and transform the data for further analysis.

## Contributing
We welcome contributions to enhance the Scorpion Client. To contribute, please follow these steps:

-   Fork the repository.
-   Create a new branch for your feature: git checkout -b feature/your-feature-name.
-   Make your changes and commit them: git commit -m "Add your changes".
-   Push to the branch: git push origin feature/your-feature-name.

## License
Scorpion Client is licensed under the MIT License. See the LICENSE file for more details.

This documentation provides a starting point for using the Scorpion Client. For more detailed information, refer to the individual modules and classes within the package.