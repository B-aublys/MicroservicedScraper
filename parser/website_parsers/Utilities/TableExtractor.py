
class TableExtractor:
    """Generic helper for extracting data from HTML tables"""
    
    @staticmethod
    def extract_from_table(table, label: str) -> str | None:
        if not table:
            return None
        
        rows = table.find_all('tr')
        for row in rows:
            th = row.find('th')
            if th and label in th.get_text():
                td = row.find('td')
                return td.get_text(strip=True) if td else None
        return None
