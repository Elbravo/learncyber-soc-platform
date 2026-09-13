# 05 — Endpoint Monitoring

## Agent Details

| Field | Value |
|-------|-------|
| Agent name | staff-laptop |
| Agent ID | 001 |
| OS | Microsoft Windows 11 Pro 10.0.26200.8655 |
| CPU | Intel Core i5-8265U @ 1.60GHz |
| RAM | 7.9 GB |
| Wazuh version | v4.14.5 |
| Registration date | 11 June 2026 |
| Status | Active |

## Why a Real Endpoint Matters

Most SOC training platforms use log files generated from scripted scenarios. The staff-laptop generates genuine Windows telemetry from a real device used by real people every day. Every process creation, every network connection, every authentication event, every file change — all real.

This means intern investigations are based on actual endpoint behaviour, not fabricated events.

## Data Generated

### CIS Microsoft Windows 11 Enterprise Benchmark v3.0.0

Wazuh runs all 473 CIS benchmark checks against the endpoint automatically.

| Result | Count |
|--------|-------|
| Passed | 122 |
| Failed | 351 |
| Not applicable | 9 |
| Overall score | 25% |

A 25% score is normal for a personal device. Enterprise IT teams target 80%+. The 351 failures represent real configuration gaps that interns assess, prioritise, and report on — using the same methodology a security analyst uses when onboarding a new device.

### PCI DSS Compliance

Control 2.2 (System Configuration Standards) shows 484 findings from real device activity. Interns categorise these, identify the highest-risk findings, and produce a compliance report.

### MITRE ATT&CK Detections

**Defense Evasion** detected within the first hour of enrollment. Something running on the device triggered a detection consistent with techniques used to hide activity or bypass security controls. Interns investigate whether this is a true positive (malicious), false positive (legitimate software behaving similarly), or suspicious but unexplained.

## Enrollment Process

The Wazuh dashboard provides a deployment wizard that generates the exact installation command:

```
Wazuh Dashboard → ☰ Menu → Endpoints → Deploy new agent
→ Select: Windows MSI 32/64 bits
→ Server address: 132.145.68.116
→ Agent name: staff-laptop
→ Copy generated PowerShell command
```

On the Windows laptop (PowerShell as Administrator):
```powershell
# Paste generated command here
NET START WazuhSvc
Set-Service -Name WazuhSvc -StartupType Automatic
```

## Intern Investigation Tasks

Three structured tasks use this endpoint data:

| Task | Week | Focus |
|------|------|-------|
| CIS Benchmark Assessment | Week 1 | Pick the 5 highest-risk failures from 351. Justify choices. Write verdict on overall security posture. |
| PCI DSS 2.2 Analysis | Week 10 | Categorise 484 findings. Assess audit pass/fail. Write plain-English remediation report. |
| Defense Evasion Investigation | Week 2 | Investigate the MITRE detection. Identify the rule, the technique, the process. True positive or false positive? |
