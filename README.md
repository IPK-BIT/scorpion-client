# Scorpion Client

This project is a high-level interface designed to interact with the API of [Scorpion](https://github.com/IPK-BIT/scorpion). It provides a convenient way to access and utilize the functionalities of the Scorpion API. Additionally, it includes plugins that enable the extraction of key performance indicators (KPIs) from various monitoring systems. These plugins allow users to easily extract and transform KPI measurements to submit them to Scorpion.

## Installation

### From release

To install the Scorpion Client from the release, follow these steps:

1. Download the relevant file from: `https://github.com/IPK-BIT/scorpion-client/releases`
2. Install the dependecy with: `pip install /path/to/package.tar.gz` or `pip install /path/to/package.whl`


### From Source 

To install the Scorpion Client from source, follow these steps:

1. Clone the repository: `git clone https://github.com/IPK-BIT/scorpion-client.git`
2. Navigate to the project directory: `cd scorpion-client`
3. Install the project dependencies: `poetry install`

## Usage

### Basic Usage

To interact with the Scorpion API, create and use the Scorpion Client as follows:
```py
from scorpion_client import ScorpionClient

client = ScorpionClient(os.getenv('BASE_URL'), os.getenv('API_KEY'))
services = client.getServices()

print(services)
```

### Data Sources

Scorpion Client includes features to interact with monitoring systems to extract and transform the KPI measurements from. Those features are made available through a Plugin Interface and can be used as follows:

```py
from scorpion_client import DataSource
from scorpion_client.data_sources.matomo import Matomo

matomo = DataSource('matomo', Matomo(os.getenv('MATOMO_BASE_URL'), os.getenv('MATOMO_AUTH_TOKEN')))
web_stat_data = matomo.extract({'site_id': os.getenv('MATOMO_SITE_ID'), 'period': 'month', 'date': 'today'})
web_stats = matomo.transform(web_stat_data)
```

## Contributing

Contributions are welcome! If you would like to contribute to the Scorpion Client, please follow these guidelines:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m "Add your changes"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
