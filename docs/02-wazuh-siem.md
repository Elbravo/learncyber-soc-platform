# 02 — Wazuh SIEM

## Version

Wazuh 4.14.5 — deployed as an all-in-one installation (manager + indexer + dashboard on a single node).

## Access

- Dashboard: `https://wazuh.yourdomain.com`
- API: `https://localhost:55000` (internal only)
- Authentication: SSO via LearnCyber Academy management system

## Log Sources

| Source | Format | Location |
|--------|--------|----------|
| Cowrie honeypot | JSON | `/home/cowrie/cowrie/var/log/cowrie/cowrie.json` |
| Suricata IDS | JSON | `/var/log/suricata/eve.json` |
| System auth | Syslog | `/var/log/auth.log` |
| Wazuh agent (Windows) | Agent | staff-laptop (Agent ID: 001) |
| Cloudflare WAF | JSON | `/var/log/cloudflare-events.log` |

## Custom Detection Rules

Rules are stored in `/var/ossec/etc/rules/`. See `wazuh/rules/` in this repository for the full rule files.

### Rule ranges

| Range | Count | Purpose |
|-------|-------|---------|
| 100001–100070 | 70 | SOC scenarios: brute force, privilege escalation, persistence, lateral movement, credential access |
| 200001–200008 | 8 | Cowrie honeypot: session events, login attempts, command execution, file downloads |
| 300001–300013 | 13 | AWS CloudTrail: root usage, IAM escalation, S3 exposure, GuardDuty tampering |
| 400001–400010 | 10 | Enhanced MITRE ATT&CK: LOLBin abuse, process injection, indicator removal |
| 100300–100304 | 5 | Suricata elevation: ET DROP, ET CINS, ET SCAN, ET EXPLOIT, ET MALWARE |

### Alert level thresholds

| Level | Meaning | Example |
|-------|---------|---------|
| 3 | Informational | Background Suricata noise |
| 7+ | Minimum stored | System enforced minimum |
| 8 | Medium | Network reconnaissance (ET SCAN) |
| 10 | High | Blocklisted IP (ET DROP / ET CINS) |
| 12 | Critical | Exploit attempt (ET EXPLOIT / Mozi botnet) |
| 15 | Maximum | Reserved for confirmed active compromise |

## Alert Fatigue Management

Two mechanisms prevent alert overload:

**1 — Minimum alert level:**
```xml
<alerts>
  <log_alert_level>7</log_alert_level>
  <email_alert_level>12</email_alert_level>
</alerts>
```

**2 — Frequency suppression on noisy rules:**
```xml
<rule id="100300" level="10" timeframe="3600" frequency="5">
  <if_matched_sid>86601</if_matched_sid>
  <match>ET DROP</match>
  ...
</rule>
```
Rules 100300, 100301, and 100302 only fire after 5 triggers within a 1-hour window.

## JSON Decoder Configuration

Suricata's eve.json contains more fields than Wazuh's default JSON decoder limit. Fix applied in `/var/ossec/etc/local_internal_options.conf`:

```
analysisd.decoder_json_buffer=65536
analysisd.decoder_json_max_fields=200
```

## Compliance Modules Active

| Framework | Status | Used in |
|-----------|--------|---------|
| GDPR | Active | GRC track Week 6 |
| NIST 800-53 | Active | GRC track Week 10 |
| PCI DSS | Active | SOC track + GRC track |
| HIPAA | Active | Reference |
| TSC | Active | Reference |

## Wazuh Index Retention

Indices set to auto-delete after 90 days via Index Management policy applied to `wazuh-alerts-*` pattern.
