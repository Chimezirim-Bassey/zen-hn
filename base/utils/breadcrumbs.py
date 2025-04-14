from dataclasses import dataclass


@dataclass
class BreadCrumb:
    name: str
    url: str
