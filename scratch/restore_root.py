import os

root_dir = r"d:\LLM Wiki DHCHO"

# Mapping of keywords in current filenames to intended stable names
restore_map = {
    "LLM Wiki DHCHO": "README.md",
    "ANTIGRAVITY": "ANTIGRAVITY.md",
    "My Core Context": "My Core Context.md",
    "Sector News Impact Intelligence": "Sector News Impact Intelligence.md"
}

for filename in os.listdir(root_dir):
    if not filename.endswith(".md"): continue
    filepath = os.path.join(root_dir, filename)
    if os.path.isdir(filepath): continue
    
    for keyword, stable_name in restore_map.items():
        if keyword in filename:
            dest = os.path.join(root_dir, stable_name)
            if filename.lower() != stable_name.lower():
                print(f"RESTORING: {filename} -> {stable_name}")
                if os.path.exists(dest):
                    os.remove(dest)
                os.rename(filepath, dest)
                break
