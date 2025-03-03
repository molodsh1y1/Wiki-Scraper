import asyncio
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Country
from src.database.session import engine
from src.utils.config import logger


class WebScraper:
    def __init__(self, url: str):
        self.url = url
        self.driver = self._initialize_driver()
    
    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service()
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def scrape_page(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "wikitable"))
            )
            table = self.driver.find_element(By.CLASS_NAME, "wikitable")
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    data_row = [cell.text for cell in cells]
                    cleaned_data = DataCleaner.clean_data(data_row)
                    if cleaned_data:
                        data.append(cleaned_data)
            return data[1:]
        finally:
            self.driver.quit()


class DataCleaner:
    @staticmethod
    def clean_data(row):
        try:
            country_name = re.sub(r"\[[a-zA-Z]\]", "", row[0]).replace("\xa0", " ").strip()
            population_before = DataCleaner._check_na(row[1])
            population_after = DataCleaner._check_na(row[2])
            
            if population_before:
                population_before = int(row[1].replace(",", ""))
            if population_after:
                population_after = int(row[2].replace(",", ""))
            
            region = DataCleaner._check_na(row[4].strip())
            sub_region = DataCleaner._check_na(row[5].strip())
            
            return country_name, population_before, population_after, region, sub_region
        except Exception as e:
            logger.error(f"Error: {e}")
            return None, None, None, None, None

    @staticmethod
    def _check_na(value):
        return value if value != "N/A" else None


class DatabaseSaver:
    @staticmethod
    async def save_to_db(data):
        async with AsyncSession(engine) as session:
            for row in data:
                country_name, population_before, population_after, region, sub_region = row
                country = Country(
                    country_name=country_name,
                    population_before=population_before,
                    population_after=population_after,
                    region=region,
                    sub_region=sub_region,
                )
                session.add(country)
            await session.commit()


async def main():
    url = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"
    scraper = WebScraper(url)
    data = scraper.scrape_page()
    await DatabaseSaver.save_to_db(data)
    logger.info("Data saved to database")


if __name__ == "__main__":
    asyncio.run(main())
