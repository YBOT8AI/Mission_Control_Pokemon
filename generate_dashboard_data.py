#!/usr/bin/env python3
"""
generate_dashboard_data.py
Generates a fresh data.json for the Mission Control dashboard from live sources.
Run: python3 generate_dashboard_data.py
Output: /Users/ybot/Mission_Control_Pokemon/data.json
"""

import json
import subprocess
import os
import sys
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
REPO_DIR = "/Users/ybot/Mission_Control_Pokemon"
DATA_FILE = os.path.join(REPO_DIR, "data.json")

# ── Project definitions ──────────────────────────────────────────────
PROJECTS = {
    "orbitx": {
        "name": "OrbitX NFT",
        "emoji": "🌌",
        "pokemon": "Mewtwo",
        "pokemonId": 150,
        "status": "pre-launch",
        "phase": "1 - Fine Arts",
        "repo": "evilmoni/Orbitx-NFT",
        "local_path": "/Users/ybot/Orbitx-NFT",
        "priority": "high",
        "classification": "CONFIDENTIAL",
    },
    "kinkin": {
        "name": "KINKIN",
        "emoji": "🚀",
        "pokemon": "Pikachu",
        "pokemonId": 25,
        "status": "deploying",
        "url": "kinkin.vercel.app",
        "repo": "evilmoni/KinKin",
        "local_path": "/Users/ybot/KinKin",
        "priority": "high",
        "classification": "CONFIDENTIAL",
    },
    "techwealth": {
        "name": "TechWealth",
        "emoji": "💼",
        "pokemon": "Meowth",
        "pokemonId": 52,
        "status": "building",
        "focus": "Financial Tech",
        "repo": "evilmoni/TechWealth",
        "local_path": "/Users/ybot/TechWealth",
        "priority": "high",
        "classification": "CONFIDENTIAL",
    },
    "techwealthTracker": {
        "name": "TechWealth Tracker Pro",
        "emoji": "📊",
        "pokemon": "Kadabra",
        "pokemonId": 64,
        "status": "deploying",
        "repo": "evilmoni/TechWealth-Tracker-Pro",
        "local_path": "/Users/ybot/TechWealth-Tracker-Pro",
        "priority": "high",
        "classification": "CONFIDENTIAL",
    },
    "wpo": {
        "name": "WPO (World Paws Org)",
        "emoji": "🐾",
        "pokemon": "Chansey",
        "pokemonId": 113,
        "status": "standby",
        "phase": "Option B - Full Build",
        "blockchain": "Solana",
        "repo": "WorldPaws/WorldPawsOrg_Website",
        "local_path": "/Users/ybot/WorldPawsOrg_Website",
        "priority": "medium",
        "classification": "INTERNAL",
    },
    "aeroview": {
        "name": "Aeroview",
        "emoji": "🚁",
        "pokemon": "Dragonite",
        "pokemonId": 149,
        "status": "planning",
        "focus": "Drone Fleet Management",
        "phase": "Concept Definition",
        "repo": "evilmoni/AEROVIEW",
        "local_path": None,  # Repo not yet cloned locally
        "priority": "medium",
        "classification": "INTERNAL",
    },
}


def run(cmd, timeout=15):
    """Run a shell command, return (stdout, success)."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode == 0
    except Exception as e:
        return str(e), False


def get_cron_statuses():
    """Get cron job statuses by parsing hermes cron list text output."""
    out, ok = run("hermes cron list 2>/dev/null", timeout=10)
    if not ok or not out:
        return {"error": "hermes cron list failed", "jobs": [], "total": 0, "healthy": 0}

    cron_jobs = []
    current = None

    for line in out.split("\n"):
        line = line.strip()
        if not line:
            continue

        # New job entry: "  <job_id> [active|paused]"
        if line and not line.startswith("│") and not line.startswith("┌") and not line.startswith("└") and not line.startswith("Name:") and not line.startswith("Schedule:") and not line.startswith("Repeat:") and not line.startswith("Next run:") and not line.startswith("Deliver:") and not line.startswith("Script:") and not line.startswith("Mode:") and not line.startswith("Last run:") and not line.startswith("Skills:") and "[" in line and "]" in line:
            if current:
                cron_jobs.append(current)
            # Parse: "  c4a0f2b0c07e [active]"
            parts = line.split()
            job_id = parts[0] if parts else ""
            state = parts[1].strip("[]") if len(parts) > 1 else "unknown"
            current = {"id": job_id, "enabled": state == "active", "name": "", "schedule": "", "last_status": "unknown", "last_run": None, "next_run": None}
            continue

        if not current:
            continue

        if line.startswith("Name:"):
            current["name"] = line.replace("Name:", "").strip()
        elif line.startswith("Schedule:"):
            current["schedule"] = line.replace("Schedule:", "").strip()
        elif line.startswith("Next run:"):
            current["next_run"] = line.replace("Next run:", "").strip()
        elif line.startswith("Last run:"):
            rest = line.replace("Last run:", "").strip()
            # Format: "2026-08-08T09:00:37.725831+08:00  ok" or "... error: ..."
            if "  ok" in rest:
                current["last_run"] = rest.split("  ok")[0].strip()
                current["last_status"] = "ok"
            elif "  error:" in rest:
                parts_err = rest.split("  error:", 1)
                current["last_run"] = parts_err[0].strip()
                current["last_status"] = "error"
            else:
                current["last_run"] = rest
                current["last_status"] = "unknown"

    if current:
        cron_jobs.append(current)

    return {
        "jobs": cron_jobs,
        "total": len(cron_jobs),
        "healthy": sum(1 for j in cron_jobs if j.get("last_status") == "ok"),
    }


def get_git_stats(local_path):
    """Get git stats for a local repo."""
    if not local_path or not os.path.isdir(local_path):
        return None

    stats = {}

    # Last commit
    out, ok = run(f"cd {local_path} && git log -1 --format='%H|%s|%an|%aI' 2>/dev/null", timeout=5)
    if ok and out:
        parts = out.split("|", 3)
        if len(parts) >= 4:
            stats["lastCommit"] = {
                "sha": parts[0][:7],
                "message": parts[1][:80],
                "author": parts[2],
                "time": parts[3],
            }

    # Commit count (last 30 days)
    out, ok = run(f"cd {local_path} && git rev-list --count HEAD --since='30 days ago' 2>/dev/null", timeout=5)
    if ok and out:
        stats["commits30d"] = int(out.strip())

    # Total commits
    out, ok = run(f"cd {local_path} && git rev-list --count HEAD 2>/dev/null", timeout=5)
    if ok and out:
        stats["totalCommits"] = int(out.strip())

    # Branch
    out, ok = run(f"cd {local_path} && git branch --show-current 2>/dev/null", timeout=5)
    if ok and out:
        stats["branch"] = out.strip()

    # Uncommitted changes
    out, ok = run(f"cd {local_path} && git status --porcelain 2>/dev/null | wc -l", timeout=5)
    if ok and out:
        stats["uncommittedChanges"] = int(out.strip())

    return stats


def get_hermes_agent_status():
    """Check if Hermes agent is running."""
    out, ok = run("pgrep -f hermes-agent 2>/dev/null | wc -l", timeout=5)
    agent_count = int(out.strip()) if ok and out else 0

    out, ok = run("pgrep -f 'hermes cron' 2>/dev/null | wc -l", timeout=5)
    cron_count = int(out.strip()) if ok and out else 0

    return {
        "hermesAgent": "running" if agent_count > 0 else "stopped",
        "cronScheduler": "running" if cron_count > 0 else "stopped",
        "processCount": agent_count + cron_count,
    }


def get_system_health():
    """System health metrics — CPU, memory, disk, network, top processes."""
    import platform

    # Disk usage
    out, ok = run("df -h / | tail -1 | awk '{print $5, $4}'", timeout=5)
    disk_used, disk_avail = (out.split() + ["?", "?"])[:2] if ok else ("?", "?")

    # Uptime
    out, ok = run("uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}'", timeout=5)
    uptime = out.strip() if ok else "?"

    # CPU: load averages + usage %
    load = []
    out, ok = run("sysctl -n vm.loadavg 2>/dev/null", timeout=5)
    if ok and out:
        load = [float(x) for x in out.replace("{", "").replace("}", "").split()[:3]]

    cpu_usage = "?"
    out, ok = run("top -l 1 -n 0 2>/dev/null | grep 'CPU usage' | awk -F'idle' '{print $1}'", timeout=8)
    if ok and out:
        # e.g. "CPU usage: 19.61% user, 14.83% sys, " → sum user+sys
        import re as _re
        nums = _re.findall(r"([\d.]+)%\s*(user|sys)", out)
        if nums:
            busy = sum(float(n) for n, _ in nums)
            cpu_usage = f"{round(busy, 1)}%"

    # Memory: total (bytes) + used %
    mem_total_gb = "?"
    out, ok = run("sysctl -n hw.memsize 2>/dev/null", timeout=5)
    if ok and out and out.isdigit():
        mem_total_gb = round(int(out) / (1024**3), 1)

    mem_used_pct = "?"
    out, ok = run("vm_stat 2>/dev/null | awk '/Pages active/{a=$3} /Pages wired/{w=$4} /Pages occupied/{o=$3} END{print a+w}'", timeout=5)
    # fallback: use memory_pressure
    if ok and out and out.strip().isdigit():
        pages_used = int(out.strip())
        # approximate: pages * 4096 / total
        out2, ok2 = run("sysctl -n hw.memsize 2>/dev/null", timeout=5)
        if ok2 and out2.isdigit():
            total_bytes = int(out2)
            mem_used_pct = round((pages_used * 4096 / total_bytes) * 100, 1)

    # Network: local IP
    local_ip = "?"
    out, ok = run("ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null", timeout=5)
    if ok and out:
        local_ip = out.strip()

    # Top processes by CPU
    top_procs = []
    out, ok = run("ps -Ao pcpu,pmem,comm -r 2>/dev/null | head -6", timeout=5)
    if ok and out:
        lines = out.split("\n")[1:]  # skip header
        for line in lines:
            parts = line.split(None, 2)
            if len(parts) >= 3:
                top_procs.append({
                    "cpu": parts[0],
                    "mem": parts[1],
                    "name": parts[2].split("/")[-1][:30],
                })

    return {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "diskUsed": disk_used.rstrip("%"),
        "diskAvail": disk_avail,
        "uptime": uptime,
        "cpu": {
            "loadAvg": load,
            "usage": cpu_usage,
        },
        "memory": {
            "totalGb": mem_total_gb,
            "usedPct": mem_used_pct,
        },
        "network": {
            "localIp": local_ip,
        },
        "topProcesses": top_procs,
    }


def get_workout_data():
    """Parse ~/.hermes/workout-log.md into structured training data."""
    import re
    log_path = os.path.expanduser("~/.hermes/workout-log.md")
    result = {
        "exists": False,
        "commitment": {},
        "weeks": [],
        "stats": {"daysLogged": 0, "runsCompleted": 0, "pushupsCompleted": 0, "totalDays": 0},
    }
    if not os.path.isfile(log_path):
        return result

    result["exists"] = True
    try:
        with open(log_path, "r") as f:
            text = f.read()
    except Exception:
        return result

    # Commitment lines
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("- 🏃"):
            result["commitment"]["run"] = s.lstrip("- ").strip()
        elif s.startswith("- 💪"):
            result["commitment"]["pushups"] = s.lstrip("- ").strip()
        elif s.startswith("- Rules"):
            result["commitment"]["rules"] = s.lstrip("- ").strip()

    # Parse weekly tables: rows like | Mon Aug 17 | ✅ 5km | ✅ 100 | ... |
    rows = []
    for line in text.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        # header rows: "Day", "Run (5km)" — skip
        if cells and cells[0].lower() in ("day", "-----", ""):
            continue
        if len(cells) >= 3 and re.search(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", cells[0]):
            rows.append(cells)

    total_days = runs = pushups = 0
    for r in rows:
        day = r[0] if len(r) > 0 else ""
        run_cell = r[1] if len(r) > 1 else ""
        pu_cell = r[2] if len(r) > 2 else ""
        notes = r[3] if len(r) > 3 else ""
        if not day:
            continue
        total_days += 1
        run_done = "✅" in run_cell and "❌" not in run_cell
        pu_done = "✅" in pu_cell
        if run_done:
            runs += 1
        if pu_done:
            pushups += 1

    result["weeks"] = [
        {"day": r[0], "run": r[1], "pushups": r[2], "notes": r[3] if len(r) > 3 else ""}
        for r in rows
    ]
    result["stats"] = {
        "daysLogged": total_days,
        "runsCompleted": runs,
        "pushupsCompleted": pushups,
        "totalDays": total_days,
    }

    # Current streak estimate: count trailing consecutive ✅ runs
    streak = 0
    for r in reversed(rows):
        run_cell = r[1] if len(r) > 1 else ""
        if "✅" in run_cell and "❌" not in run_cell:
            streak += 1
        elif "❌" in run_cell or "—" in run_cell:
            # a rest day or miss breaks the "never miss twice" streak only if not makeup
            continue
        else:
            break
    result["stats"]["currentStreak"] = streak

    return result


def get_sub_agents(cron_data):
    """Build the sub-agent roster, cross-referencing live cron jobs."""
    jobs = cron_data.get("jobs", []) if cron_data else []
    job_names = " ".join(j.get("name", "") for j in jobs)

    def status_for(needle):
        if needle.lower() in job_names.lower():
            return "active"
        return "standby"

    roster = [
        {"name": "Lawania", "emoji": "⚖️", "role": "Legal Compliance", "status": status_for("Lawania")},
        {"name": "Dr. Demi", "emoji": "🩺", "role": "Health & Biohacking", "status": status_for("Dr. Demi")},
        {"name": "Noelle", "emoji": "📅", "role": "Personal Assistant", "status": status_for("Noelle")},
        {"name": "Agent-Bling Bling", "emoji": "💎", "role": "Investment Strategist", "status": status_for("Bling")},
        {"name": "Lucky 8", "emoji": "🎱", "role": "TechWealth Revenue Team", "status": status_for("Lucky 8")},
        {"name": "Future Me 44", "emoji": "🔮", "role": "Future Self Advisor", "status": status_for("Future Me")},
    ]

    # Find the cron job names/schedules for each
    for a in roster:
        match = next((j for j in jobs if a["name"].lower() in j.get("name", "").lower()), None)
        if match:
            a["schedule"] = match.get("schedule", "")
            a["lastStatus"] = match.get("last_status", "unknown")
            a["lastRun"] = match.get("last_run")

    return roster


def get_github_activity():
    """Fetch recent commit activity across all repos via GitHub API."""
    import urllib.request
    import urllib.error

    def _fetch_commit_message(repo, sha, token):
        """Resolve a commit message from its SHA when the event payload is truncated."""
        url = f"https://api.github.com/repos/{repo}/commits/{sha}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "mission-control"})
        if token:
            req.add_header("Authorization", f"token {token}")
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
            return (data.get("commit", {}) or {}).get("message", "")
        except Exception:
            return ""

    # Read token from ~/.git-credentials (format: https://user:token@github.com)
    token = None
    cred_path = os.path.expanduser("~/.git-credentials")
    if os.path.isfile(cred_path):
        try:
            with open(cred_path) as f:
                for line in f:
                    if "github.com" in line:
                        token = line.strip().split("@github.com")[0].rsplit(":", 1)[-1]
                        break
        except Exception:
            pass

    repos = [p.get("repo", "") for p in PROJECTS.values() if p.get("repo")]
    events = []

    for repo in repos:
        if not repo:
            continue
        url = f"https://api.github.com/repos/{repo}/events?per_page=15"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "mission-control"})
        if token:
            req.add_header("Authorization", f"token {token}")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
        except Exception:
            continue

        for ev in data:
            etype = ev.get("type", "")
            if etype not in ("PushEvent", "PullRequestEvent", "IssuesEvent", "CreateEvent", "DeleteEvent", "ReleaseEvent"):
                continue
            actor = (ev.get("actor") or {}).get("login", "unknown")
            created = ev.get("created_at", "")
            repo_name = (ev.get("repo") or {}).get("name", repo)
            title = ""
            detail = ""
            if etype == "PushEvent":
                payload = ev.get("payload", {})
                commits = payload.get("commits", [])
                if commits:
                    title = commits[-1].get("message", "")[:60]
                else:
                    # GitHub truncates commit arrays on busy repos — resolve via head SHA
                    head_sha = payload.get("head", "")
                    if head_sha:
                        cmsg = _fetch_commit_message(repo, head_sha, token)
                        title = (cmsg or "")[:60]
                    if not title:
                        title = head_sha[:7] if head_sha else "push"
                detail = f"{payload.get('size', 1)} commit(s)"
            elif etype == "PullRequestEvent":
                pr = ev.get("payload", {}).get("pull_request", {})
                title = pr.get("title", "")[:60]
                detail = (ev.get("payload", {}).get("action", "") or "").title()
            elif etype == "IssuesEvent":
                iss = ev.get("payload", {}).get("issue", {})
                title = iss.get("title", "")[:60]
                detail = (ev.get("payload", {}).get("action", "") or "").title()
            elif etype == "CreateEvent":
                title = (ev.get("payload", {}).get("ref_type", "") or "") + " " + (ev.get("payload", {}).get("ref", "") or "")
            elif etype == "ReleaseEvent":
                title = (ev.get("payload", {}).get("release", {}) or {}).get("name", "release")
                detail = "Release"
            else:
                title = etype

            events.append({
                "repo": repo_name,
                "type": etype,
                "actor": actor,
                "time": created,
                "title": title,
                "detail": detail,
            })

    events.sort(key=lambda x: x.get("time", ""), reverse=True)
    return events[:40]


def get_research_buddy():
    """Parse the AI research buddy state + journal into structured data."""
    base = os.path.expanduser("~/ai-research-buddy")
    result = {
        "exists": False,
        "state": {},
        "journal": [],
        "lastUpdated": None,
    }
    state_path = os.path.join(base, "state.md")
    journal_path = os.path.join(base, "journal.md")

    if not os.path.isdir(base):
        return result
    result["exists"] = True

    # Parse state.md
    if os.path.isfile(state_path):
        try:
            with open(state_path) as f:
                state_text = f.read()
        except Exception:
            state_text = ""

        def grab_section(heading):
            import re as _re
            lines = []
            in_section = False
            for line in state_text.split("\n"):
                if line.startswith("## " + heading):
                    in_section = True
                    continue
                if in_section and line.startswith("## "):
                    break
                if in_section:
                    s = line.strip()
                    # bullet "- item" or numbered "1. item"
                    if s.startswith("- "):
                        lines.append(s[2:].strip())
                    elif _re.match(r"^\d+\.\s+", s):
                        lines.append(_re.sub(r"^\d+\.\s+", "", s).strip())
            return lines

        result["state"] = {
            "meta": {
                "created": "",
                "lastUpdated": "",
                "cycles": "",
            },
            "hierarchy": grab_section("Research Hierarchy"),
            "currentFocus": grab_section("Current Focus"),
            "activeHypotheses": grab_section("Active Hypotheses"),
            "openQuestions": grab_section("Open Questions"),
            "completedResearch": grab_section("Completed Research"),
            "nextSteps": grab_section("Next Steps"),
            "keyInsights": grab_section("Key Insights"),
        }
        # Meta lines
        for line in state_text.split("\n"):
            s = line.strip()
            if s.startswith("- Created:"):
                result["state"]["meta"]["created"] = s.split(":", 1)[-1].strip()
            elif s.startswith("- Last updated:"):
                result["state"]["meta"]["lastUpdated"] = s.split(":", 1)[-1].strip()
                result["lastUpdated"] = s.split(":", 1)[-1].strip()
            elif s.startswith("- Cycles run:"):
                result["state"]["meta"]["cycles"] = s.split(":", 1)[-1].strip()

    # Parse journal.md (reverse chronological)
    if os.path.isfile(journal_path):
        try:
            with open(journal_path) as f:
                journal_text = f.read()
        except Exception:
            journal_text = ""
        entries = []
        current = None
        for line in journal_text.split("\n"):
            s = line.strip()
            if s.startswith("## "):
                if current:
                    entries.append(current)
                current = {"date": s.lstrip("# ").strip(), "items": []}
            elif current and s.startswith("-"):
                current["items"].append(s.lstrip("- ").strip())
        if current:
            entries.append(current)
        result["journal"] = entries

    return result


def build_activity_log(git_stats, cron_data):
    """Build activity log from real data."""
    activities = []
    now = datetime.now(HKT).isoformat()

    # Git commits from all projects
    for key, proj in PROJECTS.items():
        stats = git_stats.get(key, {})
        if stats and stats.get("lastCommit"):
            activities.append({
                "time": stats["lastCommit"]["time"],
                "type": "success",
                "text": f"{proj['emoji']} {proj['name']}: {stats['lastCommit']['message']}",
                "project": key,
            })

    # Cron status summary
    if cron_data.get("jobs"):
        ok_count = cron_data.get("healthy", 0)
        total = cron_data.get("total", 0)
        if total > 0:
            activities.append({
                "time": now,
                "type": "info",
                "text": f"⏰ Cron: {ok_count}/{total} jobs healthy",
            })

    # Sort by time descending
    activities.sort(key=lambda x: x["time"], reverse=True)

    # Add generation marker
    activities.insert(0, {
        "time": now,
        "type": "info",
        "text": "🔄 Dashboard data auto-generated from live sources",
    })

    return activities[:25]


def main():
    print("🔍 Generating Mission Control dashboard data...")

    # 1. Cron statuses
    print("  📋 Fetching cron job statuses...")
    cron_data = get_cron_statuses()
    print(f"     → {cron_data.get('total', 0)} jobs, {cron_data.get('healthy', 0)} healthy")

    # 2. Git stats for each project
    print("  📦 Fetching git stats...")
    git_stats = {}
    for key, proj in PROJECTS.items():
        path = proj.get("local_path")
        if path and os.path.isdir(path):
            stats = get_git_stats(path)
            if stats:
                git_stats[key] = stats
                lc = stats.get("lastCommit", {})
                print(f"     → {proj['name']}: {stats.get('totalCommits', 0)} commits, last: {lc.get('time', 'N/A')}")
            else:
                print(f"     → {proj['name']}: no git data")
        else:
            print(f"     → {proj['name']}: repo not found at {path}")

    # 3. Agent status
    print("  🤖 Checking agent status...")
    agent_status = get_hermes_agent_status()
    print(f"     → Hermes: {agent_status['hermesAgent']}, Cron: {agent_status['cronScheduler']}")

    # 4. System health
    print("  💻 System health...")
    sys_health = get_system_health()
    print(f"     → {sys_health['hostname']}, disk: {sys_health['diskUsed']}% used")

    # 5. Workout / training data
    print("  🏋️ Workout log...")
    workout_data = get_workout_data()
    print(f"     → {workout_data['stats'].get('daysLogged', 0)} days logged, streak: {workout_data['stats'].get('currentStreak', 0)}")

    # 6. Sub-agent roster
    print("  🤖 Sub-agent roster...")
    sub_agents = get_sub_agents(cron_data)
    print(f"     → {len(sub_agents)} agents")

    # 7. GitHub activity feed
    print("  📊 GitHub activity...")
    github_activity = get_github_activity()
    print(f"     → {len(github_activity)} events")

    # 8. Research buddy insights
    print("  🧠 Research buddy...")
    research_buddy = get_research_buddy()
    print(f"     → cycles: {research_buddy.get('state', {}).get('meta', {}).get('cycles', '?')}")

    # 9. Build activity log
    activity = build_activity_log(git_stats, cron_data)

    # 6. Assemble final data.json
    now = datetime.now(HKT).isoformat()

    # Build projects section
    projects_out = {}
    for key, proj in PROJECTS.items():
        gs = git_stats.get(key, {})
        lc = gs.get("lastCommit", {})

        # Calculate progress: known_progress is the FLOOR, git activity can boost it
        commits30 = gs.get("commits30d", 0)
        total_commits = gs.get("totalCommits", 0)
        known_progress = {
            "orbitx": 75, "kinkin": 90, "techwealth": 55,
            "techwealthTracker": 85, "wpo": 45, "aeroview": 20,
        }
        base = known_progress.get(key, 50)

        # Git activity bonus: recent commits push progress above the floor
        if commits30 >= 30:
            progress = min(98, base + 15)
        elif commits30 >= 10:
            progress = min(95, base + 10)
        elif commits30 >= 3:
            progress = min(92, base + 5)
        else:
            progress = base

        entry = {
            "name": proj["name"],
            "emoji": proj["emoji"],
            "pokemon": proj["pokemon"],
            "pokemonId": proj["pokemonId"],
            "status": proj["status"],
            "progress": progress,
            "repo": proj.get("repo", ""),
            "priority": proj.get("priority", "medium"),
            "classification": proj.get("classification", "INTERNAL"),
            "git": {
                "lastCommit": lc,
                "commits30d": commits30,
                "totalCommits": total_commits,
                "branch": gs.get("branch", "main"),
                "uncommittedChanges": gs.get("uncommittedChanges", 0),
            },
        }

        # Add project-specific fields
        for field in ["phase", "url", "focus", "blockchain", "build"]:
            if field in proj:
                entry[field] = proj[field]

        projects_out[key] = entry

    # Build agents section
    agents_out = {
        "hermes": {
            "name": "Hermes Agent",
            "emoji": "⚡",
            "status": agent_status["hermesAgent"],
            "role": "AI Assistant & Automation",
        },
        "cron": {
            "name": "Cron Scheduler",
            "emoji": "⏰",
            "status": agent_status["cronScheduler"],
            "role": "Scheduled Task Runner",
        },
    }

    data = {
        "generatedAt": now,
        "generatedBy": "generate_dashboard_data.py",
        "source": "live-local",
        "refreshIntervalSeconds": 60,
        "projects": projects_out,
        "cron": cron_data,
        "agents": agents_out,
        "systemHealth": sys_health,
        "workout": workout_data,
        "subAgents": sub_agents,
        "githubActivity": github_activity,
        "researchBuddy": research_buddy,
        "activity": activity,
        "stats": {
            "totalProjects": len(PROJECTS),
            "totalCronJobs": cron_data.get("total", 0),
            "healthyCronJobs": cron_data.get("healthy", 0),
            "avgProgress": round(sum(p["progress"] for p in projects_out.values()) / len(projects_out)),
        },
    }

    # Write data.json
    os.makedirs(REPO_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ data.json written ({os.path.getsize(DATA_FILE)} bytes)")
    print(f"   Path: {DATA_FILE}")
    print(f"   Projects: {len(projects_out)}")
    print(f"   Cron jobs: {cron_data.get('total', 0)}")
    print(f"   Activity entries: {len(activity)}")
    print(f"   Avg progress: {data['stats']['avgProgress']}%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
