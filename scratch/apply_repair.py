import os
import json
import re

map_file = r"d:\LLM Wiki DHCHO\scratch\repair_map.json"

def clean_filename(name):
    # Remove emojis and non-standard symbols
    # This regex keeps Korean, English, numbers, and allowed punctuation
    # \uAC00-\uD7A3: Korean syllables
    # \u3131-\u318E: Korean compatibility jamo
    # \u0020-\u007E: Basic ASCII (includes English and most punct)
    cleaned = re.sub(r'[^\uAC00-\uD7A3\u3131-\u318E\u0020-\u007E]', ' ', name)
    # Remove leading/trailing spaces and consolidate internal spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Ensure it ends with .md
    if not cleaned.lower().endswith(".md"):
        cleaned += ".md"
    return cleaned

with open(map_file, "r", encoding="utf-8") as f:
    mapping_data = json.load(f)

def execute_rename(items):
    logs = []
    for item in items:
        if "intended" in item:
            src = item["full_path"]
            if not os.path.exists(src):
                # Try to see if it already has a "different" garbled name we can find
                continue
                
            new_name = clean_filename(item["intended"])
            dest = os.path.join(os.path.dirname(src), new_name)
            
            if src == dest:
                continue
                
            try:
                # If destination exists, add a suffix to avoid collision
                base, ext = os.path.splitext(dest)
                counter = 1
                final_dest = dest
                while os.path.exists(final_dest) and final_dest.lower() != src.lower():
                    final_dest = f"{base}_{counter}{ext}"
                    counter += 1
                
                os.rename(src, final_dest)
                logs.append(f"SUCCESS: {os.path.basename(src)} -> {os.path.basename(final_dest)}")
            except Exception as e:
                logs.append(f"FAILED: {os.path.basename(src)} -> {str(e)}")
    return logs

print("--- RENAMING WIKI FILES ---")
wiki_logs = execute_rename(mapping_data["wiki"])
for log in wiki_logs:
    print(log)

print("\n--- RENAMING ROOT FILES ---")
root_logs = execute_rename(mapping_data["root"])
for log in root_logs:
    print(log)
