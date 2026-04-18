const fs = require('fs');
const path = require('path');

const WIKI_DIR = path.join(__dirname, '../wiki');
const INDEX_FILE = path.join(WIKI_DIR, 'index.md');

function lint() {
    console.log("🔍 LLM Wiki 로컬 린트 시작...");
    
    // wiki/ 폴더가 없으면 에러
    if (!fs.existsSync(WIKI_DIR)) {
        console.error("❌ wiki/ 폴더를 찾을 수 없습니다.");
        return;
    }

    const files = fs.readdirSync(WIKI_DIR).filter(f => f.endsWith('.md') && f !== 'ANTIGRAVITY.md');
    const indexContent = fs.existsSync(INDEX_FILE) ? fs.readFileSync(INDEX_FILE, 'utf8') : "";
    
    const report = {
        total_pages: files.length,
        broken_links: [],
        orphan_pages: [],
        index_missing: [],
        frontmatter_errors: [],
        stats: {
            concept: 0,
            entity: 0,
            summary: 0,
            comparison: 0,
            insight: 0,
            stub: 0,
            other: 0
        }
    };

    const allFileNames = new Set(files.map(f => f.replace('.md', '')));
    const referencedBy = {}; // { target: [sources] }

    files.forEach(file => {
        const filePath = path.join(WIKI_DIR, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const fileName = file.replace('.md', '');

        // 1. Frontmatter Check
        const fmMatch = content.match(/^---([\s\S]*?)---/);
        if (fmMatch) {
            const fm = fmMatch[1];
            const typeMatch = fm.match(/type:\s*["']?(\w+)["']?/);
            if (typeMatch) {
                const type = typeMatch[1];
                report.stats[type] = (report.stats[type] || 0) + 1;
            } else {
                report.stats.other++;
                report.frontmatter_errors.push(`${file}: type 누락`);
            }
        } else {
            report.stats.other++;
            report.frontmatter_errors.push(`${file}: frontmatter 없음`);
        }

        // 2. Link Check
        // Match both [[Link]] and [[Link|Alias]]
        const links = [...content.matchAll(/\[\[(.*?)\]\]/g)].map(m => m[1].split('|')[0].trim());
        links.forEach(link => {
            // Skip special files and raw references
            if (['index', 'log', 'dashboard', 'ANTIGRAVITY'].includes(link)) return;
            if (link.startsWith('raw/')) return; // raw/ 파일 링크는 무시
            if (link.startsWith('wiki/')) link = link.replace('wiki/', ''); // wiki/ 접두사는 제거하고 체크

            if (!allFileNames.has(link)) {
                report.broken_links.push({ from: file, to: link });
            } else {
                if (!referencedBy[link]) referencedBy[link] = [];
                referencedBy[link].push(fileName);
            }
        });

        // 3. Index Check
        if (!['index', 'log', 'dashboard'].includes(fileName)) {
            if (!indexContent.includes(`[[${fileName}]]`)) {
                report.index_missing.push(file);
            }
        }
    });

    // 4. Orphan Check
    files.forEach(file => {
        const fileName = file.replace('.md', '');
        if (['index', 'log', 'dashboard'].includes(fileName)) return;
        if (!referencedBy[fileName] || referencedBy[fileName].length === 0) {
            report.orphan_pages.push(file);
        }
    });

    // Output Report
    console.log("\n--- 린트 결과 보고서 ---");
    console.log(`📊 총 페이지: ${report.total_pages}개`);
    console.log(`  (개념: ${report.stats.concept}, 엔티티: ${report.stats.entity}, 요약: ${report.stats.summary}, 인사이트: ${report.stats.insight}, 스텁: ${report.stats.stub})`);
    
    if (report.broken_links.length > 0) {
        console.log(`\n🔴 깨진 링크 (${report.broken_links.length}건):`);
        report.broken_links.slice(0, 10).forEach(l => console.log(`  - ${l.from} -> [[${l.to}]]`));
        if (report.broken_links.length > 10) console.log(`  ...외 ${report.broken_links.length - 10}건`);
    }

    if (report.index_missing.length > 0) {
        console.log(`\n🟡 인덱스 누락 (${report.index_missing.length}건):`);
        report.index_missing.slice(0, 10).forEach(f => console.log(`  - ${f}`));
        if (report.index_missing.length > 10) console.log(`  ...외 ${report.index_missing.length - 10}건`);
    }

    if (report.orphan_pages.length > 0) {
        console.log(`\n🟡 고아 페이지 (${report.orphan_pages.length}건):`);
        report.orphan_pages.slice(0, 10).forEach(f => console.log(`  - ${f}`));
        if (report.orphan_pages.length > 10) console.log(`  ...외 ${report.orphan_pages.length - 10}건`);
    }

    if (report.frontmatter_errors.length > 0) {
        console.log(`\n🟠 Frontmatter 오류 (${report.frontmatter_errors.length}건):`);
        report.frontmatter_errors.slice(0, 10).forEach(e => console.log(`  - ${e}`));
    }

    console.log("\n🔍 자동 수정 제안:");
    if (report.index_missing.length > 0) {
        console.log("  - index.md에 누락된 페이지들을 추가해야 합니다.");
    }
    if (report.frontmatter_errors.length > 0) {
        console.log("  - 스텁 페이지들에 기본 frontmatter를 추가해야 합니다.");
    }

    console.log("\n✅ 린트 완료");
}

lint();
