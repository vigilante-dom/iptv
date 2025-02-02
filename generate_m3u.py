import requests

# Base API URL (Replace with the actual API URL)
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

def get_streams(source, match_id):
    """Fetches stream links for a match."""
    url = f"{BASE_URL}/stream/{source}/{match_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch streams for {match_id}")
        return []

def generate_m3u(matches):
    """Generates an M3U playlist from live matches."""
    m3u_content = "#EXTM3U\n"

    for match in matches:
        if "teams" in match and match["teams"]:
            home = match["teams"].get("home", {}).get("name", "Unknown")
            away = match["teams"].get("away", {}).get("name", "Unknown")

            if match.get("sources"):
                source = match["sources"][0]["source"]
                match_id = match["sources"][0]["id"]
                stream_url = f"{BASE_URL}/stream/{source}/{match_id}"

                channel_id = f"{home.lower()}-{away.lower()}".replace(" ", "-")
                m3u_content += f'#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{home} vs {away}", {home} vs {away}\n'
                m3u_content += f"{stream_url}\n"

    return m3u_content

def save_m3u_to_file(m3u_data, filename="playlist.m3u"):
    """Saves the M3U playlist to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(m3u_data)

def main():
    print("📢 Fetching live matches...")
    live_matches = get_live_matches()

    if live_matches:
        print("✅ Found matches. Generating M3U...")

        # Generate and save M3U
        m3u_data = generate_m3u(live_matches)
        save_m3u_to_file(m3u_data)

        print("✅ M3U successfully generated!")
    else:
        print("❌ No live matches available.")

if __name__ == "__main__":
    main()
