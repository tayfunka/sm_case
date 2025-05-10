from pydantic import BaseModel
from typing import List


class FetchCampgroundsRequest(BaseModel):
    bbox: str = '-101.792,18.75,-90.93,52.334'
    sort: str = 'recommended'
    page_number: int = 1
    page_size: int = 1
    insert_db: bool = False

    def to_params(self) -> dict:
        '''Convert the request object to a dictionary of parameters'''
        return {
            "filter[search][bbox]": self.bbox,
            "sort": self.sort,
            "page[number]": self.page_number,
            "page[size]": self.page_size
        }


class FetchCampgroundsResponse(BaseModel):
    data: List[dict]
    meta: dict
    links: dict
