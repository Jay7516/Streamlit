import asyncio

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
)
from dotenv import load_dotenv
from utils.scrap_utils import get_llm_strategy
from utils.json_utils import save_data, clear_data
load_dotenv()


URL = "https://www.mcdonalds.com/ca/en-ca/product/junior-chicken.html"
#URL = "https://www.mcdonalds.com/ca/en-ca/product/mcchicken.html"
#URL = "https://www.mcdonalds.com/ca/en-ca/product/maple-cream-pie.html"
#URL = "https://www.mcdonalds.com/ca/en-ca/full-menu/drinks.html"
async def main():
    clear_data()
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        #result = await crawler.arun(url=URL)
        # Print the extracted content
        session_id = "venue_crawl_session"
        #print(result.markdown)
        result = await crawler.arun(
        url=URL, config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Do not use cached data
            extraction_strategy=get_llm_strategy(),  # Strategy for data extraction
            #css_selector=css_selector,  # Target specific content on the page
            session_id=session_id,  # Unique session ID for the crawl
        ),

    )
    #print(result.extracted_content)
    save_data(result.extracted_content)
    
# Run the async main function
asyncio.run(main())