# 🔍 DNS & Subdomain Enumeration Tool

A simple, user-friendly GUI application built using **Python** and **Kivy** to perform DNS Enumeration and Subdomain Discovery.

---

## 🚀 Features

* 🌐 DNS Enumeration (A, AAAA, MX, TXT, CNAME, SOA records)
* 🧭 Subdomain Discovery using a wordlist file
* 🖥️ Intuitive GUI with soft green background
* 📂 File chooser to select your subdomain wordlist
* 💾 Saves discovered subdomains to a text file

---

## 🖼️ Screenshots

<img width="795" alt="image" src="https://github.com/user-attachments/assets/02607e2f-255e-487d-ab08-d637235c2a47" />




---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aniket-cs/GreenTunnel.git
cd dns-subdomain-gui
```

### 2. Install Dependencies

```bash
pip install kivy requests dnspython
```

### 3. Run the App

```bash
python your_script_name.py
```

---

## 🏗️ Build Executable

### For Windows

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### For macOS

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

\*For full build instructions, see \*[*Build Instructions*](./Build%20Instructions.md)

---

## 📄 Usage

1. Enter a domain (e.g., `youtube.com`)
2. Click **Choose File** to load your subdomain wordlist file
3. Click **Run DNS Enumeration** or **Run Subdomain Enumeration**
4. Discovered subdomains will be saved in `discovered_subdomains.txt`

---

## 📁 Sample Subdomain Wordlist

```txt
www
mail
FTP
localhost
webmail
smtp
pop
nsl
blog
API
music
webdisk
ns2
cpanel
imap
test
ns
blog
pop3
dev
www2
admin
news
VPN
ns3
pcm
pct
cyan
village
aire
bubbles
career
info
```

Save it as `subdomains.txt` and select it in the app.

---

## 🙌 Contributing

Feel free to submit pull requests or report issues to improve this tool.

---

## 📜 License

Open Source

---

Made with ❤️ by 
