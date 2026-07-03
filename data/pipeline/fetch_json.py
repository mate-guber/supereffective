import httpx

def fetch_json(client: httpx.Client, url: str, params: dict | None = None) -> dict:
    """Fetch a URL and return its parsed JSON body.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = client.get(url, params=params)
    response.raise_for_status()
    return response.json()