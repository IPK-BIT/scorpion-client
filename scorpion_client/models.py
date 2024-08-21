from pydantic import BaseModel

class UserDetails(BaseModel):
    """
    User details object.
    
    Attributes:
        user_name (str): User name.
        email (str): Email address.
        is_admin (bool): Admin status.
        providers (list[str]): List of providers.
    """
    user_name: str
    email: str
    is_admin: bool
    providers: list[str]
    
class Service(BaseModel):
    """
    Service object.
    
    Attributes:
        abbreviation (str): Abbreviation of the service.
        name (str): Name of the service.
        category (str): Category of the service.
        provider (str): Provider of the service.
        license (str): License of the service.
        consortia (list[str]): Consortia of the
    """
    abbreviation: str
    name: str
    category: str
    provider: str
    license: str|None
    consortia: list[str]

class IndicatorValue(BaseModel):
    """
    Indicator value object.
    
    Attributes:
        kpi (str): Key performance indicator.
        date (str): Date of the value.
        value (int|None): Value of the key performance indicator.
    """    
    kpi: str
    date: str
    value: int|None
    
class Indicator(BaseModel):
    """
    Indicator object.
    
    Attributes:
        name (str): Name of the indicator.
        necessity (str): Necessity of the indicator.
        description (str): Description of the indicator.
    """
    name: str
    necessity: str
    description: str
