from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class TOCItem:
    title: str
    page: int
    level: int = 1
    
@dataclass
class EncodedItem:
    toc_item: TOCItem
    locus: str
    actor: str
    imagery: str
    scent_positive: str
    scent_negative: str

@dataclass
class EncodingResult:
    source_file: str
    items: List[EncodedItem] = field(default_factory=list)
