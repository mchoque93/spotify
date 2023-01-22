from dataclasses import dataclass, field


@dataclass
class Artist:
    name: str
    genres: field(default_factory=list)
