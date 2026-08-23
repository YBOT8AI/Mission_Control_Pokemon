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
    """Basic system health metrics."""
    import platform

    # Disk usage
    out, ok = run("df -h / | tail -1 | awk '{print $5, $4}'", timeout=5)
    disk_used, disk_avail = (out.split() + ["?", "?"])[:2] if ok else ("?", "?")

    # Uptime
    out, ok = run("uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}'", timeout=5)
    uptime = out.strip() if ok else "?"

    return {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "diskUsed": disk_used.rstrip("%"),
        "diskAvail": disk_avail,
        "uptime": uptime,
    }


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

    # 5. Build activity log
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
