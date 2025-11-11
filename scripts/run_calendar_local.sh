#!/bin/bash
# Quick wrapper to run calendar update locally with refresh token
# Usage: ./scripts/run_calendar_local.sh <refresh_token>
# Or: GOOGLE_CALENDAR_REFRESH_TOKEN="..." ./scripts/run_calendar_local.sh

if [ -z "$GOOGLE_CALENDAR_REFRESH_TOKEN" ]; then
    if [ -z "$1" ]; then
        echo "Error: No refresh token provided"
        echo ""
        echo "Usage:"
        echo "  ./scripts/run_calendar_local.sh <refresh_token>"
        echo ""
        echo "Or set the env var first:"
        echo "  export GOOGLE_CALENDAR_REFRESH_TOKEN='...'"
        echo "  ./scripts/run_calendar_local.sh"
        exit 1
    fi
    export GOOGLE_CALENDAR_REFRESH_TOKEN="$1"
fi

# Extract client ID/secret from credentials.json
export GOOGLE_CLIENT_ID="$(python3 -c 'import json;print(json.load(open("credentials.json"))["installed"]["client_id"])')"
export GOOGLE_CLIENT_SECRET="$(python3 -c 'import json;print(json.load(open("credentials.json"))["installed"]["client_secret"])')"

echo "Running calendar update with refresh token..."
echo "Client ID: $GOOGLE_CLIENT_ID"
echo ""

python3 scripts/update_calendar.py
