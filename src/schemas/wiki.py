from pydantic import BaseModel


class RegionSummary(BaseModel):
    region: str | None
    total_population: int | None
    largest_country_name: str | None
    largest_country_population: int | None
    smallest_country_name: str | None
    smallest_country_population: int | None
