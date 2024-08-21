# Matomo

## Plugin configuration
Takes as input for instantiation the base URL, the auth token and optionally a mapping from the matomo indicators to the Scorpion indicators. By default a mapping to the indicator names for the hosted instance is used. This default mapping looks as follows:

```py
{
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
```


## Usage

```py title="main.py"
matomo = DataSource('matomo', Matomo(os.getenv('MATOMO_BASE_URL'), os.getenv('MATOMO_AUTH_TOKEN')))
web_stat_data = matomo.extract({'site_id': os.getenv('MATOMO_SITE_ID'), 'period': 'month', 'date': 'today'})
web_stats = matomo.transform(web_stat_data)
```

### `extract(self, config)`

Configuration options:

- site_id: The integer id of your website, eg. idSite=1 
- period: The period you request the statistics for. Can be any of: day, week, month, year or range. All reports are returned for the dates based on the website's time zone.
    - **day** returns data for a given day.
    - **week** returns data for the week that contains the specified 'date'
    - **month** returns data for the month that contains the specified 'date'
    - **year** returns data for the year that contains the specified 'date'
    - **range** returns data for the specified 'date' range.
- date: Standard format is `YYYY-MM-DD`. Magic keywords are
    - today
    - yesterday
    - lastWeek
    - lastMonth
    - lastYear

### `transform()`

Takes a dictionary containing the extracted KPI measurements and transforms the dictionary keys to the indicator names provided in the mapping.
