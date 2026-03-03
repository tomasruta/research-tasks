#!/usr/bin/env python3
"""Step 2: Filter raw YC company list for agent-infrastructure candidates.

Strategy: Require BOTH an AI/agent signal AND an infrastructure signal.
This prevents matching generic payroll companies, insurance companies, etc.
"""

import csv
import os
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
INPUT_FILE = os.path.join(DATA_DIR, "yc_companies_raw.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "yc_candidates.csv")

# Tier 1: Explicitly about agent infrastructure (auto-qualify, score +10)
AGENT_INFRA_PHRASES = [
    r"agent infrastructure", r"agent platform", r"for ai agents",
    r"for agents", r"agent orchestrat", r"agent deploy",
    r"agent monitor", r"agent observab", r"agent memory",
    r"agent evaluat", r"agent test", r"agent runtime",
    r"agent framework", r"multi-agent", r"agent-to-agent",
    r"agent workflow", r"agentic payment", r"agentic infra",
    r"agent identity", r"agent auth", r"agent sandbox",
    r"agent execution", r"payments.*agent", r"agent.*payment",
    r"identity.*agent", r"agent.*identity",
    r"agent.*bank", r"bank.*agent",
    r"aws for ai agent", r"vercel for ai agent",
    r"agent sdk", r"agent api",
]

# Tier 2: AI infra keywords (score +3 each)
AI_INFRA_KEYWORDS = [
    r"\bagentic\b", r"\bmcp\b", r"\bguardrail", r"\bai safety\b",
    r"\bllm infrastructure\b", r"\bai infrastructure\b",
    r"\bllm ops\b", r"\bmlops\b", r"\bmodel serving\b",
    r"\binference\b", r"\bvector database\b", r"\bfine-tun",
    r"\brag\b", r"\bprompt management\b", r"\bprompt engineering\b",
    r"\bai middleware\b", r"\bai gateway\b", r"\bllm gateway\b",
    r"\btool use\b", r"\bfunction calling\b",
    r"\bcomputer use\b", r"\bbrowser automation\b",
    r"\bai sandbox\b", r"\borchestrat.*ai\b", r"\bai.*orchestrat",
    r"\bai observab", r"\bllm evaluat", r"\bai evaluat",
]

# Tier 3: AI company signals (needed for context, score +1)
AI_SIGNALS = [
    r"\bai\b", r"\bartificial intelligence\b", r"\bllm\b",
    r"\blarge language model\b", r"\bgpt\b", r"\bclaude\b",
    r"\bmachine learning\b", r"\bdeep learning\b", r"\bneural\b",
    r"\bagent\b", r"\bagentic\b", r"\bautonomous\b",
    r"\bcopilot\b", r"\bchatbot\b", r"\bgenerat.*ai\b",
    r"\binference\b", r"\bmodel\b",
]

# Tier 4: Infrastructure/financial layer signals (only count if AI signal present, score +2)
INFRA_LAYER_KEYWORDS = [
    r"\binfrastructure\b", r"\bplatform\b", r"\bdeveloper tool",
    r"\bapi\b", r"\bsdk\b", r"\bframework\b",
    r"\bpayment", r"\bwallet\b", r"\bbanking\b",
    r"\bidentity\b", r"\bkyc\b", r"\bauth",
    r"\bcompliance\b", r"\binsurance\b", r"\bcredential",
    r"\bregistry\b", r"\blegal\b", r"\bentity\b",
    r"\bliability\b", r"\bllc\b", r"\btrust\b",
    r"\bstablecoin\b", r"\bcrypto\b", r"\bdefi\b", r"\btoken\b",
    r"\bdeploy", r"\bmonitor", r"\bobservab",
    r"\bworkflow\b", r"\bautomation\b", r"\bsandbox\b",
    r"\bevaluat", r"\bembedding", r"\bpipeline\b",
    r"\bmemory\b", r"\bcontext\b", r"\bbrowser\b",
    r"\bexecution\b", r"\bdispute\b", r"\barbitrat",
]


def score_company(row):
    """Score a company for agent-infrastructure relevance."""
    text = " ".join([
        row.get("one_liner", ""),
        row.get("long_description", ""),
        row.get("tags", ""),
        row.get("industry", ""),
        row.get("subindustry", ""),
    ]).lower()

    score = 0
    matched = []

    # Tier 1: Explicit agent-infra phrases → auto-qualify
    for phrase in AGENT_INFRA_PHRASES:
        if re.search(phrase, text, re.IGNORECASE):
            score += 10
            matched.append(f"T1:{phrase}")

    # Tier 2: AI infra keywords
    for kw in AI_INFRA_KEYWORDS:
        if re.search(kw, text, re.IGNORECASE):
            score += 3
            matched.append(f"T2:{kw}")

    # Check for AI signal
    has_ai = False
    for sig in AI_SIGNALS:
        if re.search(sig, text, re.IGNORECASE):
            has_ai = True
            break

    # Tier 4: Infra layer keywords (only count with AI signal)
    if has_ai:
        for kw in INFRA_LAYER_KEYWORDS:
            if re.search(kw, text, re.IGNORECASE):
                score += 2
                matched.append(f"T4:{kw}")

    # Bonus: AI signal itself adds +1
    if has_ai:
        score += 1

    return score, matched


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    print(f"Read {len(all_rows)} companies from {INPUT_FILE}")

    # Score all companies
    scored = []
    for row in all_rows:
        score, matched = score_company(row)
        if score >= 8:  # Need meaningful signal (not just "has AI + 1 generic keyword")
            row["relevance_score"] = str(score)
            row["matched_keywords"] = "; ".join(matched[:10])
            scored.append(row)

    # Sort by score descending
    scored.sort(key=lambda r: int(r["relevance_score"]), reverse=True)

    print(f"Filtered to {len(scored)} candidates (score >= 6)")

    # Show top 20 for sanity check
    print("\nTop 20 candidates:")
    for c in scored[:20]:
        print(f"  [{c['relevance_score']:>3}] {c['name']}: {c['one_liner'][:80]}")

    # Show score distribution
    print("\nScore distribution:")
    buckets = {}
    for c in scored:
        s = int(c["relevance_score"])
        bucket = f"{(s//5)*5}-{(s//5)*5+4}"
        buckets[bucket] = buckets.get(bucket, 0) + 1
    for b in sorted(buckets.keys(), reverse=True):
        print(f"  {b}: {buckets[b]}")

    # Write output
    if scored:
        fieldnames = list(all_rows[0].keys()) + ["relevance_score", "matched_keywords"]
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(scored)
        print(f"\nWritten to {OUTPUT_FILE}")
    else:
        print("No candidates found!")


if __name__ == "__main__":
    main()
