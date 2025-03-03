# Population Data Service

This project is a service that fetches population data for countries, stores it in a PostgreSQL database, and outputs aggregated regional data. The service is containerized using Docker Compose.

## Data Source
The population data is sourced from the Wikipedia table:
[List of countries by population (United Nations)](https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959)

## Features
- Fetches, parses, and stores country population data in PostgreSQL.
- Aggregates and displays total population data by region.
- Outputs the largest and smallest countries by population within each region.
- Uses Docker Compose for easy deployment.
- Implements functionality using classes.

## Installation and Setup

### Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/).
- Install [Docker Compose](https://docs.docker.com/compose/install/).

### Clone the repository
```bash
git clone https://github.com/molodsh1y1/Wiki-Scraper.git-url
cd Wiki-Scraper
```

### Build and Start the Services
1. **Build the services**
```bash
docker-compose build
```
2. **Fetch and store data**
```bash
docker-compose up get_data
```
3. **Process and display aggregated data**
```bash
docker-compose up print_data
```

## Expected Output Format
Each region will be displayed with the following information:
```
Region Name
Total Population of the Region
Largest Country by Population:
Population of Largest Country:
Smallest Country by Population:
Population of Smallest Country:
```

## Project Structure
```
.
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image configuration
├── src                     # Source code
│   ├── database            # Database connection and query
│   │   ├── alembic         # Alembic migration scripts
│   │   ├── models.py       # Database models
│   │   ├── session.py      # Database session
│   ├── schemas             # Pydantic schemas
│   │   ├── wiki.py         # Wikipedia data schema 
│   ├── utils.py            # Database utility functions
│   │   ├── config.py       # Project configuration
│   ├── scrapers            # Web scrapers
│   │   ├── wiki_scraper.py # Wikipedia scraper
```
