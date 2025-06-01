# 🔍 HTTP Credential Sniffer

A simple project that demonstrates how HTTP credentials can be captured from network traffic using tools like Wireshark.

> ⚠️ This project is for **educational and ethical testing purposes only**. Do **NOT** use it on networks you do not own or have explicit permission to test.

---

## 📸 Demo Screenshots

![Credential Sniffing](./screenshots/credential-captured.png)
*Captured POST request showing username and password sent in plaintext over HTTP.*

---

## 📂 Project Structure

| Path             | Description                               |
|------------------|-------------------------------------------|
| `src/`           | Python script for sniffing (if any)       |
| `server/`        | Flask test server to simulate login POST  |
| `captures/`      | Example `.pcapng` file of captured traffic|
| `screenshots/`   | Screenshots showing setup and output      |

---

## ⚙️ How It Works

1. A **Flask server** is hosted on Kali Linux to accept HTTP POST login requests.
2. Wireshark captures the traffic on `eth0`.
3. A victim device (browser) sends credentials using HTTP (not HTTPS).
4. The POST data, including `username` and `password`, is visible in plaintext in the capture.
5. The capture is filtered using:
   ```wireshark
   **http.request.method == "POST"**
6. Credentials are shown under:
     ** HTML Form URL Encoded: application/x-www-form-urlencoded**
