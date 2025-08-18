from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Page:
    type: str
    filepath: Optional[str] = None
    tab_name: Optional[str] = None


@dataclass
class Book:
    id: str
    pages: List[Page]
