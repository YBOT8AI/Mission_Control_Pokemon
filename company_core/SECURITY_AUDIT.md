# Security Audit — Workspace Sanitization

**Date:** 2026-04-24  
**Auditor:** YBOT  
**Status:** 🟢 Clear for GitHub Commit

---

## ✅ Files Cleared for Public Repo

The following files contain **no sensitive data** and are ready to be pushed to `YBOT8AI/Dashboard` and `YBOT8AI/Orbitx-NFT`:

- `company_core/dashboard/dashboard.md` (Public status board)
- `orbitx/core/manifesto.md` (Public mission statement)
- `orbitx/artist_outreach/outreach_scripts.md` (Public templates)
- `orbitx/operations/hiring_plan_v2.md` (High-level strategy, no salaries listed)
- `vercel_configs/*.json` (Public build configs)

## ⚠️ Files to KEEP PRIVATE (Do NOT Commit)

The following files contain **sensitive context** and must **NEVER** be pushed to GitHub:

- `TOOLS.md` (Contains local SSH details, camera names, TTS prefs)
- `USER.md` (Contains personal info about TOBY NG)
- `memory/*.md` (Daily logs, private thoughts, heartbeat state)
- `MEMORY.md` (Long-term private memory)
- `AGENTS.md` (Internal operating instructions)
- `SOUL.md` (Persona definition)
- `IDENTITY.md` (Internal ID)
- `.ssh/` folder (Private Keys — **CRITICAL**)

## 🔒 Recommended `.gitignore`

Ensure this `.gitignore` is in the root of both repos:

```gitignore
# OpenClaw Internal
TOOLS.md
USER.md
MEMORY.md
AGENTS.md
SOUL.md
IDENTITY.md
memory/
state/
.openclaw/

# System
.DS_Store
Thumbs.db
*.log

# Secrets
.env
*.key
*.pem
```

---

*Audit complete. Workspace is safe to commit.*
