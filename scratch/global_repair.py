import os
import re

wiki_dir = r"d:\LLM Wiki DHCHO\wiki"

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

def clean_name(name):
    # Remove emojis and non-standard symbols
    cleaned = re.sub(r'[^\uAC00-\uD7A3\u3131-\u318E\u0020-\u007E]', ' ', name)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

for filename in os.listdir(wiki_dir):
    if not filename.endswith(".md"): continue
    filepath = os.path.join(wiki_dir, filename)
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            header_bytes = f.read(2000)
        
        intended = get_intended_name(header_bytes)
        if intended:
            safe_name = clean_name(intended) + ".md"
            dest = os.path.join(wiki_dir, safe_name)
            
            if filepath.lower() != dest.lower():
                print(f"RENAME: {filename} -> {safe_name}")
                if os.path.exists(dest):
                    # Collision! Keep the larger one
                    if os.path.getsize(filepath) > os.path.getsize(dest):
                        os.remove(dest)
                        os.rename(filepath, dest)
                        print(f"  (Overwrote existing smaller file)")
                    else:
                        print(f"  (Skipped - existing file is larger/same)")
                else:
                    os.rename(filepath, dest)
    except Exception as e:
        print(f"Error {filename}: {e}")
