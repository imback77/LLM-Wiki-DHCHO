
import json
import os
import re
import difflib

wiki_dir = r"d:\LLM Wiki DHCHO\wiki"
valid_filenames_file = r"d:\LLM Wiki DHCHO\scratch\valid_filenames.txt"

with open(valid_filenames_file, 'r', encoding='utf-8') as f:
    valid_names = [line.strip() for line in f if line.strip()]

# Mapping from previous run
with open(r"d:\LLM Wiki DHCHO\scratch\link_mapping.json", 'r', encoding='utf-8') as f:
    manual_mapping = json.load(f)

def get_clean_chars(s):
    # Keep only letters, numbers, and Korean characters
    return re.sub(r'[^a-zA-Z0-9ㄱ-ㅣ가-힣]', '', s)

def find_best_match(link, valid_names):
    if link in valid_names:
        return link
    if link in manual_mapping:
        return manual_mapping[link]
    
    cleaned_link = get_clean_chars(link)
    if len(cleaned_link) < 2:
        return None
    
    best_name = None
    best_score = 0
    
    for name in valid_names:
        cleaned_name = get_clean_chars(name)
        # Use SequenceMatcher for a more robust fuzzy match
        score = difflib.SequenceMatcher(None, cleaned_link, cleaned_name).ratio()
        
        if score > best_score:
            best_score = score
            best_name = name
            
    if best_score > 0.4: # Threshold for match
        return best_name
    return None

def repair_links(content):
    def replace_match(match):
        link_full = match.group(0)
        link_name = match.group(1).strip()
        
        # Don't touch external or system links
        if link_name.startswith("http") or link_name.endswith(".png") or link_name.endswith(".jpg"):
            return link_full
            
        best = find_best_match(link_name, valid_names)
        if best and best != link_name:
            # Preserve alias if existed [[Link|Alias]]
            if "|" in match.group(0):
                alias = match.group(0).split("|")[1].replace("]]", "")
                return f"[[{best}|{alias}]]"
            return f"[[{best}]]"
        return link_full
    
    return re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', replace_match, content)

count = 0
for filename in os.listdir(wiki_dir):
    if filename.endswith(".md"):
        path = os.path.join(wiki_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = repair_links(content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Aggressive Repair: {filename}")
                count += 1
        except Exception as e:
            pass # Silent error for brevity

print(f"Total files repaired (Aggressive): {count}")
