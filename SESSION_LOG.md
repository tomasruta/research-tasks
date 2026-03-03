# SESSION_LOG

## Session 1 — 2026-03-03

**Duration:** ~2 hours
**Task:** Systematic scan of every YC company (2024–2025+ batches) to map the agent infrastructure landscape

### What was built

Complete pipeline to identify YC companies building picks-and-shovels for the agent economy:

1. **`fetch_yc_batches.py`** — Fetched 1,468 companies across 13 batches (W24–W26) from the YC Open API (`yc-oss.github.io/api/`)
2. **`filter_candidates.py`** — Two-tier keyword filter requiring both AI signal AND infrastructure signal. Narrowed to 178 candidates (score ≥ 8)
3. **`fetch_websites.py`** — Bulk-fetched 178 candidate websites with httpx. 159 OK, 13 empty (JS-rendered), 4 connection errors, 2 timeouts
4. **`classify_candidates.py`** — Merge script for classifications → final CSV
5. **`data/classifications.jsonl`** — 175 hand-classified companies (3 duplicates across batches)
6. **`data/yc_agent_infra_classified.csv`** — Final classified dataset
7. **`yc_agent_infra_summary.md`** — Full summary report with clickable links for every company
8. **`yc_agent_infra_deep_dive.md`** — Deep-dive analysis of all 48 AGENT-INFRA-DIRECT companies

### Classification breakdown

| Category | Count |
|---|---|
| AGENT-INFRA-DIRECT | 48 |
| AGENT-INFRA-ADJACENT | 48 |
| AGENT-AS-PRODUCT | 57 |
| NOT-RELEVANT | 22 |

### Key decisions & reasoning

- **YC Open API over scraping** — Fully open, no auth, no rate limits, all fields needed. Way faster than scraping YC directory.
- **Regex HTML extraction over BeautifulSoup** — Avoided adding dependencies. Regex was sufficient for text extraction from marketing sites.
- **Two-tier keyword filter** — Initial single-tier was too broad (781 matches). Restructured to require both AI signal AND infrastructure signal, which brought it to 178 high-quality candidates.
- **In-conversation classification over API** — Claude classified all 175 companies in batches of ~25, reading name + one_liner + extracted website text. More accurate than keyword-only approaches.
- **Four categories, not two** — Separating AGENT-INFRA-DIRECT from AGENT-AS-PRODUCT is critical: direct infra companies are potential partners/competitors, agent-as-product companies are potential Agent LLC customers.

### Key finding

**No YC company is building legal entity infrastructure for AI agents.** The Agent LLC Act occupies a genuine white space. Closest adjacencies: Anon (agent identity/auth), Skyfire (agent payments), Payman AI (agent payments), Giselle (agent governance/guardrails).

### What's next

- Review the summary and deep-dive reports
- Cross-reference with Agent LLC Act positioning
- Potentially reach out to HIGH-relevance companies (Anon, Skyfire, Payman AI, Giselle, Patched)
- Repeat scan in 3–6 months as more batches launch
