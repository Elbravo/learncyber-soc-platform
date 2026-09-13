# 09 — Lessons Learned

## What Worked Well

**Oracle Always Free Tier is genuinely capable**
The concern going into this was whether Always Free resources would be sufficient for a production SIEM. 4 vCPU ARM Ampere with 24GB RAM handles Wazuh manager, indexer, dashboard, Cowrie, Suricata, and Nginx simultaneously with headroom. Monthly cost: £0.

**Real data is infinitely better than simulated data**
The original plan included scenario injection scripts — fabricated JSON alerts designed to give interns varied investigations. After testing, this was abandoned. The authenticity problem was fatal: interns doing OSINT on a fabricated IP would find real data unconnected to a fake event. The live honeypot generates genuinely diverse attack patterns without any fabrication needed.

**Suricata transforms alert diversity immediately**
Within one hour of Suricata going live the alert landscape changed completely — from exclusively SSH brute force to network reconnaissance, botnet activity, exploit attempts, and threat intelligence matches. The Mozi botnet alert fired on day 6.

**SSO with single-click Wazuh access genuinely works**
The SSO integration means interns never need to manage Wazuh credentials. One click from the management system dashboard and they are authenticated with the correct permissions. This removes a significant barrier to daily monitoring habit formation.

## What Was Harder Than Expected

**Wazuh dual-layer security is not well documented**
The issue where SSO users could see dashboards but not agents took significant time to diagnose. The root cause — OpenSearch indexer roles and Wazuh API roles being completely separate security systems requiring independent configuration — is not clearly explained anywhere in Wazuh's official documentation. The diagnostic approach (watching the API log in real time during SSO login to see the actual JWT payload) was arrived at through trial and error.

**Suricata JSON decoder field limit**
Suricata's eve.json contains more fields than Wazuh's default JSON decoder maximum. This caused custom rule field matching to silently fail — the rules loaded without errors but never matched because the relevant fields were not being extracted. The fix (`analysisd.decoder_json_max_fields=200`) is buried in internal options documentation.

**Alert fatigue appears faster than expected**
Within 24 hours of Suricata deployment the case management system queue was overwhelmed with identical ET DROP and ET CINS alerts. Frequency suppression (5 triggers per hour threshold) and minimum alert level (Level 7) resolved this, but the problem appeared faster and more severely than anticipated.

**Cowrie Telnet on port 23**
The assumption that port 23 was unused and could be removed from the OCI security list was incorrect. An iptables redirect rule sends external port 23 traffic to Cowrie on port 2225. Removing the security list rule would have silently killed Telnet honeypot capture without any error. Always verify with `iptables -t nat -L -n` before modifying firewall rules.

## What Would Be Done Differently

**Document from day one**
The platform was built over several months before documentation was started. Reconstructing configuration decisions and the reasoning behind them retrospectively is significantly harder than documenting at the time. For any future infrastructure project: document every decision as it is made, including what was tried and rejected.

**Set up index retention from the start**
Wazuh indices grow continuously. Without a retention policy, storage consumption compounds over time. Setting a 90-day retention policy from deployment day would have prevented unnecessary storage accumulation.

**Start Suricata in alerts-only mode from the beginning**
The default Suricata configuration logs all network events — alerts, DNS, HTTP, TLS, SSH, flow records. This generates enormous log volume. Alerts-only mode should be the default for a training environment where only threat detections matter.

**Use Gmail plus-addressing for all AWS sub-accounts from the start**
The initial AWS Organizations sub-account was created with a non-existent email address, making it impossible to access the account's root user. Using `email+cloudlab001@gmail.com` from the beginning avoids this completely.

## Key Decisions That Proved Correct

**Rolling individual intake over cohort model**
Each intern starts when they are ready rather than waiting for a cohort date. The platform's architecture supports this — every intern has their own investigation queue and progresses at their own pace. This turned out to be a significant commercial advantage as well as a technical one.

**Wazuh over Splunk**
Splunk's free tier is too limited for a production environment with real traffic volumes. Wazuh is fully open source, has native honeypot and IDS integration, and runs comfortably on Always Free resources.

**Building case management natively rather than using TheHive**
TheHive is powerful but adds licensing complexity and another platform for interns to navigate. The native LearnCyber Case Management System built by Raymond Asogwa integrates directly with the management system, SSO, and Wazuh — reducing complexity and eliminating licensing costs.

**Keeping Cloud Security track as AWS-only**
The original plan included Azure in the Cloud Security track. This was dropped in favour of deep AWS-only coverage. Trying to cover both in 12 weeks would have produced surface-level knowledge of both platforms. Deep competence in one is more valuable to employers than shallow familiarity with two.
