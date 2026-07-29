import httpx # Since FastAPI and MCP are async frameworks, we need an async HTTP client to call the TMDB API without blocking.httpx is like requests but supports async.
import os  # Built-in Python module. We use it to read environment variables (your API keys) from the system.
from mcp.server.fastmcp import FastMCP  # FastMCP is a class that lets you define an MCP server easily — similar to how FastAPI lets you define a REST API.
from dotenv import load_dotenv 

load_dotenv()  #load_dotenv() reads your .env file and loads all the key=value pairs into environment variables. Without this, os.getenv("TMDB_API_KEY") would return None.

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"   #BASE_URL is just a constant so you don't repeat the full URL in every function. This url returns json. You get this url from tmdb developer documentation.

mcp = FastMCP("tmdb") #Creates your MCP server and names it "tmdb". Think of this like app = FastAPI() — it's the server instance everything else attaches to.

#This decorator registers the function below as a tool on your MCP server. The agent will see it by its function name search_movies and its docstring as the description. This is how the agent knows what tools are available and when to use them.
@mcp.tool()
async def search_movies(query: str) -> dict:   #query: str is the input the agent passes in. -> dict means it returns a dictionary.
    """Search for movies by title"""
    async with httpx.AsyncClient() as client:     # Opens an async HTTP session. The 'async with' block ensures the connection is properly closed when done, even if something crashes.
        response = await client.get(
            f"{BASE_URL}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": query}  # Makes a GET request to TMDB. await means "pause here until the response comes back". The params dict becomes query parameters in the URL. Parameter name and the no: of parameters to be passed can be understood by referring the API documentation.
        )
        data = response.json()  # Parses the JSON response into a Python dict.
        results = data.get("results", [])[:5]  # TMDB returns a results list — we take only the first 5 to keep responses concise. The [] is a fallback if results key is missing.
        return {
            # The key names are all expected return values in 
            "movies": [
                {
                    "id": m["id"],
                    "title": m["title"],
                    "year": m.get("release_date", "")[:4],
                    "overview": m.get("overview", ""),
                    "rating": m.get("vote_average", 0),
                    "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
                                if m.get("poster_path") else None
                }
                for m in results    # This is a list comprehension — it loops over results and builds a clean dict for each of the 5 movies.
            ]
        }

@mcp.tool()
async def get_movie_details(movie_id: int) -> dict:
    """Get full details of a movie by its TMDB ID"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY, "append_to_response": "credits"}
        )
        m = response.json()
        cast = m.get("credits", {}).get("cast", [])[:5]   #Safely navigates nested dicts. If credits doesn't exist, returns {}. If cast doesn't exist inside that, returns []. Then takes the top 5 cast members.
        return {
            "id": m["id"],
            "title": m["title"],
            "overview": m.get("overview", ""),
            "year": m.get("release_date", "")[:4],
            "runtime": m.get("runtime"),
            "rating": m.get("vote_average"),
            "genres": [g["name"] for g in m.get("genres", [])],
            "cast": [c["name"] for c in cast],
            "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
                        if m.get("poster_path") else None
        }

@mcp.tool()
async def get_similar_movies(movie_id: int) -> dict:
    """Get movies similar to a given movie"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/movie/{movie_id}/similar",
            params={"api_key": TMDB_API_KEY}
        )
        results = response.json().get("results", [])[:5]
        return {
            "movies": [
                {
                    "id": m["id"],
                    "title": m["title"],
                    "year": m.get("release_date", "")[:4],
                    "rating": m.get("vote_average", 0),
                    "overview": m.get("overview", "")
                }
                for m in results
            ]
        }

@mcp.tool()
async def get_watch_providers(movie_id: int, region: str = "IN") -> dict:  #region: str = "IN" means India is the default 
    """Get streaming availability for a movie in a given region"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/movie/{movie_id}/watch/providers",
            params={"api_key": TMDB_API_KEY}
        )
        results = response.json().get("results", {})
        region_data = results.get(region, {})
        return {
            "region": region,
            "stream": [p["provider_name"] for p in region_data.get("flatrate", [])],
            "rent":   [p["provider_name"] for p in region_data.get("rent", [])],
            "buy":    [p["provider_name"] for p in region_data.get("buy", [])]
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")