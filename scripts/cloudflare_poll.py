#!/usr/bin/env python3
"""
Cloudflare WAF to Wazuh Event Poller
LearnCyber Academy | yourdomain.com

Polls the Cloudflare GraphQL API for security events and writes them
to a log file monitored by Wazuh. Runs as a systemd service.

Requirements:
    pip install requests --break-system-packages

Configuration:
    Set CF_API_TOKEN and CF_ZONE_ID below before deploying.
    
Systemd service file: /etc/systemd/system/cloudflare-wazuh.service
"""

import requests
import json
import time
import os
from datetime import datetime, timezone, timedelta

# --- CONFIGURATION ---
CF_API_TOKEN  = "YOUR_CLOUDFLARE_API_TOKEN"
CF_ZONE_ID    = "YOUR_CLOUDFLARE_ZONE_ID"
LOG_FILE      = "/var/log/cloudflare-events.log"
STATE_FILE    = "/opt/cloudflare-wazuh/last_seen.txt"
POLL_INTERVAL = 300  # 5 minutes

GRAPHQL_URL = "https://api.cloudflare.com/client/v4/graphql"

HEADERS = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_since():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

def save_since(timestamp):
    with open(STATE_FILE, "w") as f:
        f.write(timestamp)

def fetch_events(since):
    until = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    query = """
    query FirewallEvents($zoneTag: String, $filter: FirewallEventsAdaptiveFilter_InputObject) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          firewallEventsAdaptive(
            filter: $filter
            limit: 100
            orderBy: [datetime_DESC]
          ) {
            action
            clientIP
            clientCountryName
            clientAsn
            clientRequestPath
            clientRequestQuery
            clientRequestHTTPMethodName
            clientRequestHTTPHost
            userAgent
            datetime
            source
            ruleId
            rayName
          }
        }
      }
    }
    """
    variables = {
        "zoneTag": CF_ZONE_ID,
        "filter": {
            "datetime_geq": since,
            "datetime_leq": until
        }
    }
    resp = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={"query": query, "variables": variables}
    )
    if resp.status_code == 200:
        data = resp.json()
        zones = data.get("data", {}).get("viewer", {}).get("zones", [])
        if zones:
            return zones[0].get("firewallEventsAdaptive", [])
    else:
        print(f"[{datetime.now()}] Error: {resp.status_code} {resp.text}")
    return []

def write_to_log(events):
    with open(LOG_FILE, "a") as f:
        for event in events:
            log_entry = {
                "timestamp":   event.get("datetime"),
                "source":      "cloudflare",
                "zone":        "yourdomain.com",
                "action":      event.get("action"),
                "client_ip":   event.get("clientIP"),
                "country":     event.get("clientCountryName"),
                "method":      event.get("clientRequestHTTPMethodName"),
                "host":        event.get("clientRequestHTTPHost"),
                "path":        event.get("clientRequestPath"),
                "user_agent":  event.get("userAgent"),
                "rule_id":     event.get("ruleId"),
                "waf_source":  event.get("source"),
                "ray_id":      event.get("rayName"),
            }
            f.write(json.dumps(log_entry) + "\n")

def main():
    os.makedirs("/opt/cloudflare-wazuh", exist_ok=True)
    print(f"[{datetime.now()}] Starting Cloudflare WAF event poller...")
    while True:
        since = get_since()
        print(f"[{datetime.now()}] Fetching events since {since}")
        events = fetch_events(since)
        if events:
            print(f"[{datetime.now()}] Fetched {len(events)} events")
            write_to_log(events)
            save_since(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        else:
            print(f"[{datetime.now()}] No new events")
            save_since(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
