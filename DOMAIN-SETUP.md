# Mission Control — Custom Domain Setup

> Everything is now **domain-agnostic** (relative paths). When you buy a domain, follow these steps and it'll work with zero code changes.

## Current state (pre-domain)
- Live at: `https://ybot8ai.github.io/Mission_Control_Pokemon/`
- All asset/data URLs are **relative** (`./icons/...`, `data.json`, `market.json`, `sw.js`) → they resolve correctly on ANY origin/subpath.
- `manifest.json` uses `start_url: "./"` and `scope: "./"` → works on both subpath and custom domain.
- `sw.js` cache is versioned (`mission-control-v4`) and serves HTML/JSON/manifest network-first → always fresh.

## When you buy a domain (e.g. `mission.ybot.hk`)

### Option A — Subdomain (recommended, cleanest)
Map `mission.ybot.hk` → the repo.

1. **DNS (at your registrar/Cloudflare):** add a `CNAME` record:
   - Name: `mission`
   - Target: `ybot8ai.github.io`
2. **GitHub:** repo → **Settings → Pages → Custom domain** → enter `mission.ybot.hk` → Save.
   - This auto-creates a `CNAME` file in the repo root and provisions a Let's Encrypt cert (enable **Enforce HTTPS**).
3. **Wait ~10 min** for DNS + cert propagation.

### Option B — Apex domain (e.g. `ybotmission.com`)
1. **DNS:** add 4 `A` records → GitHub's IPs (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`).
2. **GitHub:** Settings → Pages → Custom domain → `ybotmission.com`.
3. Wait for propagation + cert.

## After DNS resolves — one-time local updates

The **macOS `.app` launcher** reads a `BASE_URL` variable. Update it to your domain:

```bash
# /Users/ybot/Applications/Mission Control.app/Contents/MacOS/launcher.sh
BASE_URL="https://mission.ybot.hk"   # ← change this one line
```

Then refresh the app: `touch "/Users/ybot/Applications/Mission Control.app" && killall Dock`.

## Re-install PWA (iOS/Android)

The home-screen icon is tied to the old origin. On the new domain:
1. Open the domain in the browser.
2. **Share → Add to Home Screen**.

## Rollback
Revert `BASE_URL` in launcher.sh back to `https://ybot8ai.github.io/Mission_Control_Pokemon` — the GitHub Pages URL keeps working even after a custom domain is attached (it just redirects).

## Checklist
- [ ] Domain purchased (recommend Cloudflare registrar — no markup)
- [ ] DNS record added (CNAME or A)
- [ ] GitHub Pages custom domain entered + Enforce HTTPS on
- [ ] `CNAME` file committed
- [ ] launcher.sh `BASE_URL` updated
- [ ] PWA re-added on new origin
