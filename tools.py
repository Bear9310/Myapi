import xml.etree.ElementTree as ET
import requests

def get_live_weather(location_name):
    try:
        # 1. Search worldwide coordinates for the location
        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={location_name}&count=1"
        )
        geo_resp = requests.get(geo_url).json()
        
        if not geo_resp.get("results"):
            return f"Could not find any location named '{location_name}'."
            
        result = geo_resp["results"][0]
        lat = result["latitude"]
        lon = result["longitude"]
        correct_name = result["name"]
        country = result.get("country", "")
        
        # 2. Fetch live temperature and local time
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true&timezone=auto"
        )
        weather_resp = requests.get(weather_url).json()
        
        current = weather_resp["current_weather"]
        temp = current["temperature"]
        
        # 3. Format the local time string cleanly (YYYY-MM-DD THH:MM)
        raw_time = current["time"]
        local_date, local_time = raw_time.split("T")
        
        display_location = f"{correct_name}, {country}" if country else correct_name
        
        return (
            f"Location: {display_location} | "
            f"Current Temperature: {temp}°C | "
            f"Local Time: {local_time} (Date: {local_date})"
        )
        
    except Exception as e:
        return "Weather and time service is currently unavailable."

import xml.etree.ElementTree as ET

# === REAL-WORLD NEWS FETCHER ===
def get_live_news(topic="World"):
    try:
        # Use general news, or search for a specific topic
        if topic.lower() in ["world", "general", "top", "news"]:
            url = "https://news.google.com/rss"
        else:
            # Format the URL safely
            safe_topic = topic.replace(" ", "%20")
            url = f"https://news.google.com/rss/search?q={safe_topic}"
            
        resp = requests.get(url)
        
        # Parse the XML response
        root = ET.fromstring(resp.content)
        
        headlines = []
        # Extract the top 5 news items
        for item in root.findall('.//item')[:5]:
            title = item.find('title').text
            pub_date = item.find('pubDate').text
            
            # Clean up timezone text for easier reading
            clean_date = pub_date.replace(" GMT", "")
            headlines.append(f"- {title} (Published: {clean_date})")
            
        if not headlines:
            return f"No recent news found for '{topic}'."
            
        news_text = "\n".join(headlines)
        return f"Top 5 Latest Headlines for '{topic}':\n{news_text}"
        
    except Exception as e:
        return "News service is currently unavailable."
