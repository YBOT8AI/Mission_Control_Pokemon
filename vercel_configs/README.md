# Vercel Deployment Configs

**Prepared by:** YBOT  
**Date:** 2026-04-24  
**Purpose:** Instant deployment for OrbitX projects once GitHub access is granted.

---

## 📁 File Structure

These configs are ready to be committed to the root of their respective repos.

### 1. **Dashboard Repo (`YBOT8AI/Dashboard`)**
- **File:** `vercel.json`
- **Goal:** Serve `index.html` (converted from `dashboard.md`) at the root domain.
- **Build Command:** None (Static HTML).
- **Output Directory:** `/`

### 2. **OrbitX NFT Repo (`YBOT8AI/Orbitx-NFT`)**
- **File:** `vercel.json`
- **Goal:** Configure rewrites for a Next.js or React app.
- **Build Command:** `npm run build`
- **Output Directory:** `.next` or `/build`

---

## 🚀 Deployment Instructions (For TOBY)

Once YBOT pushes the code:

1.  Go to [vercel.com/new](https://vercel.com/new).
2.  **Import Git Repository:** Select `YBOT8AI/Dashboard`.
3.  **Framework Preset:** Select "Other" (it's static HTML).
4.  **Root Directory:** `./`
5.  Click **Deploy**.
    *   *Result:* Your dashboard is live at `https://dashboard-orbitx.vercel.app` (or custom domain).

6.  **Import Git Repository:** Select `YBOT8AI/Orbitx-NFT`.
7.  **Framework Preset:** Select "Next.js" (or appropriate framework).
8.  Click **Deploy**.
    *   *Result:* Your marketplace landing page is live.

---

## 🔗 Custom Domains (Optional)

After deployment:
1.  Go to Project Settings → Domains.
2.  Add `dashboard.orbitx.io` or `orbitx.art`.
3.  Update DNS records as instructed by Vercel.

*Configs ready. Awaiting GitHub push.*
