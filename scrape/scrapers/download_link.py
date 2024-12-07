import aiohttp
from . import Scraper

class DownloadLink(Scraper):
    def __init__(self, url_formatter, replay_ids):
        """
        :param url_formatter: A function that takes replay_id and returns the download URL.
        :param replay_ids: A list of replay IDs to scrape.
        """
        self.url_formatter = url_formatter
        self.replay_ids = replay_ids

    async def scrape(self):
        fetched_replays = []
        async with aiohttp.ClientSession() as session:
            for replay_id in self.replay_ids:
                try:
                    # Generate the download URL using the formatter function
                    download_url = self.url_formatter(replay_id)
                    print(f"Scraping: {download_url}")

                    async with session.get(download_url) as response:
                        if response.status == 200:
                            replay_data = await response.read()
                            fetched_replays.append({
                                "file_name": f"{replay_id}.SC2Replay",
                                "data": replay_data
                            })
                        else:
                            print(f"Failed to download replay {replay_id}: HTTP {response.status}")
                except Exception as e:
                    print(f"Error fetching replay {replay_id}: {e}")
        return fetched_replays

