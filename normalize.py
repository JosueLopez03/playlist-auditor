import os
import sys
import re
import unicodedata
from datetime import datetime
from uuid import uuid4

def normalize_filename(filename: str) -> str:
    """
    Normalize into 'artist - title':
    - lowercase
    - remove (...) and [...]
    - collapse spaces
    - use the FIRST dash-like separator as the artist/title split
      (any additional separators become spaces inside the title)
    """
    base, _ext = os.path.splitext(filename)
    name = base.lower()

    # Remove bracketed text
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"\[.*?\]", "", name)

    # Collapse whitespace early
    name = re.sub(r"\s+", " ", name).strip()

    # Split on dash separators (any number of dashes with optional spaces)
    parts = [p.strip() for p in re.split(r"\s*-+\s*", name) if p.strip()]

    if len(parts) >= 2:
        artist = parts[0]
        # Title = everything after the first separator; join with spaces to ensure
        # we end up with a single 'artist - title' delimiter in the final name.
        if (artist == "na"):
            artist = "unknown"
        title = " ".join(parts[1:])
        name = f"{artist} - {title}"
    else:
        # No separator found — fall back to 'unknown - <name>'
        # (Keep it predictable rather than guessing)
        if name:
            name = f"unknown - {name}"
        else:
            name = "unknown - unknown"

    # Final whitespace tidy and NFC unicode normalization (helps on macOS volumes)
    name = re.sub(r"\s+", " ", name).strip()
    name = unicodedata.normalize("NFC", name)
    return name

def _two_step_case_rename(old_path: str, new_path: str):
    """
    On case-insensitive filesystems, renaming only case may fail or be treated as "exists".
    Do a two-step hop via a temp name.
    """
    folder = os.path.dirname(old_path)
    tmp_path = os.path.join(folder, f".__rename_tmp_{uuid4().hex}")
    os.rename(old_path, tmp_path)
    os.rename(tmp_path, new_path)

def normalize_music_folder(folder_path: str, dry_run: bool = True, log_file: str = "normalized_log.txt"):
    seen = set()
    log_entries = []

    # Snapshot list so renames don't affect iteration
    for filename in list(os.listdir(folder_path)):
        if not filename.lower().endswith(".ogg"):
            continue

        normalized_base = normalize_filename(filename)
        target_name = normalized_base + ".ogg"

        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, target_name)

        # Detect case-only change (important for case-insensitive volumes)
        is_case_only_change = (filename != target_name) and (filename.lower() == target_name.lower())

        # Resolve collisions, but DO NOT treat case-only change as a collision
        counter = 1
        candidate = target_name
        while (candidate in seen or os.path.exists(os.path.join(folder_path, candidate))) and not (
            is_case_only_change and candidate.lower() == filename.lower()
        ):
            base_no_ext, _ = os.path.splitext(normalized_base)
            candidate = f"{normalized_base}_{counter}.ogg"
            counter += 1

        target_name = candidate
        new_path = os.path.join(folder_path, target_name)
        seen.add(target_name)

        if filename != target_name:
            entry = f"{filename}  -->  {target_name}"
            print(entry)
            log_entries.append(entry)

            if not dry_run:
                try:
                    if is_case_only_change and target_name.lower() == filename.lower():
                        _two_step_case_rename(old_path, new_path)
                    else:
                        os.rename(old_path, new_path)
                except FileNotFoundError:
                    print(f"File not found: {old_path}. Skipping.")
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

    if log_entries:
        with open(os.path.join(folder_path, log_file), "a", encoding="utf-8") as log:
            log.write(f"\n=== Normalization run on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            for entry in log_entries:
                log.write(entry + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 normalize.py /path/to/music/folder [--apply]")
        sys.exit(1)

    music_dir = os.path.expanduser(sys.argv[1])
    dry_run = "--apply" not in sys.argv
    normalize_music_folder(music_dir, dry_run=dry_run)
