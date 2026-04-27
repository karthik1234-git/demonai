# Demon Copilot 😈

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Demon Copilot** is an AI bot designed to handle tasks within Arch Linux. Operating through a sleek, hacker-style terminal UI known as the **"Neural Link"**, it serves as a powerful, localized assistant for your virtualized environment.

## 👁️ System Architecture

Demon Copilot is built on a cross-platform, VM-to-Host architecture designed for secure, local inference:

- **Frontend / Client:** Runs inside an **Arch Linux VM (64-bit)** hosted on Oracle VirtualBox. This is where the "Neural Link" terminal UI lives and executes tasks.
- **Backend / LLM Host:** Communicates with an **Ollama server** running on the Windows Host machine.
- **Networking:** The connection bridges the VM to the Host via the VirtualBox NAT gateway IP: `10.0.2.2`.
- **Model:** Powered by local inference using a lightweight but capable **3B parameter model** (such as Llama 3.2).

## 🖼️ Visuals

The "Neural Link" interface is intended to provide a sleek, hacker-style terminal UI for interacting with Demon Copilot.

*A repository screenshot is not currently included in this README.*

## 🚀 Installation & Setup

### 1. Windows Host Configuration (Ollama)
By default, Ollama only listens to `localhost`. You must expose it so the Arch VM can connect.

> [!WARNING]
> Setting `OLLAMA_HOST=0.0.0.0` binds Ollama on all network interfaces of the Windows host. Do **not** create a broad inbound firewall rule that exposes port `11434` to your entire LAN. Restrict access to the VirtualBox/VM network only, or otherwise limit exposure to trusted local addresses.

1. Open your Windows Environment Variables.
2. Add a new System Variable:
   - **Variable Name:** `OLLAMA_HOST`
   - **Variable Value:** `0.0.0.0`
3. Restart the Ollama application or service.
4. Update your Windows firewall to allow inbound traffic on port `11434` **only** from the VirtualBox/VM network used by your Arch guest (for example, the VirtualBox NAT path to `10.0.2.2`), rather than allowing access from all networks.

### 2. Arch Linux VM Setup
Inside your Arch Linux VirtualBox instance:

1. Clone this repository:
   ```bash
   git clone https://github.com/karthik1234-git/demonai.git
   cd demonai
   ```
2. Configure the API endpoint in the code to point to the host gateway:
   ```python
   # The current implementation hard-codes the Ollama endpoint in demon_copilot.py.
   # Update that URL to point to the VirtualBox host gateway if needed:
   "http://10.0.2.2:11434/api/generate"
   ```
3. Run the bot:
   ```bash
   python demon_copilot.py
   ```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
