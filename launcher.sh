#!/bin/bash
# Mission Control launcher — opens the dashboard in a standalone browser window
URL="https://ybot8ai.github.io/Mission_Control_Pokemon/"
open -a "Google Chrome" --args --app="$URL" 2>/dev/null || \
open -a "Safari" "$URL" 2>/dev/null || \
open "$URL"
