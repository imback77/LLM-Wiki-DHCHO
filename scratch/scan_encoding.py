import os
import re

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
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(1000) # Read first 1000 chars
                
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

print("--- WIKI SCAN ---")
wiki_mapping = scan_dir(wiki_dir)
for item in wiki_mapping:
    if "intended" in item and item["current"] != item["intended"]:
         print(f"RENAME: {item['current']} -> {item['intended']}")

print("\n--- ROOT SCAN ---")
root_mapping = scan_dir(root_dir)
for item in root_mapping:
    if "intended" in item and item["current"] != item["intended"]:
         print(f"RENAME: {item['current']} -> {item['intended']}")
