from pydantic import BaseModel
from typing import Optional

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
    pH: Optional[int]
    O: Optional[int]
    I: Optional[str]
    M: Optional[int]
    Thw: Optional[int]
    Ka: Optional[int]
    SAR: Optional[int]
    IIWP_Dc: Optional[int]
    Tr: Optional[int]
    Fl: Optional[int]
    Fa: Optional[int]