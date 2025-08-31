# playlist-auditor
A toolkit for keeping your MP3 player's music library in sync with your YouTube playlists.  
It helps you clean up file names, extract playlist data, and compare collections to find missing or extra tracks.

---
## Features
- **File Normalization**: Standardizes `.ogg` file names on your MP3 player by:
  - Lowercasing all text
  - Removing parentheses `(official video)` and brackets `[feat. artist]`
  - Enforcing `artist - song` format
  - Handling collisions safely (`song.ogg`, `song_1.ogg`, etc.)
  - Logging all changes for reference
- **Playlist Export (Planned)**:
  - Chrome extension to extract YouTube playlist titles into `.txt`
- **Comparison (Planned)**:
  - Python script to compare normalized MP3 library against YouTube playlist export
  - Output missing tracks and extras

---
## Getting Started

### Prerequisites
- Python 3.8+
- Git (to clone the repository)

### Installation
```
# Clone the repo
git clone https://github.com/JosueLopez03/playlist-auditor.git
cd playlist-auditor

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate
```

---
## Usage
**Step 1: Normalize your MP3/OGG files**
```
python3 normalize.py /path/to/mp3player/music
```
***Runs in dry-run mode by default (preview only).***

**To apply changes:**
```
python3 normalize.py /path/to/mp3player/music --apply
```
***A log file normalized_log.txt will be created in the folder.***

**Step 2: Export YouTube Playlist (coming soon)**

Use the Chrome extension to save your youtube playlist to .txt.

**Step 3: Compare (coming soon)**

Run the comparator script to identify missing or extra tracks.

## Project Structure
```
playlist-auditor/
│── normalize.py          # Script to normalize MP3/OGG filenames
│── comparator.py         # (Planned) Compare MP3 vs YouTube txt export
│── extension/            # (Planned) Chrome extension to export playlist
│── README.md             # Project documentation
```

## Roadmap

- [ ] MP3/OGG normalizer with logging
- [ ] Chrome extension to export YouTube playlists
- [ ] Python comparator for playlists
- [ ] Fuzzy matching for song titles
- [ ] Optional integration with yt-dlp for downloading missing tracks

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.
