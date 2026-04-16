# Graph Report - wiki  (2026-04-16)

## Corpus Check
- Corpus is ~1,468 words - fits in a single context window. You may not need a graph.

## Summary
- 17 nodes · 23 edges · 5 communities detected
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.88)
- Token cost: 3,200 input · 1,100 output

## Community Hubs (Navigation)
- [[_COMMUNITY_LLM Wiki Architecture|LLM Wiki Architecture]]
- [[_COMMUNITY_Knowledge Tools|Knowledge Tools]]
- [[_COMMUNITY_AI Second Brain|AI Second Brain]]
- [[_COMMUNITY_Operations & Workflow|Operations & Workflow]]
- [[_COMMUNITY_Knowledge Concepts|Knowledge Concepts]]

## God Nodes (most connected - your core abstractions)
1. `LLM Wiki Pattern` - 14 edges
2. `AI Second Brain` - 7 edges
3. `Antigravity` - 3 edges
4. `Summary: Brain Trinity LLM Wiki Video` - 3 edges
5. `Andrej Karpathy` - 2 edges
6. `Graphify` - 2 edges
7. `Obsidian Web Clipper` - 2 edges
8. `raw/ Folder` - 2 edges
9. `wiki/ Folder` - 2 edges
10. `Knowledge Compounding` - 2 edges

## Surprising Connections (you probably didn't know these)
- `LLM Wiki Pattern` --semantically_similar_to--> `Knowledge Compounding`  [INFERRED] [semantically similar]
  wiki/LLM Wiki Pattern.md → wiki/AI Second Brain.md
- `Andrej Karpathy` --references--> `LLM Wiki Pattern`  [EXTRACTED]
  wiki/Andrej Karpathy.md → wiki/LLM Wiki Pattern.md
- `LLM Wiki Pattern` --conceptually_related_to--> `AI Second Brain`  [EXTRACTED]
  wiki/LLM Wiki Pattern.md → wiki/AI Second Brain.md
- `Summary: Brain Trinity LLM Wiki Video` --references--> `LLM Wiki Pattern`  [EXTRACTED]
  wiki/summary.md → wiki/LLM Wiki Pattern.md
- `AI Second Brain` --references--> `Antigravity`  [EXTRACTED]
  wiki/AI Second Brain.md → wiki/LLM Wiki Pattern.md

## Hyperedges (group relationships)
- **LLM Wiki 3-Layer Architecture** — raw_folder, wiki_folder, output_folder [EXTRACTED 1.00]
- **LLM Wiki 3 Operations** — ingest_op, query_op, lint_op [EXTRACTED 1.00]
- **DHCHO Tool Chain** — obsidian, antigravity, graphify, obsidian_web_clipper [EXTRACTED 0.95]

## Communities

### Community 0 - "LLM Wiki Architecture"
Cohesion: 0.29
Nodes (7): Ingest Operation, Lint Operation, LLM Wiki Pattern, Obsidian, output/ Folder, Query Operation, RAG (Retrieval Augmented Generation)

### Community 1 - "Knowledge Tools"
Cohesion: 0.5
Nodes (4): AI Second Brain, Graphify, Knowledge Compounding, PKM (Personal Knowledge Management)

### Community 2 - "AI Second Brain"
Cohesion: 1.0
Nodes (2): Andrej Karpathy, Summary: Brain Trinity LLM Wiki Video

### Community 3 - "Operations & Workflow"
Cohesion: 1.0
Nodes (2): Antigravity, wiki/ Folder

### Community 4 - "Knowledge Concepts"
Cohesion: 1.0
Nodes (2): Obsidian Web Clipper, raw/ Folder

## Knowledge Gaps
- **7 isolated node(s):** `Obsidian`, `PKM (Personal Knowledge Management)`, `output/ Folder`, `Ingest Operation`, `Query Operation` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `AI Second Brain`** (2 nodes): `Andrej Karpathy`, `Summary: Brain Trinity LLM Wiki Video`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Operations & Workflow`** (2 nodes): `Antigravity`, `wiki/ Folder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Knowledge Concepts`** (2 nodes): `Obsidian Web Clipper`, `raw/ Folder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLM Wiki Pattern` connect `LLM Wiki Architecture` to `Knowledge Tools`, `AI Second Brain`, `Operations & Workflow`, `Knowledge Concepts`?**
  _High betweenness centrality (0.794) - this node is a cross-community bridge._
- **Why does `AI Second Brain` connect `Knowledge Tools` to `LLM Wiki Architecture`, `AI Second Brain`, `Operations & Workflow`, `Knowledge Concepts`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `raw/ Folder` connect `Knowledge Concepts` to `LLM Wiki Architecture`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Obsidian`, `PKM (Personal Knowledge Management)`, `output/ Folder` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._