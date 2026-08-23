#!/bin/bash
# Mission Control launcher — opens the dashboard in a standalone browser window.
# ── CUSTOM DOMAIN: change BASE_URL below to your domain (e.g. "https://mission.ybot.hk") ──
BASE_URL="https://ybot8ai.github.io/Mission_Control_Pokemon"
URL="${MISSION_CONTROL_URL:-$BASE_URL}"

open -a "Google Chrome" --args --app="$URL/" 2>/dev/null || \
open -a "Safari" "$URL/" 2>/dev/null || \
open "$URL/"
