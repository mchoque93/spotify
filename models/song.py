from dataclasses import dataclass, field


@dataclass
class Song:
    name: str
    artist_name: field(default_factory=list)