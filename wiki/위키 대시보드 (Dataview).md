---
type: dashboard
created: 2026-04-18
updated: 2026-04-18
tags: ["dashboard"]
---

# 📊 위키 대시보드 (Dataview)

> Obsidan Dataview 플러그인이 활성화되어 있어야 아래 쿼리들이 정상적으로 표시됩니다.

---

## ⚡ 최근 업데이트된 지식 (최신 10건)

```dataview
TABLE type, updated
FROM "wiki"
WHERE file.name != "dashboard" AND file.name != "index" AND file.name != "log" AND file.name != "ANTIGRAVITY"
SORT updated DESC
LIMIT 10
```

## 🏗️ 채워야 할 지식 (스텁 페이지)

> 다른 문서에서 언급되었으나 아직 내용이 없는 페이지들입니다. `/fetch`나 `/research`를 통해 내용을 채워보세요.

```dataview
TABLE created
FROM "wiki"
WHERE type = "stub"
SORT created ASC
```

## 📈 지식 분포 (유형별 통계)

```dataview
TABLE length(rows) AS "문서 수"
FROM "wiki"
WHERE file.name != "dashboard" AND file.name != "index" AND file.name != "log" AND file.name != "ANTIGRAVITY"
GROUP BY type
SORT length(rows) DESC
```

## 💰 투자 리서치 현황

```dataview
TABLE type, updated
FROM "wiki"
WHERE type = "stock" OR type = "sector" OR type = "strategy" OR type = "macro" OR type = "thesis"
SORT updated DESC
```
