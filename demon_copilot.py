import customtkinter as ctk
import os
import threading
import requests
import subprocess
import pyperclip 

# --- Appearance Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Exact mapping from your 'ollama list'
MODELS = {
    "Pro (3B)": "llama3.2:latest",
    "Fast (1B)": "llama3.2:1b",
    "Thinking (R1)": "deepseek-r1:1.5b",
    "Coder (6.7B)": "deepseek-coder:6.7b",
    "Phi-3": "phi3:latest"
}

class Controller(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Demon Copilot")
        self.geometry("720x680")
        
        # --- The "Beautiful" UI Config ---
        self.attributes('-alpha', 0.9)  # 90% Transparency for that ghost overlay
        self.is_pinned = True
        self.attributes('-topmost', True)
        self.configure(fg_color="#050505") # OLED Black

        # --- Top Navigation Bar ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.top_frame, text="NEURAL LINK: 10.0.2.2", 
                     font=("Courier New", 14, "bold"), text_color="#00FF41").pack(side="left")

        # Window Buttons
        self.min_btn = ctk.CTkButton(self.top_frame, text="-", width=35, fg_color="#222", command=self.iconify)
        self.min_btn.pack(side="right", padx=2)

        self.pin_btn = ctk.CTkButton(self.top_frame, text="📌", width=35, 
                                     fg_color="#00FF41", text_color="black", command=self.toggle_pin)
        self.pin_btn.pack(side="right", padx=2)

        self.mode_selector = ctk.CTkOptionMenu(self.top_frame, values=list(MODELS.keys()), 
                                              width=140, fg_color="#1a1a1a", button_color="#333")
        self.mode_selector.pack(side="right", padx=5)

        # --- Matrix Chat Window ---
        self.chat = ctk.CTkTextbox(self, width=680, height=480, wrap="word", 
                                  font=("Courier New", 13), fg_color="#0a0a0a", 
                                  text_color="#00FF41", border_color="#00FF41", border_width=1)
        self.chat.pack(pady=10, padx=20)
        self.log(">>> System Initialized. Waiting for input, Demon.")
        
        # --- Input Section ---
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ask the hivemind...", 
                                 width=580, fg_color="#111", border_color="#333")
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", self.process_input)

        self.engage_btn = ctk.CTkButton(self.input_frame, text="→", width=50, 
                                       fg_color="#00FF41", text_color="black", command=self.process_input)
        self.engage_btn.pack(side="right")

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.attributes('-topmost', self.is_pinned)
        self.pin_btn.configure(fg_color="#00FF41" if self.is_pinned else "#444")

    def log(self, text):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"\n{text}\n")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def process_input(self, event=None):
        user_text = self.entry.get()
        if not user_text: return
        self.entry.delete(0, "end")
        self.log(f"[YOU]: {user_text}")
        
        cmd = user_text.lower()
        if cmd == "code":
            subprocess.Popen(["code"])
        elif "sim" in cmd or "verilator" in cmd:
            self.log("--- Executing Verilator Lab Suite ---")
            # Assumes your project is in this directory
            subprocess.Popen(["verilator", "--binary", "-j", "0", "vedic_multiplier.sv", "tb_top.sv"])
        else:
            selected_mode = MODELS[self.mode_selector.get()]
            threading.Thread(target=self.ask_host_ai, args=(user_text, selected_mode)).start()

    def ask_host_ai(self, prompt, model_name):
        system_instruction = (
            "You are the Demon Copilot, a high-level ECE assistant. "
            "You specialize in SystemVerilog, CMOS layouts (Virtuoso/Innovus), and Vedic Math logic. "
            "Be technical, concise, and prioritize hardware efficiency."
        )

        try:
            url = 'http://10.0.2.2:11434/api/generate'
            payload = {
                "model": model_name, 
                "prompt": prompt, 
                "system": system_instruction,
                "stream": False
            }
            # Timeout set to 60s for the 6.7B model to think
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                answer = response.json().get('response', 'Empty Brain...')
                self.log(f"[DEMON]: {answer}")
            else:
                self.log(f"[CRITICAL ERROR]: Server returned {response.status_code}. Check 'ollama list'.")
                
        except Exception as e:
            self.log(f"[LINK SEVERED]: Could not reach Windows Host. Ensure OLLAMA_HOST is 0.0.0.0.")

if __name__ == "__main__":
    app = Controller()
    app.mainloop()
