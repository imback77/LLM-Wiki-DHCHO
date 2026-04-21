
import os
import re
import json

wiki_dir = r"d:\LLM Wiki DHCHO\wiki"
index_file = r"d:\LLM Wiki DHCHO\wiki\index.md"

# 1. 파일 목록 및 인덱스 현황 파악
files = [f for f in os.listdir(wiki_dir) if f.endswith('.md')]
all_base_names = [f.replace('.md', '') for f in files]

with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

# 인덱스에 없는 파일들 추출
missing_from_index = [f for f in all_base_names if f"[[{f}]]" not in index_content and f not in ['index', 'log', 'archive', 'ANTIGRAVITY']]

# 2. 아카이브 생성 로직
archive_data = []
for name in missing_from_index:
    path = os.path.join(wiki_dir, name + ".md")
    date = "Unknown"
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        date_match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            date = date_match.group(1)
        elif re.match(r'^\d{4}-\d{2}-\d{2}', name):
            date = name[:10]
    archive_data.append({"name": name, "date": date})

archive_data.sort(key=lambda x: x['date'], reverse=True)

archive_md = f"""---
type: index
created: 2026-04-21
updated: 2026-04-21
tags: ["archive"]
---

# 📂 지식 아카이브 (Knowledge Archive)

메인 인덱스에 등록되지 않은 모든 세부 지식 노드와 과거 브리핑 자료를 날짜순으로 정리한 저장소입니다.

---

"""
current_date = ""
for item in archive_data:
    if item['date'] != current_date:
        current_date = item['date']
        archive_md += f"\n### 🗓️ {current_date}\n"
    archive_md += f"- [[{item['name']}]]\n"

with open(os.path.join(wiki_dir, "archive.md"), 'w', encoding='utf-8') as f:
    f.write(archive_md)


# 3. 정밀 링크 복구 로직 (44건 대상)
def find_precision_match(link):
    # exact or normalized match
    clean_link = re.sub(r'[^a-zA-Z0-9가-힣]', '', link).lower()
    
    # 1. Substring match (e.g., 'Gemma 4' in 'Gemma 4 (젬마 4)')
    best_match = None
    for name in all_base_names:
        clean_name = re.sub(r'[^a-zA-Z0-9가-힣]', '', name).lower()
        if clean_link == clean_name:
            return name
        if clean_link in clean_name or clean_name in clean_link:
            # Pick longest or best
            if not best_match or len(name) < len(best_match):
                best_match = name
    return best_match

def repair_content(content):
    def replace_match(match):
        raw_link = match.group(0)
        link_name = match.group(1).strip()
        if link_name in all_base_names or link_name.startswith('http'):
            return raw_link
            
        match_name = find_precision_match(link_name)
        if match_name:
            if "|" in raw_link:
                alias = raw_link.split("|")[1].replace("]]", "")
                return f"[[{match_name}|{alias}]]"
            return f"[[{match_name}]]"
        return raw_link
    
    return re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', replace_match, content)

repair_count = 0
for f in files:
    path = os.path.join(wiki_dir, f)
    with open(path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    
    new_content = repair_content(content)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        repair_count += 1

print(f"Archive updated with {len(archive_data)} items.")
print(f"Precision repair completed on {repair_count} files.")
