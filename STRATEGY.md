# 🏰 THE EMPIRE — Master Strategy File

> **Last updated:** August 24, 2026 | **Age:** 33 | **Retire:** 55 (22 years / 264 months / ~8,000 days)
> **This file is auto-reviewed every Sunday. Hermes reorganizes for strategic priority.**

---

## 1. THE VISION

### Lifestyle Goals
| Asset | Cost (HKD) | Timeline |
|-------|-----------|----------|
| 🏠 China house (Shenzhen/Luohu) | ✅ OWNED | Now |
| 🚙 Zeekr 009 (6-seat executive) | $907,500 | 2027 |
| 🪪 蓮塘中港牌 (cross-border license) | ~$870,000 | 2027 |
| 👨‍✈️ Private driver | $28,000/mo | 2027 |
| 🏎️ Ferrari 488 GTB (used) | $2,000,000 | 2027 |
| 🏎️ Lamborghini Huracan (used) | $2,500,000 | 2028 |

**Total one-time:** ~HK$6,277,500 | **Ongoing:** ~HK$56,000/month

### Body Goals
| Metric | Current | Target |
|--------|---------|--------|
| Weight | 89 kg | 80–85 kg |
| Body fat | ~19.5% | ≤12% |
| Muscle mass | 39 kg | 42+ kg |
| Training | 3 days/week | 6 days/week + abs daily |

---

## 2. RETIREMENT MATH

### The Number: HK$62,000,000 (2050 HKD)

| Level | Monthly | Nest Egg |
|-------|---------|----------|
| Lean | $50K | $28.7M |
| **Comfortable** | **$108K** | **$62M** |
| Luxury | $200K | $115M |

### What It Takes
- Invest **~HK$120,000/month** for 22 years at 7% return
- Or: build ventures generating **HK$500K+/month profit**
- Or: one exit at **HK$30M+** and invest the lump sum

---

## 3. THE VENTURES (Wealth Engines)

### Priority Order (by revenue potential × readiness)

| # | Venture | Progress | Revenue Potential | Next Action |
|---|---------|----------|-------------------|-------------|
| 1 | **TechWealth** | 90% (product) / 0% (business) | $200K–$1M/mo | Launch premium tiers, onboard first 50 members |
| 2 | **TechWealth Tracker Pro** *(merged Client Tracker Pro 2026-08-24)* | 85% | $20K–$50K/mo | SaaS subscriptions for HK SMEs |
| 3 | **OrbitX NFT** | 75% | $50K–$200K/mo | Phase 2 music marketplace |
| 4 | **KinKin** | 60% | $30K–$100K/mo | Booking flow + payment integration |
| 5 | **Aeroview** | 60% | TBD | Field testing |
| 6 | **World Paws Org** | 20% | TBD | Fundraising campaign |
| 7 | **Robotics / SENTINEL RISK** | Research | TBD | HK security-robotics-as-a-service; autonomous risk-transfer platform (see `~/Robotics/`, `~/autonomous-security-firm/`) |

**Combined potential:** $300K–$850K+/month

---

## 4. TECHWEALTH — THE FLAGSHIP

### Core Principle
"Leverage collective human capital for explosive client acquisition."
Gated HNW business networking. Members pay tiered fees → platform credits. 15% transaction fee on deals.

### Premium Pricing Tiers

| Tier | Monthly | Deal Fee | Key Perk |
|------|---------|----------|----------|
| Free | $0 | 15% | Basic access |
| **Option A** | $0 | 15% | Pay only when you profit. No deal in 6mo → free lifetime |
| **Option B** | $288 | 10% | 1 curated intro/month + monthly report |
| **Option C** | $888 | 5% | Priority deals (48h), 3 intros, events, concierge |
| **Option D** | $741* | 5% | Everything + first deal fee waived |

*\*Annual equivalent of $8,888/year*

### The Guarantee
> "If you don't close a single deal within 12 months of paid membership, we refund every dollar."

### Revenue Math (200 members)
- Subscriptions: ~HK$670,000/year
- Deal fees: ~HK$2,000,000/year
- **Combined: ~HK$2.67M/year**

### What's Left to Build
- [x] Tiered membership + checkout (premium tiers) — ✅ DONE (lucky8 deliberation, 2026-08-20: fixed webhook idempotency, tier/plan confusion, provisioning downgrade)
- [x] Monetization tables in production — ✅ DONE (2026-08-27: `RUN_THIS.sql` applied via Supabase Management API; all 7 tables + `paid_tier`/`paid_at`/`password_setup_token` now live)
- [ ] **Deploy to Vercel + push env vars** — the real launch blocker now. Needs `vercel login` + `vercel link`, then `node scripts/sync-vercel-env.mjs --apply` (script now includes all 4 Stripe vars)
- [ ] Rotate leaked Supabase `service_role` key (2026-08-22 finding)
- [ ] Swap Stripe `sk_test_` → `sk_live_` + add `STRIPE_WEBHOOK_SECRET`
- [ ] Automated monthly intelligence report (Hermes)
- [ ] Invite first 10 members (free trial) — manual outreach

> ✅ Concierge form, refund/guarantee tracking, and all 12 pages are live. See `TechWealth/docs/EXECUTION_PLAN.md` Appendix A for full product status.

---

## 5. THE CRITICAL PATH

```
NOW ────► TechWealth Launch ────► $150K/mo revenue
              │
              ▼
       Zeekr 009 + 中港牌 + Driver (2027)
              │
              ▼
       $250K/mo ────► Ferrari 488 (2027)
              │
              ▼
       $350K/mo ────► Lamborghini Huracan (2028)
              │
              ▼
       $500K/mo ────► Everything paid off, retire at 55
```

---

## 6. THIS WEEK'S ACTIONS

| # | Action | Impact |
|---|--------|--------|
| 1 | Launch TechWealth premium tiers | Unlocks recurring revenue |
| 2 | Invite first 10 members (free trial) | Builds network effects |
| 3 | Set up Stripe/Firebase payment webhook | Enables paid tiers |
| 4 | Open dedicated "Zeekr Fund" savings account | Psychology + tracking |
| 5 | Test drive Zeekr 009 at HK showroom | Motivation |
| 6 | Train: Chest Monday, Back Tuesday, Legs Wednesday | Fighter physique |

---

## 7. DAILY NON-NEGOTIABLES

- 🏋️ Train (6 days/week per plan)
- 🥩 180–200g protein
- 💧 3–4L water
- 🚶 30–45 min walk
- 💼 Move TechWealth forward (even 15 min)
- 📊 Check morning briefing

---

## 8. KEY METRICS

| Metric | Current | Target |
|--------|---------|--------|
| Monthly income | ? | $500,000+ |
| Active revenue streams | 0 | 4–6 |
| Net worth | ? | $62M (2050) |
| Body fat % | 19.5% | 12% |
| Weight | 89 kg | 82 kg |
| Cars in garage | 0 | 3 |
| Days to retirement | ~8,000 | 0 |

---

*Auto-reviewed every Sunday by Hermes. Duplicates merged. Priorities reordered. New ideas integrated.*
