# 🛡️ Cyber Security Encryption Suite Pro

An ultra-modern, interactive **Security Suite** available both as a **Vercel Serverless Web Application** (FastAPI backend + Modern Cyberpunk Web UI) and as a **Desktop Application** (CustomTkinter GUI).

---

## 🌟 Key Features

* 🌐 **Vercel Serverless Ready**: Native FastAPI serverless entrypoint (`api/index.py`) and Web Client (`public/index.html`).
* 🎨 **Obsidian Dark Cyberpunk Interface**: Sleek dark mode design with glowing cyan & purple accents.
* ⚡ **Live Matrix Stream Animations**: Cyberpunk letter-scramble animations during encryption and decryption.
* 📊 **Shannon Entropy Analytics**: Live bits/symbol entropy calculation and character length counter.
* 📜 **Activity Feed & Logs**: Real-time timestamped cryptographic activity log.
* 🔄 **Format Conversion Options**: View outputs as Plaintext, Hexadecimal (`HEX`), or Base64.
* 📋 **Utility Controls**: One-click copy with toast notifications, clear, and input/output swapping.

---

## 🔐 Supported Algorithms

1. **Caesar Cipher** (*Classical Symmetric*)
   - Variable shift key amount ($0 - 25$).
2. **Columnar Transposition Cipher** (*Matrix Permutation*)
   - Key word based matrix column ordering.
3. **Affine Cipher** (*Modular Algebraic*)
   - Linear modular transformation: $E(x) = (a \cdot x + b) \pmod{26}$.
4. **RSA Cryptography** (*Asymmetric Public-Key*)
   - Modular exponentiation public/private key generation ($p, q, e$) with built-in sample key generator.

---

## 🚀 Deployment on Vercel

This repository is configured out-of-the-box for **Vercel Python Serverless Deployment**:

- **Python Entrypoint**: `api/index.py` configured via `pyproject.toml` (`tool.vercel.entrypoint = "api.index:app"`).
- **Web Frontend**: `public/index.html` routed seamlessly via `vercel.json`.

Simply import this GitHub repository (`yousafSamy1/Data-Security`) into [Vercel](https://vercel.com/new) and click **Deploy**!

---

## ⚙️ Local Development & Desktop App

### Option 1: Run Web Engine locally
```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

### Option 2: Run CustomTkinter Desktop GUI
```bash
python security_gui.py
```

### Option 3: Build Standalone Windows Executable (.exe)
```bash
pyinstaller CyberSecuritySuite.spec
```
The compiled executable will be generated in `dist/CyberSecuritySuite.exe`.
