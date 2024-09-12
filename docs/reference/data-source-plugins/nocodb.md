# NocoDB

!!! warning 
    
    Not yet implemented

## Plugin configuration
Takes as input for instantiation the base URL, the auth token and optionally a mapping from the NocoDB indicators to the Scorpion indicators. By default a mapping to the indicator names for the hosted instance is used. This default mapping looks as follows:

```py
#  NOT YET IMPLEMENTED
```


## Usage

```py title="main.py"
nocodb = DataSource('nocodb', NocoDB(os.getenv('NOCODB_BASE_URL'), os.getenv('NOCODB_AUTH_TOKEN')))
nocodb_data = nocodb.extract({'offset': 0, 'limit': 25, 'viewId': os.getenv('NOCODB_VIEW_ID')})
nocodb_stats = nocodb.transform(nocodb_data)
```

### `extract(self, config)`

Configuration options:

| Parameter  | Type    | Description                          |
| ---------------- |---------| ------------------------------------ |
| `fields`         | string  | Allows you to specify the fields that you wish to include in your API response. By default, all the fields are included in the response. <br><br>**Example**: `fields=field1,field2` will include only 'field1' and 'field2' in the API response.<br><br>Please note that it's essential not to include spaces between field names in the comma-separated list.  |
| `sort`           | string  | Allows you to specify the fields by which you want to sort the records in your API response. By default, sorting is done in ascending order for the designated fields. To sort in descending order, add a '-' symbol before the field name. <br><br>**Example**: `sort=field1,-field2` will sort the records first by 'field1' in ascending order and then by 'field2' in descending order.If viewId query parameter is also included, the sort included here will take precedence over any sorting configuration defined in the view.<br><br>Please note that it's essential not to include spaces between field names in the comma-separated list. |
| `where`          | string  | Enables you to define specific conditions for filtering records in your API response. Multiple conditions can be combined using logical operators such as 'and' and 'or'. Each condition consists of three parts: a field name, a comparison operator, and a value.<br><br>**Example**: `where=(field1,eq,value1)~and(field2,eq,value2)` will filter records where 'field1' is equal to 'value1' AND 'field2' is equal to 'value2'.<br><br>You can also use other comparison operators like 'ne' (not equal), 'gt' (greater than), 'lt' (less than), and more, to create complex filtering rules.<br><br>If `viewId` query parameter is also included, then the filters included here will be applied over the filtering configuration defined in the view.<br><br>Please remember to maintain the specified format, and do not include spaces between the different condition components |
| `offset`         | integer | Enables you to control the pagination of your API response by specifying the number of records you want to skip from the beginning of the result set. The default value for this parameter is set to 0, meaning no records are skipped by default.<br><br>**Example**: `offset=25` will skip the first 25 records in your API response, allowing you to access records starting from the 26th position.<br><br>Please note that the 'offset' value represents the number of records to exclude, not an index value, so an offset of 25 will skip the first 25 records. |
| `limit`          | integer | Enables you to set a limit on the number of records you want to retrieve in your API response. By default, your response includes all the available records, but by using this parameter, you can control the quantity you receive.<br><br>**Example**: `limit=100` will constrain your response to the first 100 records in the dataset. |
| `viewId`         | string  | **View Identifier**. Allows you to fetch records that are currently visible within a specific view. API retrieves records in the order they are displayed if the SORT option is enabled within that view.<br><br>Additionally, if you specify a `sort` query parameter, it will take precedence over any sorting configuration defined in the view. If you specify a `where` query parameter, it will be applied over the filtering configuration defined in the view.<br><br>By default, all fields, including those that are disabled within the view, are included in the response. To explicitly specify which `fields` to include or exclude, you can use the fields query parameter to customize the output according to your requirements. |


### `transform()`

Takes a dictionary containing the response of the NocoDB API for the KPI measurements and transforms this response to a dictionary using the mapping to the Scorpion Indicators.
