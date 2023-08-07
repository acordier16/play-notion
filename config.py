# A better implementation would be to have these as environment variables.

YTDLP_PATH = "/opt/homebrew/bin/yt-dlp" # Your binary path for yt-dlp
NOTION_API_VERSION = "2022-06-28"
NOTION_TOKEN = "" # Your Notion secret integration token
NOTION_DATABASE_ID = "" # The database ID you wish to query
NOTION_DATABASE_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}"
