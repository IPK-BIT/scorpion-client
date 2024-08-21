# Overview

## Introduction

The scorpion_client package comes with a suite of default plugins that make it easy to handle different data sources. They aim to facilitate the extraction and transformation processes. These plugins are there to help the user to easily connect monitoring systems as data sources. There are lots of different monitoring solutions available. If you find that a plugin for a popular data source is missing, you are welcomed to contribute to the project by developing a new plugin. You can do this by creating a pull request. 

## Writing a plugin

To implement a new plugin, you need to provide a class that implements the hookspecs `data_source` defined in [DataSourcePlugin](../plugins.md). You can use the following template to start.

```py title="my_plugin.py"
from pluggy import HookimplMarker

hookimpl = HookimplMarker("data_source")

class MyPlugin:

    def __init__(self):
        pass
    
    @hookimpl
    def extract(self, config: dict):
        pass
    
    @hookimpl
    def transform(self, data):
        pass
```