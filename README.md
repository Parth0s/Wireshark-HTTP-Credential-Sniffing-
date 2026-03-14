# HTTP Plaintext Credential Exposure Lab

> Demonstrating how unencrypted HTTP authentication exposes credentials to network interception — and how defenders can detect it.

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Type](https://img.shields.io/badge/Type-Blue%20Team%20Lab-blue)
![OWASP](https://img.shields.io/badge/OWASP-A02%3A2021%20Cryptographic%20Failures-red)

---

## Objective

This lab simulates a real-world scenario where a web application transmits login credentials over unencrypted HTTP. Using a controlled lab environment, I captured live network traffic with Wireshark to demonstrate how an attacker positioned on the same network can intercept plaintext credentials — and document what a SOC analyst should look for to detect this behavior.

**Real-world relevance:** Plaintext credential transmission remains one of the most common vulnerabilities in internal corporate applications, legacy portals, and misconfigured services. OWASP classifies this under [A02:2021 – Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/).

---

## Lab Environment

| Component        | Details                                      |
|------------------|----------------------------------------------|
| Attacker Machine | Kali Linux 2024.1 (VirtualBox VM)            |
| Victim Machine   | Windows 10 (VirtualBox VM)                   |
| Network Type     | Host-Only Adapter (fully isolated lab)       |
| Web Server       | Python Flask 2.0 — HTTP only, port 5000      |
| Capture Tool     | Wireshark 4.x                                |
| Python Version   | 3.8+                                         |

> All testing was performed on an isolated local network. No external systems were involved.

---

## Attack Simulation — What I Did

### Step 1 — Built the vulnerable login server

A simple Flask web application was created to simulate a corporate login portal running over HTTP (no TLS). This represents a real-world scenario of an internal tool or legacy application that was never migrated to HTTPS.

```bash
pip install flask
python app.py
# Server starts at http://0.0.0.0:5000
```

### Step 2 — Set up Wireshark for capture

Wireshark was launched on the attacker machine in **promiscuous mode** to capture all traffic on the network interface — not just traffic addressed to the attacker machine.

**Capture filter used:**
```
http.request.method == "POST"
```

This filter isolates form submission traffic, which is where credentials travel.

### Step 3 — Submitted credentials from victim machine

From the Windows 10 VM, a user navigated to `http://[kali-ip]:5000` and submitted a username and password through the login form.

### Step 4 — Intercepted the traffic

Wireshark captured the HTTP POST request in real time before the server processed it.

---

## Findings — What the Capture Revealed

### Raw HTTP POST request intercepted:

```http
POST /login HTTP/1.1
Host: 192.168.56.101:5000
Content-Type: application/x-www-form-urlencoded
Content-Length: 34

username=john.doe&password=Corp@2024
```

### Key observations:

- **No TLS handshake present** — traffic flows in cleartext with zero encryption
- **Credentials visible in packet body** — username and password readable without any decryption
- **Full HTTP stream reconstructable** — Wireshark's "Follow TCP Stream" feature reveals the entire session including server response
- **Source and destination IPs exposed** — attacker can map which user authenticated to which server

### Wireshark HTTP stream view:

```
POST /login HTTP/1.1
Host: 192.168.56.101:5000
username=john.doe&password=Corp@2024

HTTP/1.1 200 OK
Content-Type: text/html
Welcome, john.doe!
```

---

## Blue Team Perspective — How a SOC Analyst Detects This

This section is what matters most. Demonstrating the attack is only half the work — understanding detection and response is what separates a security analyst from a script runner.

### Detection methods:

| Detection Layer | Rule / Indicator |
|-----------------|-----------------|
| Network IDS (Snort/Suricata) | Alert on HTTP POST requests to `/login` endpoints without preceding TLS handshake |
| SIEM Correlation | Flag authentication attempts over port 80 from internal hosts — these should never occur in a hardened environment |
| Packet Inspection | Identify `application/x-www-form-urlencoded` content type on unencrypted connections |
| Behavioral Rule | Multiple POST requests to same endpoint from same source IP within 60 seconds = potential credential stuffing over HTTP |

### Indicators of Compromise (IOCs):

- HTTP traffic on port 80/8080 containing `username=` or `password=` parameters
- Authentication endpoints accessible without HTTPS redirect
- Absence of `Strict-Transport-Security` header in server responses
- Clear-text `Authorization` headers in captured traffic

### Incident Response — What I would do as an analyst:

1. **Identify** — Flag the unencrypted authentication endpoint via SIEM alert or network scan
2. **Contain** — Block port 80 access to the login endpoint at the firewall level immediately
3. **Investigate** — Review proxy/firewall logs for how long this endpoint was exposed and who accessed it
4. **Remediate** — Force HTTPS via 301 redirect, implement HSTS header, obtain and install TLS certificate
5. **Document** — Log the finding, affected users, exposure window, and fix applied

---

## Mitigation

| Vulnerability | Fix |
|---------------|-----|
| Plaintext credential transmission | Enforce HTTPS — redirect all HTTP to HTTPS with 301 |
| Missing HSTS header | Add `Strict-Transport-Security: max-age=31536000` to server response headers |
| No certificate | Obtain TLS certificate via Let's Encrypt (free) or internal CA |
| Credential exposure in transit | Implement end-to-end encryption — TLS 1.2 minimum, TLS 1.3 preferred |

---

## Key Takeaways

1. **HTTP is never safe for authentication** — any credential submitted over HTTP can be intercepted by anyone on the same network segment, including coffee shop Wi-Fi, corporate LAN, or a compromised router
2. **Detection requires proactive monitoring** — this attack leaves no trace on the victim machine; it is only visible at the network layer, making SIEM and IDS rules critical
3. **HTTPS alone is not enough** — HSTS, certificate pinning, and proper redirect configuration are all required to fully close this attack surface

---

## Project Structure

```
HTTP-Plaintext-Credential-Exposure-Lab/
├── app.py                  # Vulnerable Flask login server
├── templates/
│   └── login.html          # Login form (HTTP, no encryption)
├── captures/
│   └── http_capture.pcapng # Wireshark capture file
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## References

- [OWASP A02:2021 — Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [Wireshark HTTP Protocol Dissector Documentation](https://www.wireshark.org/docs/dfref/h/http.html)
- [Mozilla — HTTP Strict Transport Security (HSTS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [Let's Encrypt — Free TLS Certificates](https://letsencrypt.org/)

---

## Legal Notice

This project was conducted entirely within an isolated virtual lab environment for educational purposes. No unauthorized networks or systems were accessed. Always obtain explicit written permission before performing any security testing on systems you do not own.

---

*Part of my cybersecurity portfolio — documenting hands-on lab work in network security and SOC analysis.*
