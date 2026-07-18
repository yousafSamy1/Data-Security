from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import string
import math
import base64
import os
from sympy import mod_inverse
from pycipher import ColTrans

app = FastAPI(title="Cyber Shield API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Cipher Core Functions
# ---------------------------

def caesar_encrypt(message: str, shift: int) -> str:
    result = ""
    for ch in message:
        if ch.islower():
            result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        elif ch.isupper():
            result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += ch
    return result

def caesar_decrypt(cipher: str, shift: int) -> str:
    return caesar_encrypt(cipher, -shift)

lower = string.ascii_lowercase
upper = string.ascii_uppercase

def affine_encrypt(message: str, a: int, b: int) -> str:
    out = ""
    for ch in message:
        if ch in lower:
            p = lower.index(ch)
            c = (a * p + b) % 26
            out += lower[c]
        elif ch in upper:
            p = upper.index(ch)
            c = (a * p + b) % 26
            out += upper[c]
        else:
            out += ch
    return out

def affine_decrypt(cipher: str, a: int, b: int) -> str:
    try:
        inv = mod_inverse(a, 26)
    except Exception:
        raise ValueError(f"Multiplier 'a' ({a}) has no modular inverse mod 26. Must be coprime to 26.")
    out = ""
    for ch in cipher:
        if ch in lower:
            c = lower.index(ch)
            p = (inv * (c - b)) % 26
            out += lower[p]
        elif ch in upper:
            c = upper.index(ch)
            p = (inv * (c - b)) % 26
            out += upper[p]
        else:
            out += ch
    return out

def encrypt_columnar(text: str, key: str) -> str:
    return ColTrans(key).encipher(text)

def decrypt_columnar(text: str, key: str) -> str:
    return ColTrans(text if not key else key).decipher(text)

def rsa_generate_keys(p: int, q: int, e: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    k = 1
    while True:
        val = phi * k + 1
        if val % e == 0:
            d = val // e
            break
        k += 1
    return (e, n), (d, n)

def rsa_encrypt(m: int, e: int, n: int) -> int:
    return pow(m, e, n)

def rsa_decrypt(c: int, d: int, n: int) -> int:
    return pow(c, d, n)

def calc_entropy(text: str) -> float:
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum([p * math.log2(p) for p in prob if p > 0])

# ---------------------------
# Request Models
# ---------------------------

class CaesarReq(BaseModel):
    text: str
    shift: int
    mode: str = "Encrypt"

class ColumnarReq(BaseModel):
    text: str
    key: str
    mode: str = "Encrypt"

class AffineReq(BaseModel):
    text: str
    a: int
    b: int
    mode: str = "Encrypt"

class RSAReq(BaseModel):
    text: str
    p: int = 61
    q: int = 53
    e: int = 17
    mode: str = "Encrypt"

# ---------------------------
# Root HTML Route for Web UI
# ---------------------------

@app.get("/", response_class=HTMLResponse)
def get_root():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, "public", "index.html"),
        os.path.join(base_dir, "index.html"),
        "public/index.html",
        "index.html"
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Cyber Shield Engine Serverless Online</h1>")

# ---------------------------
# API Endpoints (both /api/ and / routes for maximum flexibility)
# ---------------------------

@app.get("/api/health")
@app.get("/health")
def health():
    return {"status": "ok", "system": "Cyber Shield Engine v3.0"}

@app.post("/api/caesar")
@app.post("/caesar")
def process_caesar(req: CaesarReq):
    try:
        if req.mode == "Encrypt":
            res = caesar_encrypt(req.text, req.shift)
        else:
            res = caesar_decrypt(req.text, req.shift)
        return {"result": res, "entropy": round(calc_entropy(res), 2), "mode": req.mode}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/api/columnar")
@app.post("/columnar")
def process_columnar(req: ColumnarReq):
    try:
        if not req.key.strip():
            raise ValueError("Key word cannot be empty.")
        if req.mode == "Encrypt":
            res = encrypt_columnar(req.text, req.key.strip())
        else:
            res = decrypt_columnar(req.text, req.key.strip())
        return {"result": res, "entropy": round(calc_entropy(res), 2), "mode": req.mode}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/api/affine")
@app.post("/affine")
def process_affine(req: AffineReq):
    try:
        if req.mode == "Encrypt":
            res = affine_encrypt(req.text, req.a, req.b)
        else:
            res = affine_decrypt(req.text, req.a, req.b)
        return {"result": res, "entropy": round(calc_entropy(res), 2), "mode": req.mode}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/api/rsa")
@app.post("/rsa")
def process_rsa(req: RSAReq):
    try:
        (pub_e, n), (priv_d, n2) = rsa_generate_keys(req.p, req.q, req.e)

        if req.mode == "Encrypt":
            if not req.text.isdigit():
                raise ValueError("RSA input must be an integer number.")
            m = int(req.text)
            cipher_val = rsa_encrypt(m, pub_e, n)
            res_str = (
                f"---------------------------------------------------\n"
                f"  PUBLIC KEY : (e={pub_e}, n={n})\n"
                f"  PRIVATE KEY: (d={priv_d}, n={n2})\n"
                f"---------------------------------------------------\n"
                f"  ENCRYPTED RESULT: {cipher_val}"
            )
            return {
                "result": res_str,
                "raw_result": str(cipher_val),
                "public_key": [pub_e, n],
                "private_key": [priv_d, n2],
                "entropy": round(calc_entropy(str(cipher_val)), 2),
                "mode": req.mode
            }
        else:
            if not req.text.isdigit():
                raise ValueError("RSA cipher input must be an integer number.")
            c = int(req.text)
            dec_val = rsa_decrypt(c, priv_d, n2)
            res_str = (
                f"---------------------------------------------------\n"
                f"  PUBLIC KEY : (e={pub_e}, n={n})\n"
                f"  PRIVATE KEY: (d={priv_d}, n={n2})\n"
                f"---------------------------------------------------\n"
                f"  DECRYPTED RESULT: {dec_val}"
            )
            return {
                "result": res_str,
                "raw_result": str(dec_val),
                "public_key": [pub_e, n],
                "private_key": [priv_d, n2],
                "entropy": round(calc_entropy(str(dec_val)), 2),
                "mode": req.mode
            }
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
