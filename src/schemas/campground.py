from pydantic import BaseModel, Field
from pydantic import BaseModel
from typing import List, Literal


class FetchCampgroundsRequest(BaseModel):
    component: Literal['US', 'TR']
    sort: Literal['Recommended', 'Name']
    page_number: int = Field(
        1, ge=1, le=5, description="Page number must be between 1 and 5")
    page_size: int = Field(
        1, ge=1, le=500, description="Page size must be between 1 and 500")
    insert_db: bool = False

    def to_params(self) -> dict:
        '''Convert the request object to a dictionary of parameters'''
        bbox = '-101.792,18.75,-90.93,52.334' if self.component == 'US' else '-101.792,18.75,-90.93,52.334'
        sort_ = 'recommended' if self.sort == 'Recommended' else 'name-raw'
        return {
            "filter[search][bbox]": bbox,
            "sort": sort_,
            "page[number]": self.page_number,
            "page[size]": self.page_size
        }


class FetchCampgroundsResponse(BaseModel):
    data: List[dict]
    meta: dict
    links: dict


class PaginationParams(BaseModel):
    page_size: int = Field(10, ge=1, le=100)
    page_number: int = Field(0, ge=0)

    class Config:
        schema_extra = {
            "example": {
                "page_size": 10,
                "page_number": 0
            }
        }
