from dataclasses import field, dataclass


@dataclass
class Genre:
    genre: field(default_factory=list)
