import re

class NumberExtractor:
    @staticmethod
    def int_from_text(text: str) -> int | None:
        """Extract the first integer from a string."""
        match = re.search(r'\d+', text)
        return int(match.group()) if match else None

    @staticmethod
    def float_from_text(text: str) -> float | None:
        """Extract the first float from a string."""
        match = re.search(r'\d+(?:\.\d+)?', text)
        return float(match.group()) if match else None