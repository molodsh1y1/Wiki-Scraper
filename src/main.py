import asyncio

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Country
from src.database.session import engine
from src.schemas.wiki import RegionSummary
from src.utils.config import logger


class DatabaseManager:
    @staticmethod
    async def get_region_summaries():
        async with AsyncSession(engine) as session:
            largest_country_subquery = (
                select(
                    Country.region,
                    Country.country_name,
                    Country.population_after,
                    func.row_number()
                    .over(partition_by=Country.region, order_by=Country.population_after.desc())
                    .label("row_num")
                )
                .where(Country.population_after.isnot(None))
                .subquery()
            )

            smallest_country_subquery = (
                select(
                    Country.region,
                    Country.country_name,
                    Country.population_after,
                    func.row_number()
                    .over(partition_by=Country.region, order_by=Country.population_after.asc())
                    .label("row_num")
                )
                .where(Country.population_after.isnot(None))
                .subquery()
            )

            query = (
                select(
                    Country.region,
                    func.sum(Country.population_after).label("total_population"),
                    largest_country_subquery.c.country_name.label("largest_country_name"),
                    largest_country_subquery.c.population_after.label("largest_country_population"),
                    smallest_country_subquery.c.country_name.label("smallest_country_name"),
                    smallest_country_subquery.c.population_after.label("smallest_country_population"),
                )
                .join(
                    largest_country_subquery,
                    (Country.region == largest_country_subquery.c.region)
                    & (largest_country_subquery.c.row_num == 1),
                    isouter=True,
                )
                .join(
                    smallest_country_subquery,
                    (Country.region == smallest_country_subquery.c.region)
                    & (smallest_country_subquery.c.row_num == 1),
                    isouter=True,
                )
                .group_by(
                    Country.region,
                    largest_country_subquery.c.country_name,
                    largest_country_subquery.c.population_after,
                    smallest_country_subquery.c.country_name,
                    smallest_country_subquery.c.population_after,
                )
            )

            result = await session.execute(query)
            return [RegionSummary(**row) for row in result.mappings()]


if __name__ == "__main__":
    region_summaries = asyncio.run(DatabaseManager.get_region_summaries())
    for summary in region_summaries:
        logger.info(summary)
