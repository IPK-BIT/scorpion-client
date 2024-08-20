from pydantic import BaseModel

class UserDetails(BaseModel):
    user_name: str
    email: str
    is_admin: bool
    providers: list[str]
    
class Service(BaseModel):
    abbreviation: str
    name: str
    category: str
    provider: str
    license: str|None
    consortia: list[str]

class IndicatorValue(BaseModel):
    kpi: str
    date: str
    value: int|None
    
class Indicator(BaseModel):
    name: str
    necessity: str
    description: str
