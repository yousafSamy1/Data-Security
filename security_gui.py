import customtkinter as ctk
import tkinter as tk
import string
import random
import time
import math
import base64
from sympy import mod_inverse
from pycipher import ColTrans

# ---------------------------
# Cipher Logic Functions
# ---------------------------

def caesar_encrypt(message, shift):
    result = ""
    for ch in message:
        if ch.islower():
            result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        elif ch.isupper():
            result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += ch
    return result

def caesar_decrypt(cipher, shift):
    return caesar_encrypt(cipher, -shift)

lower = string.ascii_lowercase
upper = string.ascii_uppercase

def affine_encrypt(message, a, b):
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

def affine_decrypt(cipher, a, b):
    inv = mod_inverse(a, 26)
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

def encrypt_columnar(text, key):
    return ColTrans(key).encipher(text)

def decrypt_columnar(text, key):
    return ColTrans(key).decipher(text)

def rsa_generate_keys(p, q, e):
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

def rsa_encrypt(m, e, n):
    return pow(m, e, n)

def rsa_decrypt(c, d, n):
    return pow(c, d, n)

def calc_entropy(text):
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum([p * math.log2(p) for p in prob if p > 0])


# ---------------------------
# Animated CustomTkinter Suite
# ---------------------------

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AnimatedSecurityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CYBER SHIELD PRO - Next-Gen Cryptographic Suite")
        self.geometry("1180x760")
        self.minsize(1050, 700)

        # Premium Color Palette
        self.BG_DARK = "#0B0F19"         # Ultra Dark Midnight Slate
        self.SIDEBAR_BG = "#070A10"      # Deepest Charcoal
        self.CARD_BG = "#131C2E"         # Glass Card Surface
        self.CARD_BORDER = "#1E293B"     # Card Border
        self.ACCENT_CYAN = "#00F0FF"     # Neon Cyber Cyan
        self.ACCENT_PURPLE = "#A855F7"   # Glowing Violet
        self.SUCCESS_GREEN = "#10B981"  # Emerald Green
        self.TEXT_BRIGHT = "#F8FAFC"    # Crisp White

        self.configure(fg_color=self.BG_DARK)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.active_tab = "caesar"
        self.current_result = ""
        self.animation_running = False
        self.pulse_state = True
        self.history_log = []

        # Build Layout
        self._build_sidebar()
        self._build_main_area()
        self._select_tab("caesar")

        # Start background pulse animation for system status
        self._animate_pulse()

    # ---------------------------
    # UI Layout Construction
    # ---------------------------

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=270,
            corner_radius=0,
            fg_color=self.SIDEBAR_BG,
            border_color="#1E293B",
            border_width=1
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        # Header Logo Frame
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(25, 15))

        title_lbl = ctk.CTkLabel(
            logo_frame,
            text="⚡ CYBER SHIELD",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.ACCENT_CYAN
        )
        title_lbl.pack(anchor="w")

        sub_lbl = ctk.CTkLabel(
            logo_frame,
            text="Pro Encryption Engine v3.0",
            font=ctk.CTkFont(size=12),
            text_color="#64748B"
        )
        sub_lbl.pack(anchor="w", pady=(2, 0))

        divider = ctk.CTkFrame(self.sidebar, height=1, fg_color="#1E293B")
        divider.pack(fill="x", padx=15, pady=10)

        # Navigation Buttons
        self.nav_buttons = {}
        tabs = [
            ("caesar", "🔑  Caesar Cipher", "CLASSICAL"),
            ("columnar", "📊  Columnar Transposition", "TRANSPOSITION"),
            ("affine", "📐  Affine Cipher", "ALGEBRAIC"),
            ("rsa", "⚛️  RSA Cryptography", "ASYMMETRIC")
        ]

        for tab_id, text, badge in tabs:
            btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            btn_frame.pack(fill="x", padx=15, pady=4)

            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                anchor="w",
                height=42,
                corner_radius=8,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="transparent",
                text_color="#94A3B8",
                hover_color="#131C2E",
                command=lambda tid=tab_id: self._select_tab(tid)
            )
            btn.pack(fill="x")
            self.nav_buttons[tab_id] = btn

        # History / Activity Feed Section
        hist_lbl = ctk.CTkLabel(
            self.sidebar,
            text="ACTIVITY LOG",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#475569"
        )
        hist_lbl.pack(anchor="w", padx=20, pady=(20, 5))

        self.history_box = ctk.CTkTextbox(
            self.sidebar,
            height=140,
            fg_color="#0B0F19",
            text_color="#94A3B8",
            font=ctk.CTkFont(family="Consolas", size=10),
            corner_radius=8,
            border_width=1,
            border_color="#1E293B"
        )
        self.history_box.pack(fill="x", padx=15, pady=(0, 15))
        self._log_history("System Engine initialized.")

        # System Status Card with Pulsing LED Dot
        self.status_card = ctk.CTkFrame(
            self.sidebar,
            fg_color="#0F172A",
            corner_radius=10,
            border_color="#1E293B",
            border_width=1
        )
        self.status_card.pack(fill="x", padx=15, pady=15, side="bottom")

        st_hdr = ctk.CTkFrame(self.status_card, fg_color="transparent")
        st_hdr.pack(fill="x", padx=12, pady=(10, 2))

        self.pulse_dot = ctk.CTkLabel(
            st_hdr,
            text="●",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.SUCCESS_GREEN
        )
        self.pulse_dot.pack(side="left", padx=(0, 6))

        self.st_title = ctk.CTkLabel(
            st_hdr,
            text="CORE ENGINE ONLINE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.SUCCESS_GREEN
        )
        self.st_title.pack(side="left")

        st_desc = ctk.CTkLabel(
            self.status_card,
            text="Entropy & Vector Real-Time Monitoring",
            font=ctk.CTkFont(size=10),
            text_color="#64748B"
        )
        st_desc.pack(anchor="w", padx=12, pady=(0, 10))

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=25, pady=20)
        self.main_area.grid_rowconfigure(2, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # Top Title Bar & Mode Switcher
        header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        title_sub_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_sub_frame.pack(side="left")

        self.tab_title_lbl = ctk.CTkLabel(
            title_sub_frame,
            text="Caesar Cipher",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.TEXT_BRIGHT
        )
        self.tab_title_lbl.pack(anchor="w")

        self.tab_badge_lbl = ctk.CTkLabel(
            title_sub_frame,
            text="CLASSICAL SYMMETRIC CIPHER",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.ACCENT_PURPLE
        )
        self.tab_badge_lbl.pack(anchor="w")

        # Mode Selector (Segmented Button)
        self.mode_var = ctk.StringVar(value="🔒 Encrypt")
        self.mode_selector = ctk.CTkSegmentedButton(
            header_frame,
            values=["🔒 Encrypt", "🔓 Decrypt"],
            variable=self.mode_var,
            selected_color=self.ACCENT_CYAN,
            selected_hover_color="#0891B2",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=36,
            corner_radius=8
        )
        self.mode_selector.pack(side="right")

        # Parameter Card Container
        self.param_card = ctk.CTkFrame(
            self.main_area,
            fg_color=self.CARD_BG,
            border_color=self.CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        self.param_card.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        # Main Workspace Container
        workspace = ctk.CTkFrame(self.main_area, fg_color="transparent")
        workspace.grid(row=2, column=0, sticky="nsew")
        workspace.grid_rowconfigure(0, weight=1)
        workspace.grid_rowconfigure(1, weight=1)
        workspace.grid_columnconfigure(0, weight=1)

        # INPUT PANEL
        input_panel = ctk.CTkFrame(
            workspace,
            fg_color=self.CARD_BG,
            border_color=self.CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        input_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        input_panel.grid_rowconfigure(1, weight=1)
        input_panel.grid_columnconfigure(0, weight=1)

        in_hdr = ctk.CTkFrame(input_panel, fg_color="transparent")
        in_hdr.grid(row=0, column=0, sticky="ew", padx=15, pady=(8, 4))

        in_title = ctk.CTkLabel(
            in_hdr,
            text="INPUT PLAINTEXT / CIPHERTEXT",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94A3B8"
        )
        in_title.pack(side="left")

        self.char_count_lbl = ctk.CTkLabel(
            in_hdr,
            text="0 chars | Entropy: 0.00 bits",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        )
        self.char_count_lbl.pack(side="right")

        self.input_textbox = ctk.CTkTextbox(
            input_panel,
            fg_color="#080C14",
            text_color=self.TEXT_BRIGHT,
            font=ctk.CTkFont(family="Consolas", size=13),
            corner_radius=8,
            border_width=1,
            border_color="#1E293B"
        )
        self.input_textbox.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))
        self.input_textbox.bind("<KeyRelease>", self._update_stats)

        # ACTION BUTTONS BAR WITH ANIMATION PROGRESS
        action_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        action_bar.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        self.run_btn = ctk.CTkButton(
            action_bar,
            text="⚡ EXECUTE & STREAM CIPHER",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.ACCENT_CYAN,
            hover_color="#0891B2",
            text_color="#042F2E",
            height=42,
            corner_radius=8,
            command=self._execute_cipher_animated
        )
        self.run_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.swap_btn = ctk.CTkButton(
            action_bar,
            text="🔄 Swap Input/Result",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color="#E2E8F0",
            height=42,
            corner_radius=8,
            command=self._swap_input_output
        )
        self.swap_btn.pack(side="right", padx=(0, 10))

        self.clear_btn = ctk.CTkButton(
            action_bar,
            text="🗑️ Clear",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color="#E2E8F0",
            height=42,
            width=90,
            corner_radius=8,
            command=self._clear_fields
        )
        self.clear_btn.pack(side="right")

        # OUTPUT PANEL
        output_panel = ctk.CTkFrame(
            workspace,
            fg_color=self.CARD_BG,
            border_color=self.CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        output_panel.grid(row=1, column=0, sticky="nsew")
        output_panel.grid_rowconfigure(1, weight=1)
        output_panel.grid_columnconfigure(0, weight=1)

        out_hdr = ctk.CTkFrame(output_panel, fg_color="transparent")
        out_hdr.grid(row=0, column=0, sticky="ew", padx=15, pady=(8, 4))

        out_title = ctk.CTkLabel(
            out_hdr,
            text="OUTPUT CIPHER STREAM",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94A3B8"
        )
        out_title.pack(side="left")

        # Format View Selector (Plaintext, Hex, Base64)
        self.format_var = ctk.StringVar(value="Plain")
        fmt_menu = ctk.CTkOptionMenu(
            out_hdr,
            values=["Plain", "HEX", "Base64"],
            variable=self.format_var,
            width=90,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0B0F19",
            button_color="#1E293B",
            command=self._change_output_format
        )
        fmt_menu.pack(side="right", padx=(10, 0))

        self.copy_btn = ctk.CTkButton(
            out_hdr,
            text="📋 Copy Result",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0B0F19",
            hover_color="#1E293B",
            text_color=self.ACCENT_CYAN,
            height=26,
            width=100,
            border_width=1,
            border_color=self.ACCENT_CYAN,
            corner_radius=6,
            command=self._copy_output
        )
        self.copy_btn.pack(side="right")

        self.output_textbox = ctk.CTkTextbox(
            output_panel,
            fg_color="#050811",
            text_color="#00FFB3",
            font=ctk.CTkFont(family="Consolas", size=13),
            corner_radius=8,
            border_width=1,
            border_color="#1E293B"
        )
        self.output_textbox.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))

        # Progress / Status Bar
        self.status_bar = ctk.CTkLabel(
            self.main_area,
            text="Engine ready.",
            font=ctk.CTkFont(size=12),
            text_color="#64748B",
            anchor="w"
        )
        self.status_bar.grid(row=4, column=0, sticky="ew", pady=(6, 0))

    # ---------------------------
    # Animations & Dynamic FX
    # ---------------------------

    def _animate_pulse(self):
        """Pulsing animation for green LED status dot"""
        if self.pulse_state:
            self.pulse_dot.configure(text_color=self.SUCCESS_GREEN)
        else:
            self.pulse_dot.configure(text_color="#064E3B")
        self.pulse_state = not self.pulse_state
        self.after(800, self._animate_pulse)

    def _animate_cyber_scramble(self, final_text, step=0, total_steps=12, is_error=False):
        """Scrambles characters into futuristic matrix stream before resolving"""
        scramble_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if is_error:
            self._show_result(final_text, is_error=True)
            self.animation_running = False
            self.run_btn.configure(state="normal", text="⚡ EXECUTE & STREAM CIPHER")
            return

        if step < total_steps:
            # Generate scrambled frame
            scrambled = ""
            reveal_count = int((step / total_steps) * len(final_text))
            for i, ch in enumerate(final_text):
                if ch == "\n" or ch == " " or i < reveal_count:
                    scrambled += ch
                else:
                    scrambled += random.choice(scramble_chars)
            
            self._show_result(scrambled)
            self.after(35, lambda: self._animate_cyber_scramble(final_text, step + 1, total_steps, is_error))
        else:
            self._show_result(final_text)
            self.animation_running = False
            self.run_btn.configure(state="normal", text="⚡ EXECUTE & STREAM CIPHER")
            self._set_status("Cyber Stream resolve complete.")

    # ---------------------------
    # Tab Building & Forms
    # ---------------------------

    def _select_tab(self, tab_id):
        self.active_tab = tab_id

        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.configure(fg_color="#131C2E", text_color=self.ACCENT_CYAN)
            else:
                btn.configure(fg_color="transparent", text_color="#94A3B8")

        for widget in self.param_card.winfo_children():
            widget.destroy()

        if tab_id == "caesar":
            self.tab_title_lbl.configure(text="Caesar Cipher")
            self.tab_badge_lbl.configure(text="CLASSICAL SYMMETRIC CIPHER • SHIFT VECTOR")
            self._build_caesar_params()
        elif tab_id == "columnar":
            self.tab_title_lbl.configure(text="Columnar Transposition Cipher")
            self.tab_badge_lbl.configure(text="PERMUTATION TRANSPOSITION • KEY MATRIX")
            self._build_columnar_params()
        elif tab_id == "affine":
            self.tab_title_lbl.configure(text="Affine Cipher")
            self.tab_badge_lbl.configure(text="ALGEBRAIC MODULAR CIPHER • (a*x + b) mod 26")
            self._build_affine_params()
        elif tab_id == "rsa":
            self.tab_title_lbl.configure(text="RSA Cryptography")
            self.tab_badge_lbl.configure(text="ASYMMETRIC PUBLIC KEY CRYPTOSYSTEM")
            self._build_rsa_params()

        self._set_status(f"Active Algorithm: {self.tab_title_lbl.cget('text')}")

    def _build_caesar_params(self):
        frame = ctk.CTkFrame(self.param_card, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=10)

        lbl = ctk.CTkLabel(
            frame,
            text="Shift Key Value (0-25):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#E2E8F0"
        )
        lbl.pack(side="left", padx=(0, 10))

        self.caesar_shift_entry = ctk.CTkEntry(
            frame,
            width=100,
            placeholder_text="3",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#080C14",
            border_color="#1E293B"
        )
        self.caesar_shift_entry.pack(side="left")
        self.caesar_shift_entry.insert(0, "3")

    def _build_columnar_params(self):
        frame = ctk.CTkFrame(self.param_card, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=10)

        lbl = ctk.CTkLabel(
            frame,
            text="Matrix Column Key (Word):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#E2E8F0"
        )
        lbl.pack(side="left", padx=(0, 10))

        self.col_key_entry = ctk.CTkEntry(
            frame,
            width=200,
            placeholder_text="SECRET",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#080C14",
            border_color="#1E293B"
        )
        self.col_key_entry.pack(side="left")
        self.col_key_entry.insert(0, "SECRET")

    def _build_affine_params(self):
        frame = ctk.CTkFrame(self.param_card, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=10)

        lbl_a = ctk.CTkLabel(frame, text="Key A (Coprime to 26):", font=ctk.CTkFont(size=13, weight="bold"))
        lbl_a.pack(side="left", padx=(0, 8))

        self.aff_a_entry = ctk.CTkEntry(frame, width=70, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#080C14")
        self.aff_a_entry.pack(side="left", padx=(0, 20))
        self.aff_a_entry.insert(0, "5")

        lbl_b = ctk.CTkLabel(frame, text="Key B (Offset):", font=ctk.CTkFont(size=13, weight="bold"))
        lbl_b.pack(side="left", padx=(0, 8))

        self.aff_b_entry = ctk.CTkEntry(frame, width=70, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#080C14")
        self.aff_b_entry.pack(side="left")
        self.aff_b_entry.insert(0, "8")

    def _build_rsa_params(self):
        frame = ctk.CTkFrame(self.param_card, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=10)

        p_lbl = ctk.CTkLabel(frame, text="p:", font=ctk.CTkFont(size=13, weight="bold"))
        p_lbl.pack(side="left", padx=(0, 4))
        self.rsa_p_entry = ctk.CTkEntry(frame, width=65, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#080C14")
        self.rsa_p_entry.pack(side="left", padx=(0, 12))
        self.rsa_p_entry.insert(0, "61")

        q_lbl = ctk.CTkLabel(frame, text="q:", font=ctk.CTkFont(size=13, weight="bold"))
        q_lbl.pack(side="left", padx=(0, 4))
        self.rsa_q_entry = ctk.CTkEntry(frame, width=65, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#080C14")
        self.rsa_q_entry.pack(side="left", padx=(0, 12))
        self.rsa_q_entry.insert(0, "53")

        e_lbl = ctk.CTkLabel(frame, text="e:", font=ctk.CTkFont(size=13, weight="bold"))
        e_lbl.pack(side="left", padx=(0, 4))
        self.rsa_e_entry = ctk.CTkEntry(frame, width=65, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#080C14")
        self.rsa_e_entry.pack(side="left", padx=(0, 15))
        self.rsa_e_entry.insert(0, "17")

        auto_btn = ctk.CTkButton(
            frame,
            text="⚡ Auto Primes",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1E293B",
            hover_color="#334155",
            height=28,
            command=self._fill_rsa_samples
        )
        auto_btn.pack(side="right")

    def _fill_rsa_samples(self):
        self.rsa_p_entry.delete(0, "end")
        self.rsa_p_entry.insert(0, "61")
        self.rsa_q_entry.delete(0, "end")
        self.rsa_q_entry.insert(0, "53")
        self.rsa_e_entry.delete(0, "end")
        self.rsa_e_entry.insert(0, "17")
        self._set_status("Loaded RSA prime pair (p=61, q=53, e=17)")

    # ---------------------------
    # Execution & Handlers
    # ---------------------------

    def _update_stats(self, event=None):
        text = self.input_textbox.get("1.0", "end-1c")
        count = len(text)
        entropy = calc_entropy(text)
        self.char_count_lbl.configure(text=f"{count} chars | Entropy: {entropy:.2f} bits/symbol")

    def _execute_cipher_animated(self):
        if self.animation_running:
            return

        self.animation_running = True
        self.run_btn.configure(state="disabled", text="⏳ PROCESSING CIPHER STREAM...")

        start_time = time.time()
        text = self.input_textbox.get("1.0", "end-1c").strip()
        mode = "Encrypt" if "Encrypt" in self.mode_var.get() else "Decrypt"

        if not text:
            self._animate_cyber_scramble("⚠️ Error: Input message cannot be empty.", is_error=True)
            self._set_status("Execution failed: Empty input message.")
            return

        try:
            if self.active_tab == "caesar":
                shift = int(self.caesar_shift_entry.get().strip())
                if mode == "Encrypt":
                    res = caesar_encrypt(text, shift)
                else:
                    res = caesar_decrypt(text, shift)

            elif self.active_tab == "columnar":
                key = self.col_key_entry.get().strip()
                if not key:
                    raise ValueError("Columnar key word cannot be empty")
                if mode == "Encrypt":
                    res = encrypt_columnar(text, key)
                else:
                    res = decrypt_columnar(text, key)

            elif self.active_tab == "affine":
                a = int(self.aff_a_entry.get().strip())
                b = int(self.aff_b_entry.get().strip())
                if mode == "Encrypt":
                    res = affine_encrypt(text, a, b)
                else:
                    res = affine_decrypt(text, a, b)

            elif self.active_tab == "rsa":
                p = int(self.rsa_p_entry.get().strip())
                q = int(self.rsa_q_entry.get().strip())
                e = int(self.rsa_e_entry.get().strip())
                
                (pub_e, n), (priv_d, n2) = rsa_generate_keys(p, q, e)

                if mode == "Encrypt":
                    if not text.isdigit():
                        raise ValueError("RSA input must be an integer number.")
                    m = int(text)
                    cipher_val = rsa_encrypt(m, pub_e, n)
                    res = (
                        f"---------------------------------------------------\n"
                        f"  PUBLIC KEY : (e={pub_e}, n={n})\n"
                        f"  PRIVATE KEY: (d={priv_d}, n={n2})\n"
                        f"---------------------------------------------------\n"
                        f"  ENCRYPTED RESULT: {cipher_val}"
                    )
                else:
                    if not text.isdigit():
                        raise ValueError("RSA cipher must be an integer number.")
                    c = int(text)
                    dec_val = rsa_decrypt(c, priv_d, n2)
                    res = (
                        f"---------------------------------------------------\n"
                        f"  PUBLIC KEY : (e={pub_e}, n={n})\n"
                        f"  PRIVATE KEY: (d={priv_d}, n={n2})\n"
                        f"---------------------------------------------------\n"
                        f"  DECRYPTED RESULT: {dec_val}"
                    )

            elapsed = (time.time() - start_time) * 1000
            self.current_result = res
            self._log_history(f"{self.active_tab.upper()} {mode} [{len(text)}ch] ({elapsed:.1f}ms)")
            
            # Start cyber scramble animation
            self._animate_cyber_scramble(res)
            self._set_status(f"Streamed {mode} in {elapsed:.1f} ms.")

        except Exception as err:
            self._animate_cyber_scramble(f"⚠️ Error: {str(err)}", is_error=True)
            self._set_status(f"Execution error: {str(err)}")

    def _show_result(self, result_text, is_error=False):
        self.output_textbox.delete("1.0", "end")
        if is_error:
            self.output_textbox.configure(text_color="#EF4444")
        else:
            self.output_textbox.configure(text_color="#00FFB3")
        self.output_textbox.insert("1.0", result_text)

    def _change_output_format(self, fmt_choice):
        if not self.current_result or self.current_result.startswith("⚠️"):
            return
        
        raw_text = self.current_result
        if fmt_choice == "HEX":
            encoded = raw_text.encode("utf-8").hex().upper()
            self._show_result(f"HEX STREAM:\n{encoded}")
        elif fmt_choice == "Base64":
            encoded = base64.b64encode(raw_text.encode("utf-8")).decode("utf-8")
            self._show_result(f"BASE64 STREAM:\n{encoded}")
        else:
            self._show_result(raw_text)

    def _copy_output(self):
        text = self.output_textbox.get("1.0", "end-1c").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.copy_btn.configure(text="✓ Copied!", fg_color=self.SUCCESS_GREEN, text_color="#042F2E")
            self.after(2000, lambda: self.copy_btn.configure(text="📋 Copy Result", fg_color="#0B0F19", text_color=self.ACCENT_CYAN))
            self._set_status("Cipher stream copied to system clipboard.")
        else:
            self._set_status("Nothing to copy.")

    def _swap_input_output(self):
        out_text = self.output_textbox.get("1.0", "end-1c").strip()
        if out_text and not out_text.startswith("⚠️"):
            if "ENCRYPTED RESULT:" in out_text:
                out_text = out_text.split("ENCRYPTED RESULT:")[-1].strip()
            elif "DECRYPTED RESULT:" in out_text:
                out_text = out_text.split("DECRYPTED RESULT:")[-1].strip()

            self.input_textbox.delete("1.0", "end")
            self.input_textbox.insert("1.0", out_text)
            self._update_stats()
            
            current_mode = self.mode_var.get()
            new_mode = "🔓 Decrypt" if "Encrypt" in current_mode else "🔒 Encrypt"
            self.mode_var.set(new_mode)

            self._set_status("Swapped cipher stream into input.")

    def _clear_fields(self):
        self.input_textbox.delete("1.0", "end")
        self.output_textbox.delete("1.0", "end")
        self.current_result = ""
        self._update_stats()
        self._set_status("Workspace reset.")

    def _log_history(self, log_msg):
        t_stamp = time.strftime("%H:%M:%S")
        entry = f"[{t_stamp}] {log_msg}\n"
        self.history_box.insert("end", entry)
        self.history_box.see("end")

    def _set_status(self, msg):
        self.status_bar.configure(text=f"Status: {msg}")


if __name__ == "__main__":
    app = AnimatedSecurityApp()
    app.mainloop()
