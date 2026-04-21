
import json
import os
import re

wiki_dir = r"d:\LLM Wiki DHCHO\wiki"
mapping_file = r"d:\LLM Wiki DHCHO\scratch\link_mapping.json"

with open(mapping_file, 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Sort mapping by key length descending to avoid partial replacements (though with [[ ]] it's safer)
keys = sorted(mapping.keys(), key=len, reverse=True)

def repair_links(content):
    def replace_match(match):
        link_name = match.group(1).strip()
        if link_name in mapping:
            return f"[[{mapping[link_name]}]]"
        return match.group(0)
    
    # Regex for [[Link]] or [[Link|Alias]]
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
                print(f"Repaired: {filename}")
                count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print(f"Total files repaired: {count}")
