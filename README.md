# 🔐 HTTP Credential Sniffer

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![License](https://img.shields.io/badge/License-Educational%20Only-red)

Educational project demonstrating how **HTTP credentials can be intercepted** using Wireshark and a Flask login server.

> ⚠️ **Educational Use Only** - Never test on unauthorized networks

---

## 🎯 **What It Does**

- Creates a **Flask login server** with HTTP (no encryption)
- **Captures network traffic** using Wireshark 
- **Extracts plaintext credentials** from HTTP POST requests
- Demonstrates why **HTTPS is essential** for secure communication

---

## 🛠️ **Setup**

```bash
# Install dependencies
pip install flask

# Run the server
python app.py

# Start Wireshark and filter: http.request.method == "POST"
```

---

## 🚀 **Usage**

1. **Start Flask server** on Kali Linux
2. **Open Wireshark** and begin packet capture
3. **Submit login form** from another machine via browser
4. **View captured credentials** in Wireshark HTTP POST data

---

## 📁 **Project Structure**

```
├── app.py              # Flask server
├── templates/
│   └── login.html      # Login form
└── requirements.txt    # Dependencies
```

---

## 🔍 **Example Output**

**Wireshark captures this plaintext data:**
```http
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=admin&password=secret123
```

---

## ⚖️ **Legal Notice**

**Educational purposes only.** Always get permission before network testing. Use responsibly and ethically.

---

**⭐ Star if this helped you understand HTTP security vulnerabilities!**
