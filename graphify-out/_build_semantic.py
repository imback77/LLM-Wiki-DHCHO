import json
from pathlib import Path

semantic = {
    "nodes": [
        {"id": "andrej_karpathy", "label": "Andrej Karpathy", "file_type": "document", "source_file": "wiki/Andrej Karpathy.md", "source_location": None, "source_url": "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f", "captured_at": None, "author": None, "contributor": None},
        {"id": "llm_wiki_pattern", "label": "LLM Wiki Pattern", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "ai_second_brain", "label": "AI Second Brain", "file_type": "document", "source_file": "wiki/AI Second Brain.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "obsidian", "label": "Obsidian", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "antigravity", "label": "Antigravity", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "graphify", "label": "Graphify", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "pkm", "label": "PKM (Personal Knowledge Management)", "file_type": "document", "source_file": "wiki/AI Second Brain.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "obsidian_web_clipper", "label": "Obsidian Web Clipper", "file_type": "document", "source_file": "wiki/AI Second Brain.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "raw_folder", "label": "raw/ Folder", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "wiki_folder", "label": "wiki/ Folder", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "output_folder", "label": "output/ Folder", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "ingest_op", "label": "Ingest Operation", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "query_op", "label": "Query Operation", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "lint_op", "label": "Lint Operation", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "rag", "label": "RAG (Retrieval Augmented Generation)", "file_type": "document", "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "knowledge_compounding", "label": "Knowledge Compounding", "file_type": "document", "source_file": "wiki/AI Second Brain.md", "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None},
        {"id": "brain_trinity_summary", "label": "Summary: Brain Trinity LLM Wiki Video", "file_type": "document", "source_file": "wiki/summary.md", "source_location": None, "source_url": "https://www.youtube.com/watch?v=cNlvrU-KcRg", "captured_at": "2026-04-16", "author": "Brain Trinity", "contributor": None}
    ],
    "edges": [
        {"source": "andrej_karpathy", "target": "llm_wiki_pattern", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/Andrej Karpathy.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "ai_second_brain", "relation": "conceptually_related_to", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "obsidian", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "antigravity", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "graphify", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "raw_folder", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "wiki_folder", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "output_folder", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "ingest_op", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "query_op", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "lint_op", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "rag", "relation": "conceptually_related_to", "confidence": "EXTRACTED", "confidence_score": 0.9, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0},
        {"source": "ai_second_brain", "target": "pkm", "relation": "conceptually_related_to", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/AI Second Brain.md", "source_location": None, "weight": 1.0},
        {"source": "ai_second_brain", "target": "obsidian_web_clipper", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/AI Second Brain.md", "source_location": None, "weight": 1.0},
        {"source": "ai_second_brain", "target": "knowledge_compounding", "relation": "conceptually_related_to", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/AI Second Brain.md", "source_location": None, "weight": 1.0},
        {"source": "ai_second_brain", "target": "antigravity", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/AI Second Brain.md", "source_location": None, "weight": 1.0},
        {"source": "ai_second_brain", "target": "graphify", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/AI Second Brain.md", "source_location": None, "weight": 1.0},
        {"source": "brain_trinity_summary", "target": "andrej_karpathy", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/summary.md", "source_location": None, "weight": 1.0},
        {"source": "brain_trinity_summary", "target": "llm_wiki_pattern", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/summary.md", "source_location": None, "weight": 1.0},
        {"source": "brain_trinity_summary", "target": "ai_second_brain", "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/summary.md", "source_location": None, "weight": 1.0},
        {"source": "obsidian_web_clipper", "target": "raw_folder", "relation": "references", "confidence": "INFERRED", "confidence_score": 0.9, "source_file": "wiki/AI Second Brain.md", "source_location": None, "weight": 1.0},
        {"source": "antigravity", "target": "wiki_folder", "relation": "references", "confidence": "INFERRED", "confidence_score": 0.9, "source_file": "wiki/AI Second Brain.md", "source_location": None, "weight": 1.0},
        {"source": "llm_wiki_pattern", "target": "knowledge_compounding", "relation": "semantically_similar_to", "confidence": "INFERRED", "confidence_score": 0.85, "source_file": "wiki/LLM Wiki Pattern.md", "source_location": None, "weight": 1.0}
    ],
    "hyperedges": [
        {"id": "three_layer_arch", "label": "LLM Wiki 3-Layer Architecture", "nodes": ["raw_folder", "wiki_folder", "output_folder"], "relation": "form", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md"},
        {"id": "three_ops", "label": "LLM Wiki 3 Operations", "nodes": ["ingest_op", "query_op", "lint_op"], "relation": "form", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "wiki/LLM Wiki Pattern.md"},
        {"id": "dhcho_toolchain", "label": "DHCHO Tool Chain", "nodes": ["obsidian", "antigravity", "graphify", "obsidian_web_clipper"], "relation": "form", "confidence": "EXTRACTED", "confidence_score": 0.95, "source_file": "wiki/AI Second Brain.md"}
    ],
    "input_tokens": 3200,
    "output_tokens": 1100
}

Path("graphify-out/.graphify_semantic.json").write_text(
    json.dumps(semantic, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(f"Semantic: {len(semantic['nodes'])} nodes, {len(semantic['edges'])} edges, {len(semantic['hyperedges'])} hyperedges")
