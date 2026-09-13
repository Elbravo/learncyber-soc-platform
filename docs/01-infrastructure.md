# 01 — Infrastructure

## Cloud Provider

Oracle Cloud Infrastructure (OCI) — UK South region (London).

The entire platform runs on Oracle's Always Free Tier — a permanent free tier that includes resources sufficient to run a production SOC environment at no cost.

## Server Specification

| Component | Specification |
|-----------|--------------|
| Instance type | VM.Standard.A1.Flex (ARM Ampere) |
| vCPUs | 4 |
| RAM | 24 GB |
| Storage | 50 GB boot volume |
| Network | 1 Gbps |
| OS | Ubuntu 22.04 LTS |
| Monthly cost | £0 (Always Free Tier) |
| Region | UK South — London |

## Network Security List (Firewall)

| Port | Protocol | Source | Purpose |
|------|----------|--------|---------|
| 22 | TCP | 0.0.0.0/0 | Cowrie honeypot (redirected from real SSH) |
| 23 | TCP | 0.0.0.0/0 | Cowrie Telnet honeypot |
| 80 | TCP | 0.0.0.0/0 | Nginx HTTP (redirects to HTTPS) |
| 443 | TCP | 0.0.0.0/0 | Nginx HTTPS — Wazuh dashboard |
| 2222 | TCP | Restricted | Real SSH access (admin only) |
| 1514-1515 | TCP | Restricted | Wazuh agent communication |

## Port Redirect Configuration

Real SSH runs on port 2222. Cowrie honeypot intercepts connections on the standard ports:

```bash
# SSH redirect: external port 22 → Cowrie on port 2222
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222

# Telnet redirect: external port 23 → Cowrie on port 2225
sudo iptables -t nat -A PREROUTING -p tcp --dport 23 -j REDIRECT --to-port 2225

# Persist across reboots
sudo netfilter-persistent save
```

## Nginx Reverse Proxy

Nginx serves as the reverse proxy for the Wazuh dashboard, handling SSL termination via Let's Encrypt.

- Wazuh dashboard: `https://wazuh.lcacademy.uk`
- SSL: Let's Encrypt (auto-renewing)
- Port 80 → 443 redirect for all traffic

## Key Design Decision

Running the entire stack on Oracle Always Free Tier was a deliberate choice. The goal was to prove that a production-grade SOC environment does not require expensive infrastructure. This has a direct impact on the training programme — the cost of running the platform is zero, which means the programme fee covers mentorship and curriculum, not server costs.
