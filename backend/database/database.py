from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)


class Database:

    def __init__(self, url: str, **kwargs):
        self.engine = None
        self.session = None
        self.url = url
        self.kw = kwargs

    async def startup(self):
        self.engine = create_async_engine(
            str(self.url),
            **self.kw,
        )
        self.session = async_sessionmaker(bind=self.engine,
                                          expire_on_commit=False,
                                          class_=AsyncSession)

    async def shutdown(self):
        if self.engine:
            await self.engine.dispose()
            self.engine = None
        self.session = None
