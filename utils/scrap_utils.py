import json
import os
from typing import List, Set, Tuple
from model.mc_food import MCFood
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
    LLMConfig
)

# from models.venue import Venue
# from utils.data_utils import is_complete_venue, is_duplicate_venue

def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    # https://docs.crawl4ai.com/core/browser-crawler-config/
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=False,  # Whether to run in headless mode (no GUI)
        verbose=True,  # Enable verbose logging
    )



def get_llm_strategy() -> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.

    Returns:
        LLMExtractionStrategy: The settings for how to extract data using LLM.
    """
    # https://docs.crawl4ai.com/api/strategies/#llmextractionstrategy
    return LLMExtractionStrategy(
        llm_config=LLMConfig(provider="gemini/gemini-2.0-flash",api_token=os.getenv("GEMINI_KEY")),  # Name of the LLM provider
        schema=MCFood.model_json_schema(),  # JSON schema of the data model
        extraction_type="block",  # Type of extraction to perform
        instruction=(
            """
            Extract only one food objects with 'name', 'calories', 'price', 'fat', "
            'carbohydrates', 'protein', and a 1 sentence description of the food from the "
            following content. Don't space the units. For the first food image give its url and explain what does the food look like
            Gather from the view ingredients and allergens section Please extract a mapping where the key is the ingredient name (before 'Ingredients:') and the value is the full list of ingredients (everything after 'Ingredients:').
            If either any value is an N/A, null or all_ingredients is empty, make invalid true. Otherwise false
            Also get the url of the site
            """
 
        ),  # Instructions for the LLM
        input_format="markdown",  # Format of the input content
        verbose=True,  # Enable verbose logging
    )

def hi():
    print("DFSGdSG")

# async def check_no_results(
#     crawler: AsyncWebCrawler,
#     url: str,
#     session_id: str,
# ) -> bool:
#     """
#     Checks if the "No Results Found" message is present on the page.

#     Args:
#         crawler (AsyncWebCrawler): The web crawler instance.
#         url (str): The URL to check.
#         session_id (str): The session identifier.

#     Returns:
#         bool: True if "No Results Found" message is found, False otherwise.
#     """
#     # Fetch the page without any CSS selector or extraction strategy
#     result = await crawler.arun(
#         url=url,
#         config=CrawlerRunConfig(
#             cache_mode=CacheMode.BYPASS,
#             session_id=session_id,
#         ),
#     )

#     if result.success:
#         if "No Results Found" in result.cleaned_html:
#             return True
#     else:
#         print(
#             f"Error fetching page for 'No Results Found' check: {result.error_message}"
#         )

#     return False


# async def fetch_and_process_page(
#     crawler: AsyncWebCrawler,
#     page_number: int,
#     base_url: str,
#     css_selector: str,
#     llm_strategy: LLMExtractionStrategy,
#     session_id: str,
#     required_keys: List[str],
#     seen_names: Set[str],
# ) -> Tuple[List[dict], bool]:
#     """
#     Fetches and processes a single page of venue data.

#     Args:
#         crawler (AsyncWebCrawler): The web crawler instance.
#         page_number (int): The page number to fetch.
#         base_url (str): The base URL of the website.
#         css_selector (str): The CSS selector to target the content.
#         llm_strategy (LLMExtractionStrategy): The LLM extraction strategy.
#         session_id (str): The session identifier.
#         required_keys (List[str]): List of required keys in the venue data.
#         seen_names (Set[str]): Set of venue names that have already been seen.

#     Returns:
#         Tuple[List[dict], bool]:
#             - List[dict]: A list of processed venues from the page.
#             - bool: A flag indicating if the "No Results Found" message was encountered.
#     """
#     url = f"{base_url}?page={page_number}"
#     print(f"Loading page {page_number}...")

#     # Check if "No Results Found" message is present
#     no_results = await check_no_results(crawler, url, session_id)
#     if no_results:
#         return [], True  # No more results, signal to stop crawling

#     # Fetch page content with the extraction strategy
#     result = await crawler.arun(
#         url=url,
#         config=CrawlerRunConfig(
#             cache_mode=CacheMode.BYPASS,  # Do not use cached data
#             extraction_strategy=llm_strategy,  # Strategy for data extraction
#             css_selector=css_selector,  # Target specific content on the page
#             session_id=session_id,  # Unique session ID for the crawl
#         ),
#     )

#     if not (result.success and result.extracted_content):
#         print(f"Error fetching page {page_number}: {result.error_message}")
#         return [], False

#     # Parse extracted content
#     extracted_data = json.loads(result.extracted_content)
#     if not extracted_data:
#         print(f"No venues found on page {page_number}.")
#         return [], False

#     # After parsing extracted content
#     print("Extracted data:", extracted_data)

#     # Process venues
#     complete_venues = []
#     for venue in extracted_data:
#         # Debugging: Print each venue to understand its structure
#         print("Processing venue:", venue)

#         # Ignore the 'error' key if it's False
#         if venue.get("error") is False:
#             venue.pop("error", None)  # Remove the 'error' key if it's False

#         if not is_complete_venue(venue, required_keys):
#             continue  # Skip incomplete venues

#         if is_duplicate_venue(venue["name"], seen_names):
#             print(f"Duplicate venue '{venue['name']}' found. Skipping.")
#             continue  # Skip duplicate venues

#         # Add venue to the list
#         seen_names.add(venue["name"])
#         complete_venues.append(venue)

#     if not complete_venues:
#         print(f"No complete venues found on page {page_number}.")
#         return [], False

#     print(f"Extracted {len(complete_venues)} venues from page {page_number}.")
#     return complete_venues, False  # Continue crawling
