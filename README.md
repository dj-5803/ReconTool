# ReconTool - Security Testing and Reconnaissance Assistant

![ReconTool Banner](docs/images/banner.png)

A multi-purpose security tool for reconnaissance and testing purposes.

## 🔍 Features Overview

| Tool                    | Description                                                                 | Output Example                          |
|-------------------------|-----------------------------------------------------------------------------|-----------------------------------------|
| **IP Scanner**          | Displays local machine IP and public IP address                             | `192.168.1.10` / `45.32.121.98`        |
| **Port Scanner**        | Scans target IP for open ports (common/custom ranges) with service detection| `Port 80 (http) - OPEN`                |
| **Barcode Generator**   | Creates EAN-13 barcodes from 12-digit numbers                               | `barcode_123456789012.png`             |
| **QR Code Generator**   | Generates QR codes (PNG/SVG) from text/URLs                                 | `qr_20240510_142022.png`               |
| **Password Generator**  | Creates secure passwords with customizable length/complexity                | `Xk8&qL92!fTp`                         |
| **Wordlist Generator**  | Builds custom wordlists from character sets and length parameters           | `custom_wordlist.txt` (1000+ entries)  |
| **Phone Number Info**   | Identifies carrier, location, and validity of international phone numbers   | `Carrier: Verizon (USA)`               |
| **Subdomain Scanner**   | Discovers live subdomains using a wordlist                                  | `admin.example.com → 200 OK`           |
| **DDoS Simulator**      | *(Educational)* Simulates TCP flood attacks with configurable parameters    | `Sent 15,342 packets (1024/thread)`    |

### Key Attributes
- **Safety Warnings** for potentially disruptive tools (DDoS/scanning)
- **Auto-organized outputs** in dedicated directories
- **Multi-threaded** scans for faster results
- **Phone number validation** using `phonenumbers` library
- **Dual-format export** (PNG+SVG for QR codes)


## Installation Guide
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ReconTool.git
   cd ReconTool

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the tool:
    ```bash
    python src/app.py

## Usage
See [USAGE.md](/docs/USAGE.md) for detailed usage instructions.

## Disclaimer
This tool is for educational and authorized testing purposes only. Use responsibly and legally.

## License
MIT License - See [LICENSE](LICENSE) for details.

## Contributing
Pull requests welcome! For major changes, open an issue first.
