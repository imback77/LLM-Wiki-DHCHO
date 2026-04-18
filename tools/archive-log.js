const fs = require('fs');
const path = require('path');

const WIKI_DIR = path.join(__dirname, '../wiki');
const ARCHIVE_DIR = path.join(WIKI_DIR, 'archive');
const LOG_FILE = path.join(WIKI_DIR, 'log.md');

function rotateLog() {
    console.log("📦 로그 아카이빙 시작...");
    
    if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR);
    
    const content = fs.readFileSync(LOG_FILE, 'utf8');
    const sections = content.split(/\n## /);
    
    if (sections.length <= 21) {
        console.log("✅ 보관할 로그가 부족합니다. (현재 엔트리 20개 이하)");
        return;
    }

    const header = sections[0];
    const latestEntries = sections.slice(1, 21); // 최신 20개
    const oldEntries = sections.slice(21); // 나머지

    // 아카이브 파일명 결정 (현재 날짜 기준 분기)
    const now = new Date();
    const quarter = Math.floor((now.getMonth() + 3) / 3);
    const archiveName = `log_archive_${now.getFullYear()}_Q${quarter}.md`;
    const archivePath = path.join(ARCHIVE_DIR, archiveName);

    let archiveHeader = `---\ntype: log-archive\ncreated: ${now.toISOString().split('T')[0]}\n---\n# 로그 아카이브 (${now.getFullYear()} Q${quarter})\n\n`;
    
    let existingArchive = "";
    if (fs.existsSync(archivePath)) {
        existingArchive = fs.readFileSync(archivePath, 'utf8').split('\n\n---\n\n')[1] || "";
    }

    const archivedContent = archiveHeader + oldEntries.map(e => "## " + e).join("\n") + "\n\n---\n\n" + existingArchive;
    
    fs.writeFileSync(archivePath, archivedContent, 'utf8');
    
    const newLogContent = header + latestEntries.map(e => "\n## " + e).join("");
    fs.writeFileSync(LOG_FILE, newLogContent, 'utf8');

    console.log(`✅ ${oldEntries.length}개의 로그가 ${archiveName}으로 보관되었습니다.`);
}

rotateLog();
