from attr import dataclass

@dataclass
class ParseJob:
    """Represents a website parsing job."""
    url: str
    html_content: str
    error: str | None = None

