# LearnCyber Academy — Production SOC Platform

> A production-grade Security Operations Centre deployed on Oracle Cloud Infrastructure from scratch, running 24 hours a day, capturing real attacker sessions from the internet and routing them to cybersecurity interns as live investigation tasks.

[![Platform Status](https://img.shields.io/badge/Status-Live-brightgreen)](https://lcacademy.uk)
[![Infrastructure](https://img.shields.io/badge/Cloud-Oracle%20Always%20Free-orange)](https://cloud.oracle.com)
[![SIEM](https://img.shields.io/badge/SIEM-Wazuh%204.14.5-blue)](https://wazuh.com)
[![IDS](https://img.shields.io/badge/IDS-Suricata%208.0.5-red)](https://suricata.io)
[![Monthly Cost](https://img.shields.io/badge/Monthly%20Cost-%C2%A30-success)](https://cloud.oracle.com/compute/free-tier)

---

## What This Is

Most cybersecurity training platforms use simulated environments. This one does not.

The LearnCyber Academy SOC Platform is a fully operational Security Operations Centre. It captures genuine attacker sessions from the internet every day, processes them through a live SIEM with 100+ custom detection rules, routes confirmed incidents to a custom case management system, and assigns them to SOC Analyst interns as real investigation tasks.

Every alert is real. Every attacker session is genuine. Every investigation report produced by an intern is based on actual threat actor activity — not a simulation, not a pre-built scenario.

---

## Architecture Overview

```
Internet Attackers (China, Russia, Netherlands, USA and more)
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│                Oracle Cloud Infrastructure — UK South (London)    │
│                    4 vCPU ARM Ampere | 24GB RAM | Always Free     │
│                                                                    │
│  Port 22/23 → Cowrie Honeypot    Port 80/443 → Nginx (Wazuh)     │
│  Port 2222  → Real SSH           Port 1514-1515 → Wazuh Agents   │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │    Cowrie    │  │   Suricata   │  │   staff-laptop          │ │
│  │  Honeypot   │  │  IDS 8.0.5  │  │   Windows 11 Pro        │ │
│  │  SSH+Telnet  │  │  40,000+    │  │   Wazuh Agent 001       │ │
│  │  Port 22/23  │  │  ET Rules   │  │   Real Endpoint Data    │ │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬─────────────┘ │
│         └─────────────────┴──────────────────────┘               │
│                            │                                       │
│                            ▼                                       │
│                   ┌─────────────────┐                              │
│                   │   Wazuh SIEM    │                              │
│                   │   v4.14.5       │                              │
│                   │   100+ Custom   │                              │
│                   │   Rules         │                              │
│                   │   MITRE ATT&CK  │                              │
│                   │   Mapped        │                              │
│                   └────────┬────────┘                              │
│                            │                                       │
│               ┌────────────┴────────────┐                          │
│               ▼                         ▼                          │
│  ┌─────────────────────┐  ┌─────────────────────────────────────┐ │
│  │  LearnCyber Case    │  │  Academy Management System          │ │
│  │  Management System  │  │  SSO + RBAC + Intern Dashboard      │ │
│  │  (Custom Built by   │  │  Rolling individual intake          │ │
│  │   Raymond Asogwa)   │  │  SOC / GRC / Cloud Security tracks  │ │
│  └─────────────────────┘  └─────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
learncyber-soc-platform/
│
├── README.md                          ← You are here
│
├── docs/
│   ├── 01-infrastructure.md           ← Oracle Cloud setup, networking
│   ├── 02-wazuh-siem.md               ← Wazuh installation and config
│   ├── 03-cowrie-honeypot.md          ← Cowrie setup and integration
│   ├── 04-suricata-ids.md             ← Suricata deployment and rules
│   ├── 05-endpoint-monitoring.md      ← Windows 11 agent enrollment
│   ├── 06-sso-rbac.md                 ← SSO and RBAC implementation
│   ├── 07-intern-workflow.md          ← Alert to investigation pipeline
│   ├── 08-alert-investigations.md     ← Real documented investigations
│   └── 09-lessons-learned.md         ← Key decisions and challenges
│
├── wazuh/
│   └── rules/
│       ├── learncyber_soc_rules.xml   ← Custom honeypot detection rules
│       └── suricata_custom.xml        ← Suricata elevation rules
│
├── suricata/
│   └── setup-notes.md                ← Suricata configuration notes
│
└── scripts/
    └── cloudflare_poll.py             ← Cloudflare → Wazuh event poller
```

---

## Live Metrics

| Metric | Value |
|--------|-------|
| Total Wazuh alerts (30 days) | 23,446+ |
| Cowrie honeypot logins | 5,639 real attacker sessions |
| Authentication failures | 3,439 |
| Suricata alerts (first 24 hours) | 100+ |
| Custom detection rules | 100+ |
| MITRE ATT&CK techniques covered | 20+ |
| Compliance frameworks active | 5 |
| CIS Benchmark checks (Windows 11) | 473 |
| Monthly infrastructure cost | £0 |

---

## Key Technical Achievements

- **Zero-cost production infrastructure** — full SOC stack on Oracle Always Free Tier
- **Automated alert-to-investigation pipeline** — attacker session to intern task in under 30 seconds, zero manual intervention
- **Wazuh SSO dual-layer RBAC** — solved a complex issue where OpenSearch indexer roles and Wazuh API roles are completely separate security systems
- **Real endpoint telemetry** — Windows 11 device generating live CIS Benchmark, PCI DSS, and MITRE ATT&CK data
- **Network IDS at scale** — Suricata 8.0.5 with 40,000+ Emerging Threats signatures, auto-updated weekly
- **Alert fatigue management** — frequency suppression on noisy rules, minimum alert level threshold, alert-only logging

---

## What This Powers

This infrastructure is the foundation of **LearnCyber Academy** — a UK cybersecurity work experience platform where SOC Analyst, GRC Analyst, and Cloud Security interns investigate real incidents and graduate with a portfolio of genuine professional investigation reports.

**www.lcacademy.uk**

---

## Author

**Daniel Oseghale**
Security Operations Lead | SOC Platform Architect
LearnCyber Academy | LearnCyber Ltd — Swansea, Wales, UK

---

*Built entirely from scratch. No templates. No pre-built labs. Real infrastructure for real investigations.*
