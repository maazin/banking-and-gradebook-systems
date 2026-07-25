from dataclasses import dataclass
from .enums import Category

@dataclass
class Assignment:
    name: str
    points_earned: float
    points_possible: float
    category: Category

    @property
    def percentage(self) -> float:
        if self.points_possible <= 0:
            raise ValueError ("Assignment has invalid popints possible")
        return(self.points_earned/self.points_possible)*100
