# 06 — SSO and RBAC

## Overview

All users authenticate through the LearnCyber Academy management system via SSO. When a user clicks the Wazuh link in the management system, they are authenticated automatically with the correct permissions — no separate Wazuh login required.

## The Dual-Layer Problem

This was the most complex technical challenge in the entire project.

Wazuh has two completely separate security systems:

1. **OpenSearch indexer security** — controls dashboard access (what pages you can see)
2. **Wazuh API security** — controls data access (what agents and rules you can query)

Both must be configured independently. A user can have full dashboard access but still see "No agents were added to the manager" because the API layer has not been configured.

This is not documented clearly anywhere in Wazuh's official documentation.

## Root Cause Diagnosis

The SSO authentication flow uses `run_as` — the management system sends a JWT token to Wazuh which extracts the `backend_roles` claim and maps it to internal Wazuh API roles.

Diagnosis was done by watching the Wazuh API log in real time while an SSO user logged in:

```bash
sudo tail -f /var/ossec/logs/api.log | grep "run_as"
```

This revealed the actual JWT payload including the `backend_roles` value for each user type:

```json
{
  "user_name": "js75xp552xj58q9mebf6tdyjqx85cjqk",
  "backend_roles": ["intern"],
  ...
}
```

## Role Architecture

| User type | Backend role | Wazuh API roles | Access |
|-----------|-------------|-----------------|--------|
| Admin | `admin` | administrator | Full access |
| Manager | `manager` | readonly + agents_readonly | Read all + view agents |
| Intern | `intern` | readonly + agents_readonly | Read all + view agents |

## RBAC Rules Configuration

Rules are created in the Wazuh API using `FIND` operator matching on `backend_roles`:

```bash
# Get API token
TOKEN=$(curl -s -k -u wazuh-wui:PASSWORD \
  -X POST "https://localhost:55000/security/user/authenticate?raw=true")

# Rule for interns
curl -s -k -X PUT "https://localhost:55000/security/rules/100" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sso-intern-readonly",
    "rule": { "FIND": { "backend_roles": "intern" } }
  }'

# Rule for admins
curl -s -k -X POST "https://localhost:55000/security/rules" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sso-admin-full",
    "rule": { "FIND": { "backend_roles": "admin" } }
  }'

# Rule for managers
curl -s -k -X POST "https://localhost:55000/security/rules" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sso-manager-readonly",
    "rule": { "FIND": { "backend_roles": "manager" } }
  }'

# Link manager rule to readonly and agents_readonly roles
curl -s -k -X POST \
  "https://localhost:55000/security/roles/2/rules?rule_ids=102" \
  -H "Authorization: Bearer $TOKEN"

curl -s -k -X POST \
  "https://localhost:55000/security/roles/4/rules?rule_ids=102" \
  -H "Authorization: Bearer $TOKEN"
```

## wazuh.yml Configuration

`/usr/share/wazuh-dashboard/data/wazuh/config/wazuh.yml`:

```yaml
hosts:
  - default:
      url: https://127.0.0.1
      port: 55000
      username: wazuh-wui
      password: "REDACTED"
      run_as: true
```

`run_as: true` is critical — without it the SSO token is not passed to the API and role mapping never occurs.

## Key Learning

When debugging SSO issues in Wazuh, always check both layers independently:

1. Can the user see the dashboard? → OpenSearch issue
2. Can the user see agents? → Wazuh API RBAC issue

They require completely different fixes.
