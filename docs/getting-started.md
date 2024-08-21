# Getting Started

## Simple Example

This guide helps you set up an automatic KPI submission to Scorpion using Matomo and Dimensions. You can use this guide as a starting point and adapt it to your setup.
After this tutorial, you will have a project structure similar to this:

```console
scorpion-submission/
├── .env
└── main.py
```

### .env

First, you need to create a .env file to store sensitive information such as API keys, database credentials, etc., securely. This file should not be committed to version control systems like Git for security reasons.

```title=".env"
API_KEY='YOUR-API-KEY'
BASE_URL='https://scorpion.bi.denbi.de'
SERVICE_NAME='YOUR-SERVICE-ABBREVIATION'
MATOMO_AUTH_TOKEN='YOUR-MATOMO-AUTH-TOKEN'
MATOMO_BASE_URL='https://matomo.cloud'
MATOMO_SITE_ID='42'
DIMENSIONS_BASE_URL='https://app.dimensions.ai'
DIMENSIONS_API_KEY='YOUR-DIMENSIONS-API-KEY'
```

### main.py

Now, let's write a simple Python script that uses the Scorpion Client to perform some operations. This example assumes you're interacting with an API provided by Scorpion.

```py title="main.py"
import os
import datetime
from dotenv import load_dotenv
from scorpion_client import ScorpionClient, DataSource
from scorpion_client.data_sources.matomo import Matomo
from scorpion_client.data_sources.dimensions import Dimensions

if __name__ == '__main__':
    load_dotenv()
    matomo = DataSource('matomo', Matomo(os.getenv('MATOMO_BASE_URL'), os.getenv('MATOMO_AUTH_TOKEN')))
    web_stat_data = matomo.extract({'site_id': os.getenv('MATOMO_SITE_ID'), 'period': 'month', 'date': 'lastMonth'})
    web_stats = matomo.transform(web_stat_data)

    dimensions = DataSource('dimensions', Dimensions(os.getenv('DIMENSIONS_BASE_URL'), os.getenv('DIMENSIONS_API_KEY')))
    citations_data = dimensions.extract({})
    citations = dimensions.transform(citations_data)

    results = {
        **web_stats,
        **citations
    }

    client = ScorpionClient(os.getenv('BASE_URL'), os.getenv('API_KEY'))
    service = client.get_service(os.getenv('SERVICE_NAME'))

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    form = client.prepare_indicator_form(service, [yesterday.strftime('%Y-%m')])
    for measurement in form:
        measurement.value = results[measurement.kpi]    

    client.send_measurements(os.getenv('SERVICE_NAME'), form)
```

### Cron Job

To run your script automatically at regular intervals, you can use cron jobs on Unix-based systems (Linux, macOS).

1. Open Terminal/Cron Tab: Open your terminal or access the crontab editor by typing `crontab -e`.
2. Add a Cron Job: Add a line to schedule your script. For example, to run the script every first day of a month at midnight, add:

```sh
0 0 1 * * cd /home/ubuntu/scorpion-submission && source /home/ubuntu/.venv/myenv/bin/activate && python3 main.py
```