from pydantic import BaseModel
from typing import Optional, Union

class LakeCreate(BaseModel):
    name: str
    region: str
    Z: Optional[int]
    H: Optional[int]
    G: Optional[int]
    A: Optional[int]
    D: Optional[int]
    W: Optional[int]
    T: Optional[int]
    Tw: Optional[int]
    pH: Optional[float]
    O: Optional[int]
    I: Optional[int]
    M: Optional[int]
    Thw: Optional[int]
    Ka: Optional[int]
    SAR: Optional[int]
    IIWP_Dc: Optional[int]
    Tr: Optional[int]
    Fl: Optional[int]
    Fa: Optional[int]


class QualityFilter(BaseModel):
    Z: Optional[Union[int, list]] = None
    H: Optional[Union[int, list]] = None
    G: Optional[Union[int, list]] = None
    A: Optional[Union[int, list]] = None
    D: Optional[Union[int, list]] = None
    W: Optional[Union[int, list]] = None
    T: Optional[Union[int, list]] = None
    Tw: Optional[Union[int, list]] = None
    pH: Optional[Union[float, list]] = None
    O: Optional[Union[int, list]] = None
    I: Optional[Union[int, list]] = None
    M: Optional[Union[int, list]] = None
    Thw: Optional[Union[int, list]] = None
    Ka: Optional[Union[int, list]] = None
    SAR: Optional[Union[int, list]] = None
    IIWP_Dc: Optional[Union[int, list]] = None
    Tr: Optional[Union[int, list]] = None
    Fl: Optional[Union[int, list]] = None
    Fa: Optional[Union[int, list]] = None