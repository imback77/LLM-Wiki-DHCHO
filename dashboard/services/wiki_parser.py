import os
import glob
import re
import frontmatter
from typing import List, Dict, Any

class WikiParser:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def get_tracked_stocks(self) -> List[Dict[str, Any]]:
        """
        1. Parse the main watchlist (관심종목.md) to get the 86 stocks.
        2. Scan individual .md files to override with specific entry/target prices if they exist.
        """
        tracked_stocks = {}
        
        # 1. Parse 관심종목.md
        watchlist_path = os.path.join(self.base_path, 'raw', 'notes', '관심종목.md')
        if os.path.exists(watchlist_path):
            try:
                with open(watchlist_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                current_sector = "미분류"
                for line in lines:
                    line = line.strip()
                    if line.startswith("## ") and "섹터" in line:
                        # Parse sector name, e.g. "## 🔴 섹터 1: 방산 (10종목)" -> "방산"
                        m = re.search(r'섹터\s*\d+:\s*([^\(]+)', line)
                        if m:
                            current_sector = m.group(1).strip()
                        else:
                            current_sector = line.replace("##", "").strip()
                    
                    elif line.startswith("|") and not "No" in line and not "---" in line and not "항목" in line and not "전략" in line:
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 6:
                            stock_name = parts[2]
                            stock_code = parts[3]
                            grade = parts[4]
                            momentum = parts[5]
                            
                            if stock_code.isdigit() and len(stock_code) >= 5:
                                stock_code = stock_code.zfill(6)
                                tracked_stocks[stock_code] = {
                                    'filepath': watchlist_path,
                                    'filename': '관심종목.md',
                                    'code': stock_code,
                                    'name': stock_name,
                                    'sector': current_sector,
                                    'entry_price': 0,
                                    'entry_reason': f"[{grade}] {momentum}",
                                    'target_price': 0,
                                    'target_reason': '개별 종목 페이지(.md)를 생성하여 진입가/목표가를 설정하세요.',
                                    'stop_loss': 0,
                                    'status': '대기중',
                                    'content': f"**{grade}** | 핵심 모멘텀: {momentum}\n\n*관심종목.md 파일에서 자동으로 불러온 정보입니다. 개별 위키 문서를 만들고 YAML 메타데이터를 추가하면 대시보드에 상세 목표가/진입가가 연동됩니다.*"
                                }
            except Exception as e:
                print(f"Error parsing watchlist: {e}")

        # 2. Recursively scan individual .md files for specific frontmatter overrrides
        search_pattern = os.path.join(self.base_path, '**', '*.md')
        
        for filepath in glob.glob(search_pattern, recursive=True):
            if '.obsidian' in filepath or '.git' in filepath or '관심종목.md' in filepath:
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                if '종목코드' in post.metadata:
                    code = str(post.metadata.get('종목코드')).zfill(6)
                    
                    # If stock exists in watchlist, update it. If not, add it.
                    if code not in tracked_stocks:
                        tracked_stocks[code] = {
                            'filepath': filepath,
                            'filename': os.path.basename(filepath),
                            'code': code,
                            'name': post.metadata.get('aliases', [os.path.basename(filepath).replace('.md', '')])[0],
                            'sector': post.metadata.get('섹터', '미분류'),
                            'entry_price': 0,
                            'entry_reason': '',
                            'target_price': 0,
                            'target_reason': '',
                            'stop_loss': 0,
                            'status': '추적중',
                            'content': ''
                        }
                    
                    # Override with specific data
                    stock = tracked_stocks[code]
                    stock['entry_price'] = post.metadata.get('진입가', stock['entry_price'])
                    if post.metadata.get('진입가_선정이유'):
                        stock['entry_reason'] = post.metadata.get('진입가_선정이유')
                    
                    stock['target_price'] = post.metadata.get('목표가1', stock['target_price'])
                    if post.metadata.get('목표가_선정이유'):
                        stock['target_reason'] = post.metadata.get('목표가_선정이유')
                        
                    stock['stop_loss'] = post.metadata.get('손절가', stock['stop_loss'])
                    stock['status'] = post.metadata.get('추적상태', stock['status'])
                    if post.content.strip():
                        stock['content'] = post.content
                        
            except Exception:
                pass
                
        return list(tracked_stocks.values())

# For standalone testing
if __name__ == "__main__":
    wiki_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    parser = WikiParser(wiki_path)
    stocks = parser.get_tracked_stocks()
    print(f"Found {len(stocks)} tracked stocks.")
    for s in stocks[:5]: # print first 5 to check
        print(f"- {s['name']} ({s['code']}) | 진입가: {s['entry_price']} | 목표가: {s['target_price']}")
        print(f"  이유: {s['entry_reason']}")
