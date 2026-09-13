# 07 — Intern Investigation Workflow

## Overview

The workflow from real attacker to intern investigation task is fully automated. No manual alert routing is required from the mentor for honeypot-triggered cases.

## Automated Pipeline

```
Step 1:  Real attacker hits Cowrie honeypot on port 22 or 23
         │
Step 2:  Cowrie captures the full session:
         credentials tried, commands run, files downloaded, duration
         │
Step 3:  Wazuh reads the Cowrie JSON log and fires custom detection rules
         │
Step 4:  Cowrie alert daemon creates a case in the LearnCyber Case
         Management System and sends a mentor notification email
         (within 30 seconds of session close)
         │
Step 5:  Wazuh-Convex integration sends enriched alert data to the
         academy management system intern dashboard
         │
Step 6:  Mentor reviews the alert and assigns it to the appropriate
         intern as a weekly investigation task
         │
Step 7:  Intern logs into the management system, sees the assigned task
         with alert details and OSINT starting points
         │
Step 8:  Intern logs into Wazuh via SSO (single click from dashboard)
         and investigates the raw SIEM data
         │
Step 9:  Intern completes the investigation: IP analysis, OSINT findings,
         MITRE ATT&CK mapping, verdict, screenshots, executive summary
         │
Step 10: Intern submits report via the case management system
         │
Step 11: Mentor grades the submission against the rubric and writes
         professional written feedback
         │
Step 12: Investigation report added to intern portfolio
```

## Daily Monitoring Routine

In addition to weekly structured tasks, SOC interns complete a daily alert monitoring check-in. This builds the daily habit of a real SOC analyst.

**Time required:** 15–30 minutes per day

**Daily check-in covers:**
- Total alerts reviewed
- Highest severity seen
- Cowrie honeypot activity
- Most interesting observation of the day
- Confidence rating
- Any escalations

Mentors review daily check-ins weekly. Consistent identical entries are flagged — an analyst who is genuinely monitoring sees something different every day.

## Escalation Format

From Week 3 onwards, every confirmed true positive requires a formal L1-to-L2 escalation handoff in the case management system.

Required escalation fields:
- Full timeline of events
- Source IP and complete OSINT findings
- MITRE ATT&CK tactic, technique, and sub-technique
- Verdict with specific evidence
- Recommended next action for the Tier 2 analyst
- Containment recommendation

## Access Control

Interns access Wazuh via SSO from the management system dashboard — one click, no separate credentials. The `intern` backend_role maps to `readonly` and `agents_readonly` Wazuh API roles — they can investigate all alerts and agents but cannot modify rules, configurations, or security settings.

## Programme Structure

The SOC Analyst track runs for 12 weeks with daily monitoring throughout. After completing the 12-week programme, interns remain on the platform — continuing to investigate alerts, build their portfolio, and receive career support — until they secure their first cybersecurity role.

LearnCyber Ltd provides an official UK employment reference upon programme completion.
