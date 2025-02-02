import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_URL = "https://streamed.example.com/api"

def get_live_matches():
    """Fetches live matches from the API."""
    url = f"{BASE_URL}/matches/live"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Failed to fetch live matches")
        return []

def convert_to_xmltv_time(unix_timestamp):
    """Converts a Unix timestamp to XMLTV format."""
    dt = datetime.utcfromtimestamp(unix_timestamp / 1000)
    return dt.strftime("%Y%m%d%H%M%S +0000")

def generate_epg_xml(matches):
    """Generates an XMLTV EPG file from live matches."""
    root = ET.Element("tv", generator="Streamed API EPG")

    for match in matches:
        if "teams" in match and match["teams"]:
            home = match["teams"].get("home", {}).get("name", "Unknown")
            away = match["teams"].get("away", {}).get("name", "Unknown")
            channel_id = f"{home.lower()}-{away.lower()}".replace(" ", "-")

            channel = ET.SubElement(root, "channel", id=channel_id)
            ET.SubElement(channel, "display-name").text = f"{home} vs {away}"

            start_time = convert_to_xmltv_time(match["date"])
            stop_time = convert_to_xmltv_time(match["date"] + (2 * 60 * 60 * 1000))  # Assume 2-hour match

            programme = ET.SubElement(root, "programme", start=start_time, stop=stop_time, channel=channel_id)
            ET.SubElement(programme, "title").text = f"Live: {home} vs {away}"
            ET.SubElement(programme, "desc").text = f"Watch the exciting match between {home} and {away}."
            ET.SubElement(programme, "category").text = "Sports"

    return ET.tostring(root, encoding="utf-8").decode("utf-8")

def save_epg_to_file(epg_data, filename="epg.xml"):
    """Saves the EPG XML file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(epg_data)

def main():
    print("📢 Fetching live matches...")
    live_matches = get_live_matches()

    if live_matches:
        print("✅ Found matches. Generating EPG...")

        # Generate and save EPG
        epg_xml = generate_epg_xml(live_matches)
        save_epg_to_file(epg_xml)

        print("✅ EPG successfully generated!")
    else:
        print("❌ No live matches available.")

if __name__ == "__main__":
    main()
