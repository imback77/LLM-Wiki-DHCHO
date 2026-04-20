import os

wiki_dir = r"d:\LLM Wiki DHCHO\wiki"

targets = {
    "주성엔지니어링.md": "주성엔지니어링.md",
    "이수페타시스.md": "이수페타시스.md",
    "보안_소프트웨어.md": "보안_소프트웨어.md",
    "바이브_코딩.md": "바이브_코딩.md",
    "솔로_프리뉴어.md": "솔로_프리뉴어.md",
    "2026-04-20_Global_Macro_Snapshot.md": "2026-04-20_Global_Macro_Snapshot.md",
    "2026-04-20_Market_Flow_Analysis.md": "2026-04-20_Market_Flow_Analysis.md",
    "2026-04-20_Vibe_Coding_and_Solo_Business.md": "2026-04-20_Vibe_Coding_and_Solo_Business.md"
}

# Search by content
for filename in os.listdir(wiki_dir):
    filepath = os.path.join(wiki_dir, filename)
    if not os.path.isfile(filepath): continue
    
    try:
        with open(filepath, "rb") as f:
            raw = f.read(2000)
            
        content_str = raw.decode("utf-8", errors="ignore")
        
        target_name = None
        if "주성엔지니어링" in content_str or "Jusung Engineering" in content_str:
            target_name = "주성엔지니어링.md"
        elif "이수페타시스" in content_str or "ISU Petasys" in content_str:
            target_name = "이수페타시스.md"
        elif "보안_소프트웨어" in content_str or "Security Software" in content_str:
            target_name = "보안_소프트웨어.md"
        elif "Vibe Coding" in content_str or "바이브 코딩" in content_str:
            target_name = "바이브_코딩.md"
        elif "Solopreneur" in content_str or "솔로 프리뉴어" in content_str:
            target_name = "솔로_프리뉴어.md"
        elif "글로벌 매크로 지표" in content_str or "Global Macro Snapshot" in content_str:
            target_name = "2026-04-20_Global_Macro_Snapshot.md"
        elif "Market_Flow_Analysis" in content_str or "시장 자금 동향" in content_str:
            target_name = "2026-04-20_Market_Flow_Analysis.md"
            
        if target_name:
            dest = os.path.join(wiki_dir, target_name)
            if filepath.lower() != dest.lower():
                print(f"RENAME: {filename} -> {target_name}")
                os.rename(filepath, dest)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
