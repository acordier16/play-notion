# play-notion
Play music from a tagged Notion database via yt-dlp and mpv! 🎵

![Live Demo](https://raw.githubusercontent.com/acordier16/play-notion/main/demo.gif)

Are you...
- ...using Notion as a database for the music links (youtube, soundcloud, ...) you listen to? 🧠

Have you...
- ...ever wanted to be able to query these links with tags and play corresponding tracks directly? 🔗

Now, this is possible! 👍

## Usage
It's quite straightforward.
```
play-notion techno trance
```
will request the latest links in your Notion database with tags `techno` and `trance`. 

These tracks links are then forwarded to `mpv` with the `yt-dlp` hook so that they can be played.

#### Options
- You can change the number of tracks to be played using `-n NUMBER`
- You can randomize the order of tracks using `-r`
- You can display existing tags in the database using `-v`
- You can force the GUI window to appear (if you don't like the terminal) using `-w`

## Requirements
This python program requires:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) to be installed
- [mpv](https://mpv.io/installation/) to be installed and available from the commandline
- [A Notion account with an integration token](https://developers.notion.com/docs/create-a-notion-integration#step-1-create-an-integration)
- [A tagged Notion database with music links shared with the above integration](https://developers.notion.com/docs/create-a-notion-integration#step-2-share-a-database-with-your-integration)

## Steps to install
1. Install yt-dlp and mpv
2. Set-up your Notion integration and share your database through it
3. Clone this repository: `git clone https://github.com/acordier16/play-notion`
4. In the repository root, fill in `config.py` (so that it matches your Notion and yt-dlp configuration).
5. From the repository root, install the python package: `pip install -e .`
6. ???
7. Profit! Usage: `play-notion [OPTIONS] ARGS` (do not hesitate to `-h` for more details)

## Supported links
So far, they are the same as the ones yt-dlp supports. Note that there is a filtering of links hard-coded within the script, so that yt-dlp doesn't break. Hence only **bandcamp**, **soundcloud**, and **youtube** links are supported (but you can add more if you want!).
