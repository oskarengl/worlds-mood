# -*- coding: utf-8 -*-
"""
Save historical snapshot of current data
Creates timestamped copies for time-travel feature
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create history directory if it doesn't exist
    history_dir = Path('history')
    history_dir.mkdir(exist_ok=True)
    
    print(f"Saving snapshot: {timestamp}")
    
    # Copy current data files with timestamp
    files_to_save = [
        'country_data.json',
        'headlines_data.json',
        'sentiment_analysis.json'
    ]
    
    saved_count = 0
    for filename in files_to_save:
        source = Path(filename)
        if source.exists():
            dest = history_dir / f'{timestamp}_{filename}'
            shutil.copy2(source, dest)
            print(f"  [OK] Saved {filename}")
            saved_count += 1
        else:
            print(f"  [SKIP] {filename} (not found)")
    
    # Update manifest
    manifest_file = history_dir / 'manifest.json'
    manifest = []
    
    if manifest_file.exists():
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    
    # Add new entry
    manifest.append({
        'timestamp': timestamp,
        'datetime': datetime.now().isoformat(),
        'files': saved_count
    })
    
    # Keep only last 50 snapshots
    manifest = manifest[-50:]
    
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n[OK] Snapshot saved: {timestamp}")
    print(f"Total snapshots in history: {len(manifest)}")

if __name__ == "__main__":
    main()

