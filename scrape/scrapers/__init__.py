from abc import ABC, abstractmethod

class Scraper(ABC):
    @abstractmethod
    async def scrape(self):
        """
        Fetch replay data asynchronously.
        Should return a list of dictionaries with keys:
        - file_name: Name of the replay file (e.g., replay ID).
        - data: Binary content of the replay file.
        """
        pass
