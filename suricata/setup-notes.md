# Suricata IDS Setup Notes

## Version
Suricata 8.0.5 (or latest stable via PPA)

## Deployment
Suricata is deployed on the Vultr honeypot server (separate from the Wazuh SIEM server).

## Installation

```bash
add-apt-repository ppa:oisf/suricata-stable -y
apt-get update -y
apt-get install -y suricata
```

## Key Configuration (/etc/suricata/suricata.yaml)

```yaml
# Network interface
af-packet:
  - interface: enp1s0

# Home network
vars:
  address-groups:
    HOME_NET: "[YOUR_SERVER_IP/32]"
    EXTERNAL_NET: "!$HOME_NET"

# Log alerts only (not all network events)
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: /var/log/suricata/eve.json
      types:
        - alert
```

## Rules
Emerging Threats Open ruleset — 40,000+ signatures.

```bash
# Initial download
suricata-update

# Weekly auto-update cron
0 3 * * 1 /usr/bin/suricata-update && systemctl restart suricata
```

## Wazuh Integration

Add to /var/ossec/etc/ossec.conf on the agent:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```

Fix permissions:
```bash
chmod 644 /var/log/suricata/eve.json
```

## JSON Decoder Fix
Suricata eve.json exceeds Wazuh's default field limit.
Add to /var/ossec/etc/local_internal_options.conf on the Wazuh manager:

```
analysisd.decoder_json_buffer=65536
analysisd.decoder_json_max_fields=200
```

## Notable Detections

- ET DROP — DShield blocklisted sources
- ET CINS — Active threat intelligence matches  
- ET SCAN — Network reconnaissance (Zmap, Masscan)
- ET EXPLOIT — Exploit attempts including Mozi botnet (24 June 2026)
- ET MALWARE — Malware traffic and C2 communication

## Custom Elevation Rules
See wazuh/rules/suricata_custom.xml for rule IDs 100300-100304.

## AUP Permission
Written permission obtained from Vultr TOS Team (September 2026) confirming
SSH honeypot and Suricata IDS deployment is permitted for educational
cybersecurity training purposes.
