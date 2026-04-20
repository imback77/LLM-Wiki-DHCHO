import os
import re
import json
import sys

wiki_dir = r"d:\LLM Wiki DHCHO\wiki"
root_dir = r"d:\LLM Wiki DHCHO"

def get_intended_name(content):
    # Try to find YAML title first
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    
    # Try to find first # Header
    header_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
    if header_match:
        return header_match.group(1).strip()
    
    return None

def scan_dir(target_dir):
    mapping = []
    for filename in os.listdir(target_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(target_dir, filename)
            try:
                # Read with utf-8, ignore errors to get at least the header
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(1000)
                
                intended = get_intended_name(content)
                if intended:
                    # Remove invalid filename chars
                    safe_intended = re.sub(r'[\\/:*?"<>|]', "", intended)
                    mapping.append({
                        "current": filename,
                        "intended": safe_intended + ".md",
                        "full_path": filepath
                    })
            except Exception as e:
                mapping.append({"current": filename, "error": str(e)})
    return mapping

all_mapping = {
    "wiki": scan_dir(wiki_dir),
    "root": scan_dir(root_dir)
}

with open("scratch/repair_map.json", "w", encoding="utf-8") as f:
    json.dump(all_mapping, f, ensure_ascii=False, indent=2)

print("Mapping generated in scratch/repair_map.json")
