from asyncio import TaskGroup

class ScraperFactory:
    def __init__(self, db_session):
        self.scrapers = []
        self.storage = None
        self.db_session = db_session

    def register_scrapers(self, scrapers):
        self.scrapers.extend(scrapers)

    def set_storage(self, storage):
        self.storage = storage

    async def run(self):
        if not self.storage:
            raise ValueError("No storage configured.")

        replay_ids = []
        async with TaskGroup() as tg:
            for scraper in self.scrapers:
                tg.create_task(self._scrape_and_store(scraper, replay_ids))

        # Perform a single bulk insert for all replay IDs
        if replay_ids:
            await self.db_session.execute(
                """
                INSERT INTO scrape.website_replay (website_replay_id, scrape_resource_id)
                VALUES (:replay_id, :scrape_resource_id)
                ON CONFLICT DO NOTHING
                """,
                [{"replay_id": rid, "scrape_resource_id": sid} for rid, sid in replay_ids]
            )
            await self.db_session.commit()

    async def _scrape_and_store(self, scraper, replay_ids):
        replays = await scraper.scrape()
        for replay in replays:
            replay_id = int(replay["file_name"].split(".")[0])
            # Save replay data using Storage
            await self.storage.save(replay["file_name"], replay["data"])
            replay_ids.append((replay_id, scraper.scrape_resource_id))

