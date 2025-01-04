import aiohttp

WEB_SEARCH_API_URL = (
    "http://example.com/search"  # Replace with actual web search API URL
)


async def perform_web_search(session, query):
    try:
        async with session.post(WEB_SEARCH_API_URL, json={"query": query}) as response:
            response.raise_for_status()
            result = await response.json()
            return result.get("results", "No results found.")
    except aiohttp.ClientError as e:
        return f"Error performing web search: {e}"
