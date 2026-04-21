import os
import re

root_dir = r"d:\LLM Wiki DHCHO"

for filename in os.listdir(root_dir):
    if not filename.endswith(".md"): continue
    filepath = os.path.join(root_dir, filename)
    if os.path.isdir(filepath): continue
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(500)
            
        if "LLM Wiki DHCHO" in content and "Knowledge" in content:
            print(f"FOUND README: {filename}")
            dest = os.path.join(root_dir, "README.md")
            if filename.lower() != "readme.md":
                if os.path.exists(dest):
                    os.remove(dest)
                os.rename(filepath, dest)
                print(f"RENAME: {filename} -> README.md")
                break
    except Exception as e:
        print(f"Error {filename}: {e}")
