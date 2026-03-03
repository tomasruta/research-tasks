# YC Agent Infrastructure Deep Dive — AGENT-INFRA-DIRECT Companies

*Scan date: March 3, 2026*
*Batches covered: W24, S24, F24, W25, X25, Spring 2025, Summer 2025, Fall 2025, Winter 2026*

---

## PAYMENTS LAYER

### Locus (Fall 2025)
**Website:** [https://paywithlocus.com](https://paywithlocus.com)
**What they build:** Payment infrastructure for autonomous AI agents. Programmatic APIs for USDC payments, freelancer escrow, and purchases — all governed by configurable spending policies and human-in-the-loop approvals.
**Key features:** USDC escrow, spending limits, policy enforcement, complete audit trails
**Pricing:** Free to use (as listed)
**Funding:** YC-backed (F25)
**WAC relevance:** HIGH — Directly solves the "how does an agent pay for things" problem. Escrow + policy enforcement maps to Agent LLC Act's need for agent financial controls. Could be a natural partner or integration target.

### Orthogonal (Winter 2026)
**Website:** [https://orthogonal.com](https://orthogonal.com)
**What they build:** "Trusted Skills and APIs" — building blocks agents need. Works with Claude Code, Codex, Cursor, and more. 15+ partners including Notte, Didit, Brand.dev.
**Funding:** YC W26
**WAC relevance:** MEDIUM — Enables agent economic activity through verified API skills. Less about payments directly, more about trusted agent-to-service interactions.

### Protegee (F24)
**Website:** [http://protegee.ai](http://protegee.ai)
**What they build:** Originally "Payments API for AI Agents." Website now shows redirect to Attimet.
**WAC relevance:** LOW — Appears to have pivoted away from agent payments.

### Maven (Winter 2026)
**Website:** [https://www.trymaven.com](https://www.trymaven.com)
**What they build:** Payments Layer for Voice AI Agents. Enables agents to collect payments during live voice calls. Callers can speak card details or receive SMS payment links. Card data never touches agent servers.
**Integrations:** Stripe, Authorize.net, Adyen, Braintree. Voice platforms: VAPI, Retell, LiveKit, Twilio.
**Funding:** YC W26 (Lambda Systems, Inc.)
**WAC relevance:** MEDIUM — Niche (voice-only payments) but proves the agent-needs-payments thesis.

---

## IDENTITY & AUTH LAYER

### Alter (Summer 2025)
**Website:** [https://alterai.dev](https://alterai.dev)
**What they build:** Zero-trust identity and access control for AI agents. Wraps every tool call in authentication, authorization, and real-time guardrails. Manages ephemeral credentials scoped per interaction.
**Key features:** Parameter-level authorization, least-privilege access, credential rotation in seconds, full audit trails
**Funding:** YC S25
**WAC relevance:** HIGH — Core agent identity infrastructure. If agents are legal entities, they need identity/auth. Alter is building exactly this layer.

### Multifactor (Fall 2025)
**Website:** [https://multifactor.com](https://multifactor.com)
**What they build:** Secure online account sharing for humans AND AI agents. Uses "Checkpoint" technology in trusted execution environments. Agents never see raw credentials — system generates temporary session tokens. Fine-grained permissions per account feature.
**Key features:** Granular permissions, cryptographic audit trails, post-quantum encryption, instant revocation
**Pricing:** Free for consumers, custom enterprise pricing
**Funding:** YC F25, Pioneer Fund, NSF, Zcash Foundation
**WAC relevance:** HIGH — Solves how agents access existing online services without credential exposure. Critical for Agent LLC operations.

### A1Base (W25)
**Website:** [https://www.a1base.com](https://www.a1base.com)
**What they build:** "Twilio for AI Agents" — API to give agents a phone number, email, and trusted identity. Products include A1Mail (email) and A1Verify (identity verification).
**Location:** San Francisco
**Funding:** YC W25
**WAC relevance:** HIGH — Directly gives agents communication identity. Phone + email + verification = agent persona. Natural fit for Agent LLC infrastructure.

### Agentic Fabriq (Fall 2025)
**Website:** [https://www.agenticfabriq.com](https://www.agenticfabriq.com) (JS-rendered, no content extracted)
**What they build:** "Okta for Agents" — agent identity management.
**Funding:** YC F25
**WAC relevance:** HIGH — If they deliver on the Okta-for-agents promise, this is a core identity layer.

### Keet (S24)
**Website:** [https://trykeet.com](https://trykeet.com)
**What they build:** Originally "Authentication for AI Agents." Website now shows "Automated enterprise onboarding."
**WAC relevance:** LOW — Pivoted away from agent auth.

---

## SAFETY, GOVERNANCE & GUARDRAILS LAYER

### Salus (Winter 2026)
**Website:** [https://www.usesalus.ai](https://www.usesalus.ai)
**What they build:** Runtime guardrails that validate every agent tool call before execution. Blocks incorrect actions, returns structured feedback for self-correction. Pre-deployment adversarial testing.
**Integrations:** OpenAI, Anthropic, LangChain, LangGraph, CrewAI
**Funding:** YC W26
**WAC relevance:** HIGH — If agents are legal entities, they need action validation. Salus provides the "before you act, check" layer that Agent LLC compliance would require.

### truthsystems (Summer 2025)
**Website:** [https://www.truthsystems.ai](https://www.truthsystems.ai)
**What they build:** AI governance infrastructure for legal and professional firms. Browser extension monitors AI tool usage, converts policies into intelligent guardrails, blocks non-compliant prompts, captures audit trails.
**Team:** Alex Mac (CEO), Nam Nguyen (COO, ex-Legora legal AI), Mikolaj Bochenski (Founding Engineer)
**Funding:** YC S25, Pear VC, UCLA, Legal Tech Fund
**WAC relevance:** HIGH — Legal-sector focused governance. Directly relevant to how law firms would manage Agent LLCs.

### TectoAI (Summer 2025)
**Website:** [https://www.tecto.ai](https://www.tecto.ai)
**What they build:** AI Governance for Regulated Enterprise. Governance for AI Agents in regulated industries. (Website JS-rendered, limited content)
**Funding:** YC S25
**WAC relevance:** MEDIUM — Governance for regulated industries maps to Agent LLC compliance needs.

### General Analysis (S24)
**Website:** [https://generalanalysis.com](https://generalanalysis.com)
**What they build:** Security for Agentic AI. RL-trained adversarial models for multi-step exploit discovery. Runtime guardrails, safety classifiers, AI asset management.
**Key features:** Red teaming, vulnerability forecasting, MCP integration security, GA Guard open-source safety classifiers
**Team:** Alumni from NVIDIA, Jane Street, DeepMind, Cohere, Snap, NASA, Caltech, Harvard, CMU
**Funding:** YC S24
**WAC relevance:** MEDIUM — Security layer for agentic systems. Necessary for any agent operating autonomously.

### Galini (F24)
**Website:** [https://www.galini.ai](https://www.galini.ai) (minimal content)
**What they build:** Compliance guardrails-as-a-service for AI applications.
**Funding:** YC F24
**WAC relevance:** MEDIUM — Compliance guardrails, but limited information available.

---

## EXECUTION & SANDBOX LAYER

### Blaxel (X25)
**Website:** [https://blaxel.ai](https://blaxel.ai)
**What they build:** Persistent sandbox platform for AI agents. MicroVMs with auto-suspend ($0 when idle), 25ms cold start, in-memory filesystems with snapshots, MCP gateway.
**Key features:** 50,000+ concurrent sandboxes, co-located agent logic + MCP servers + inference, block storage, preview URLs
**Pricing:** Usage-based (pay for active compute only)
**Funding:** YC X25
**WAC relevance:** MEDIUM — Execution environment where agents actually run. If Agent LLCs need sandboxed operations, this is where they'd live.

### Castari (Fall 2025)
**Website:** [https://castari.com](https://castari.com)
**What they build:** Deployment platform for Claude Agent SDK. Import from GitHub or generate from prompts, one-click deploy, auto-scaling sandboxes, MCP gateway, model router, agent observability.
**Key features:** <150ms cold start, tool tracing, output logging, multi-model support
**Pricing:** Free during beta, usage-based after
**Funding:** YC F25, AWS, Google Cloud partners
**WAC relevance:** LOW — Deployment infra, not specific to agents-as-entities.

### Scrapybara (F24)
**Website:** [https://scrapybara.com](https://scrapybara.com)
**What they build:** Virtual Desktops for AI Agents. Hosts remote desktop instances for computer use.
**Funding:** YC F24
**WAC relevance:** LOW — Execution infra, not entity-specific.

### Butter (Winter 2025)
**Website:** [https://butter.dev](https://butter.dev)
**What they build:** Local Agent Sandboxes. bVisor lightweight sandbox runtime embedded in local processes. Formerly Pig (Windows automation).
**Funding:** YC W25
**WAC relevance:** LOW — Local execution sandbox.

### Kernel (Summer 2025)
**Website:** [https://www.kernel.sh](https://www.kernel.sh)
**What they build:** Browser infrastructure for web agents. Open source.
**Funding:** YC S25
**WAC relevance:** LOW — Browser execution layer.

### Cyberdesk (Summer 2025)
**Website:** [https://www.cyberdesk.io](https://www.cyberdesk.io)
**What they build:** Computer use agent for Windows. Self-learning. For healthcare, finance, legacy systems.
**Funding:** YC S25
**WAC relevance:** LOW — Computer use execution.

### Truffle AI (W25)
**Website:** [https://www.trytruffle.ai](https://www.trytruffle.ai) (JS-rendered)
**What they build:** "AWS for AI Agents"
**Funding:** YC W25
**WAC relevance:** LOW — Cloud platform for agents.

---

## MEMORY & CONTEXT LAYER

### Zep AI (W24)
**Website:** [https://www.getzep.com](https://www.getzep.com)
**What they build:** Context Engineering and Agent Memory Platform. Ingests chat, JSON, documents. Builds temporal knowledge graph that evolves over time. Graph RAG with <200ms retrieval.
**Key features:** 80.32% accuracy on LoCoMo benchmark, SOC 2 Type II + HIPAA, Graphiti open-source library
**Clients:** WebMD, Swiggy, AWS
**Funding:** YC W24
**WAC relevance:** MEDIUM — Agents need memory. If an Agent LLC operates over time, it needs persistent context. Zep provides this.

### Hyperspell (Fall 2025)
**Website:** [https://hyperspell.com](https://hyperspell.com)
**What they build:** Memory and Context Layer for AI Agents. Connects to user data, builds knowledge graphs, continuous indexing. SOC 2 + GDPR compliant.
**Key features:** 5-minute setup, one-line integration, multi-source document processing
**Team:** Conor and Manu (co-founders)
**Funding:** YC F25
**WAC relevance:** MEDIUM — Agent memory for user-facing agents.

### Nozomio (Summer 2025)
**Website:** [https://www.nozomio.com](https://www.nozomio.com) (empty)
**What they build:** Context augmentation for agents.
**Funding:** YC S25
**WAC relevance:** LOW — Limited info.

---

## MCP & TOOL-USE LAYER

### Dedalus Labs (Summer 2025)
**Website:** [https://www.dedaluslabs.ai](https://www.dedaluslabs.ai)
**What they build:** MCP Cloud for Production Agents. Drop-in gateway connecting LLMs to MCP servers. Most secure MCP Auth framework. SDK (Python/TypeScript) for multi-model orchestration.
**Integrations:** Claude, Gemini, DeepSeek, Mistral
**Funding:** YC S25
**WAC relevance:** MEDIUM — MCP infrastructure is how agents access tools and services.

### Klavis AI (X25 / Spring 2025)
**Website:** [https://www.klavis.ai](https://www.klavis.ai)
**What they build:** MCP infrastructure for AI to use tools reliably at scale. Open source.
**Funding:** YC (two batches: X25 and Spring 2025)
**WAC relevance:** MEDIUM — Tool-use infrastructure for agents.

### Manufact / mcp-use (Summer 2025)
**Website:** [https://manufact.com](https://manufact.com)
**What they build:** Build and Deploy MCP Agents, Servers, and Apps. Registry, SDK, cloud hosting. Open source.
**Funding:** YC S25
**WAC relevance:** MEDIUM — MCP deployment infrastructure.

### Golf (X25)
**Website:** [https://golf.dev](https://golf.dev) (JS-rendered)
**What they build:** Agentic AI and MCP Security & Governance for Enterprises. Control layer for remote MCP servers.
**Funding:** YC X25
**WAC relevance:** HIGH — MCP governance/security. Controls what agents can access through MCP.

---

## OBSERVABILITY & TESTING LAYER

### Roark (W25)
**Website:** [https://roark.ai](https://roark.ai)
**What they build:** "Datadog for Voice AI." Monitoring, evaluation, simulations, and testing for voice agents. Multi-speaker analysis, 40+ metrics.
**Funding:** YC W25
**WAC relevance:** LOW — Observability for voice agents.

### Hamming AI (S24)
**Website:** [https://hamming.ai](https://hamming.ai)
**What they build:** Enterprise Voice Agent Testing and Production Monitoring.
**Funding:** YC S24
**WAC relevance:** LOW — Voice agent testing.

### Sentrial (Winter 2026)
**Website:** [https://sentrial.com](https://sentrial.com) (empty)
**What they build:** Production Monitoring for AI Agents.
**Funding:** YC W26
**WAC relevance:** LOW — Agent monitoring.

### The Context Company (Fall 2025)
**Website:** [https://thecontext.company](https://thecontext.company)
**What they build:** Monitor AI agents and understand user behavior. See where users get confused or stuck.
**Funding:** YC F25
**WAC relevance:** LOW — Agent UX analytics.

### Cekura (Fall 2024)
**Website:** [https://www.cekura.ai](https://www.cekura.ai)
**What they build:** Automated QA for Voice AI and Chat AI Agents. $2.4M raised.
**Funding:** YC F24
**WAC relevance:** LOW — Agent testing.

### Lucidic AI (W25)
**Website:** [https://lucidic.ai](https://lucidic.ai)
**What they build:** Training Platform for Reliable AI Agents. W&B for agents.
**Funding:** YC W25
**WAC relevance:** LOW — Agent training/evaluation.

### Lemma (Fall 2025)
**Website:** [https://www.uselemma.ai](https://www.uselemma.ai)
**What they build:** Continuous Learning for AI Agents. Monitor behavior, turn failures into improvements.
**Funding:** YC F25
**WAC relevance:** LOW — Agent improvement.

### ZeroEval (Summer 2025)
**Website:** [https://zeroeval.com](https://zeroeval.com)
**What they build:** Auto-optimizer for AI agents. Calibrated LLM judges.
**Funding:** YC S25
**WAC relevance:** LOW — Agent optimization.

### Relari (W24)
**Website:** [https://www.relari.ai](https://www.relari.ai)
**What they build:** Testing and Simulation Stack for GenAI Systems.
**Funding:** YC W24
**WAC relevance:** LOW — GenAI testing.

### AgentHub (Summer 2025)
**Website:** [https://www.agenthublabs.com](https://www.agenthublabs.com) (empty)
**What they build:** Simulation and evaluation engine for AI agents.
**Funding:** YC S25
**WAC relevance:** LOW — Agent evaluation.

### Janus (Spring 2025)
**Website:** [https://www.withjanus.com](https://www.withjanus.com)
**What they build:** Evaluate AI Agents with Simulation Environments. Video evaluation benchmarks.
**Funding:** YC Spring 2025
**WAC relevance:** LOW — Agent evaluation.

---

## TRAINING & SIMULATION LAYER

### Osmosis (Winter 2025)
**Website:** [https://osmosis.ai](https://osmosis.ai)
**What they build:** Forward Deployed RL Platform for AI Agents.
**Funding:** YC W25
**WAC relevance:** LOW — RL training.

### Foundry (F24)
**Website:** [https://www.foundryrl.com](https://www.foundryrl.com)
**What they build:** Simulation and data engine for AI web agents. Enterprise browser intelligence.
**Funding:** YC F24
**WAC relevance:** LOW — Browser agent simulation.

### Vibrant Labs (Winter 2024)
**Website:** [https://vibrantlabs.com](https://vibrantlabs.com)
**What they build:** Simulation environments for long-horizon AI agents.
**Funding:** YC W24
**WAC relevance:** LOW — Agent simulation.

### Abundant (F24)
**Website:** [https://www.abundant.ai](https://www.abundant.ai)
**What they build:** RL environments and datasets. Human supervision for AI agents.
**Funding:** YC F24
**WAC relevance:** LOW — RL environments.

### Gulp (W25)
**Website:** [https://gulp.ai](https://gulp.ai) → redirects to Osmosis
**What they build:** Agent self-improvement. Appears merged with Osmosis.
**Funding:** YC W25
**WAC relevance:** LOW — Merged/redirected.

---

## DATA & ACCESS LAYER

### Airweave (X25)
**Website:** [https://airweave.ai](https://airweave.ai)
**What they build:** Context Retrieval Layer for AI. Open-source. Lets agents search any app or database.
**Funding:** YC X25
**WAC relevance:** MEDIUM — Universal data access for agents.

### Capacitive (X25)
**Website:** [https://capacitive.ai](https://capacitive.ai)
**What they build:** Enterprise data gateway. Intranet access for agents.
**Funding:** YC X25
**WAC relevance:** MEDIUM — Gives agents access to enterprise systems.

### Praxos (S24)
**Website:** [https://www.praxos.ai](https://www.praxos.ai) (empty)
**What they build:** Data layer for AI agents.
**Funding:** YC S24
**WAC relevance:** LOW — Limited info.

---

## MARKETING & COMMERCE LAYER

### Bear (Fall 2025)
**Website:** [https://usebear.ai](https://usebear.ai)
**What they build:** Marketing Stack for AI Agents. Analytics across ChatGPT/Claude/Gemini/Perplexity, AI-optimized content, lead gen from AI referral traffic.
**Pricing:** $100/mo basic, custom enterprise
**Funding:** YC F25
**WAC relevance:** MEDIUM — If agents shop and recommend, brands need to market to them. Bear is building this new channel.
