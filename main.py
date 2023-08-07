#!/usr/bin/env python3

import argparse
import requests
from random import shuffle
from functools import partial
import subprocess

from config import YTDLP_PATH, NOTION_TOKEN, NOTION_DATABASE_ID, NOTION_DATABASE_URL


def build_headers_and_json(notion_token, tags):
    # Building the headers for all Notion requests
    headers = {
        "Authorization": "Bearer " + notion_token,
        "content-type": "application/json",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
    }
    # Building the json data for the Notion POST request
    and_query = []
    for tag in tags:  # Add selected tags to criterions.
        and_query.append({"property": "Tags", "multi_select": {"contains": tag}})
    if not "set" in tags:  # If "set" tag was not selected, specifically avoid it.
        and_query.append(
            {"property": "Tags", "multi_select": {"does_not_contain": "set"}}
        )
    json = {
        "filter": {"and": and_query},
        "sorts": [{"property": "Created", "direction": "descending"}],
        # "page_size": args.number, # Maximum number of items in the response
    }
    return headers, json


def make_request_and_do(url, headers, json, do):
    if json is not None:
        response = requests.post(url, headers=headers, json=json)  # Do a POST request
    else:
        response = requests.get(url, headers=headers)  # Do a GET request

    if response.status_code == 200:
        return do(response)
    else:
        print(f"[ERROR] {response.status_code} - {response.text}")
        # RAISE ERROR?


def get_existing_tags(response):
    print("[INFO] Connected to the Notion database successfuly.")
    existing_tags = [
        item["name"]
        for item in response.json()["properties"]["Tags"]["multi_select"]["options"]
    ]
    print(f"[INFO] Available tags: {existing_tags}")
    return existing_tags


def get_tracks_urls(response, random, tracks_number):
    def works_with_youtube_dl(url):
        services = ["youtube", "bandcamp", "soundcloud"]
        for service in services:
            if service in url:
                return True
        return False

    # Retrieve URLs for Notion query result.
    urls = [item["properties"]["URL"]["url"] for item in response.json()["results"]]
    # Filter the URLs so that they are compatible with youtube-dl
    urls = [url for url in urls if works_with_youtube_dl(url)]
    # The & character is a problem when passing the command to subprocess, so we need to escape it for each URL
    urls = [url.replace("&", "\\&") for url in urls if works_with_youtube_dl(url)]
    print(f"[INFO] Gathered last {len(urls)} URLs.")
    if random:
        shuffle(urls)
        print(f"[INFO] Randomized URLs order.")
    urls = urls[:tracks_number]
    print(f"[INFO] Selected the first {len(urls)} URLs.")
    return urls


def build_mpv_command(urls, window):
    command = (
        "mpv --term-playing-msg='Title: ${media-title}' --force-seekable=yes --script-opts=ytdl_hook-ytdl_path="
        + YTDLP_PATH
    )
    if window:
        command += " --force-window --autofit=100%x720"
    else:
        command += " --no-video"
    for url in urls:
        command += " " + url
    return command


def run_mpv_command(command):
    try:
        process = subprocess.Popen(command, shell=True)
        process.communicate()
        process.wait()
        if process.returncode != 0:
            print(f"Command failed with exit code {process.returncode}")
        else:
            print("Process executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Plays music from a tagged Notion database via yt-dlp and mpv. Will retrieve the most recent tracks first unless specified. This script requires yt-dlp and mpv to be installed."
    )
    parser.add_argument(
        "tags",
        type=str,
        nargs="+",
        help="A list of queried tags. Tags will be queried in an 'AND' fashion. By default, tracks with tag 'set' will not be retrieved (unless specified).",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        help="The number of tracks to retrieve and play. Default: 30",
        default=30,
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="If present, tracks will be retrieved in a 'random' order rather than in a 'most recent first' one.",
    )
    parser.add_argument(
        "-w",
        "--window",
        action="store_true",
        help="If present, will open a GUI window for mpv.",
    )
    args = parser.parse_args()

    # Build the headers and the json POST data
    headers, json = build_headers_and_json(notion_token=NOTION_TOKEN, tags=args.tags)

    # Connect with the database
    existing_tags = make_request_and_do(
        url=NOTION_DATABASE_URL, headers=headers, json=None, do=get_existing_tags
    )

    # Query the database to get tracks URLs
    urls = make_request_and_do(
        url=f"{NOTION_DATABASE_URL}/query",
        headers=headers,
        json=json,
        do=partial(get_tracks_urls, random=args.random, tracks_number=args.number),
    )

    # Build the mpv command from tracks URLs
    command = build_mpv_command(urls, window=args.window)

    # Run mpv
    run_mpv_command(command)


if __name__ == "__main__":
    main()
