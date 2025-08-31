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
```bash
# Clone the repo
git clone https://github.com/JosueLopez03/playlist-auditor.git
cd playlist-auditor

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate
