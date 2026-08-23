# AGENTS.md — Mission Control (Portfolio Dashboard + Identity Hub)

This is YBOT's unified portfolio dashboard and identity hub. It contains identity, memory, strategy, and a unified API for the portfolio.

## What's Here
- **SOUL.md** — YBOT's core identity and prime directives
- **IDENTITY.md** — Personality and behavioral rules
- **AGENTS.md** — This file (workspace rules)
- **api/index.js** — Unified backend API serving OrbitX and KinKin
- **memory/** — Daily logs and long-term memory
- **orbitx/** — Strategic docs, hiring plans, artist outreach
- **company_core/** — Dashboard configs, security audits
- **vercel_configs/** — Per-project Vercel deployment configs

## Rules
- Don't modify SOUL.md or IDENTITY.md without explicit user request
- Memory files in `memory/` are append-only — don't delete history
- The unified API (`api/index.js`) is the single source of truth for project data
- When working on any portfolio project, check here first for context
