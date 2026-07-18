# 🛡️ Cyber Security Encryption Suite Pro

An ultra-modern, interactive **Desktop Cryptographic Application** built in Python with **CustomTkinter**. Features real-time cipher stream animations, Shannon entropy analytics, base converters, and symmetric & asymmetric cryptographic algorithms.

---

## 🌟 Key Features

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

## ⚙️ Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yousafSamy1/Data-Security.git
   cd Data-Security
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python security_gui.py
   ```
