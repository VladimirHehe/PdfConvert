from sqlalchemy.orm import sessionmaker
from DATABASE_DIR.base_db import async_session, Session_factory
from DATABASE_DIR.models import File
from sqlalchemy.ext.asyncio import AsyncSession


async def push_pathS3_in_DB(AWS_BUCKET_NAME, filename,):
    async with Session_factory() as session:
        file_path = f"https://s3.storage.selcloud.ru/{AWS_BUCKET_NAME}/{filename}"
        file_model = File(filename=filename, filepath=file_path)
        session.add(file_model)
        await session.commit()