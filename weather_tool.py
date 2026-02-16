import requests
from typing import Any, Dict


def _fetch_weather_openweathermap(city: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch basic weather information for a given city using OpenWeatherMap API.

    Args:
        city: City name or 'city,country' string (e.g., 'London,UK').
        api_key: OpenWeatherMap API key.

    Returns:
        Parsed JSON response containing weather data.

    Raises:
        RuntimeError: If the HTTP request fails or the API returns an error.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"Weather API error: {resp.status_code} {resp.text}")
    return resp.json()


@mcp.tool()
def weather(city: str, provider: str = "openweathermap", api_key: str = "") -> Dict[str, Any]:
    """
    Get current weather for a city.

    Supports providers:
        - "openweathermap" (requires `api_key` argument with an OpenWeatherMap key)

    Args:
        city: City name (e.g., "Mumbai" or "Mumbai,IN").
        provider: Weather provider identifier.
        api_key: API key string for provider (if required).

    Returns:
        Dictionary with temperature (C), humidity (%), condition (text), and raw provider response.

    Raises:
        RuntimeError on missing dependency or provider errors.

    Semantic description:
        Returns a compact weather summary and raw payload; good for RAG/weather automations.
    """
    provider = provider.lower()
    if provider == "openweathermap":
        if not api_key:
            raise RuntimeError("OpenWeatherMap provider requires `api_key` argument.")
        data = _fetch_weather_openweathermap(city, api_key)
        main = data.get("main", {})
        weather_desc = (data.get("weather") or [{}])[0].get("description", "")
        return {
            "city": city,
            "temperature_c": main.get("temp"),
            "humidity": main.get("humidity"),
            "condition": weather_desc,
            "raw": data
        }
    else:
        raise RuntimeError(f"Unsupported weather provider: {provider}")

