from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import font as tkfont
from functionalities.scan import scan_network
from utils import get_version
from PIL import Image, ImageTk
import os
import threading

def load_icon(path, size=(40, 40)):
    """Load icons with error handling."""
    if os.path.exists(path):
        try:
            img = Image.open(path).resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image: {path}, {e}")
            return None
    else:
        print(f"Error: {path} is missing.")
        return None

from tkinter import ttk

class HomePage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = Frame(self.root, bg='#313438')
        self.icons = {}

        # Title frame
        self.title_frame = Frame(self.frame, bg='#202225', height=100)
        self.title_frame.pack(side=TOP, fill=X)
        
        self.title_label = Label(
            self.title_frame,
            text="Seahawks Harvester",
            font=tkfont.Font(family="Helvetica", size=20, weight="bold"),
            fg='white',
            bg='#202225'
        )
        self.title_label.pack(pady=20)

        # Canvas for the pulsating circle
        self.canvas = Canvas(self.frame, width=250, height=250, bg='#313438', bd=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.4, anchor="center")
        self.circle = self.canvas.create_oval(30, 30, 220, 220, outline="white", width=4)
        
        # Add "Scan" button inside the circle
        self.scan_button = Button(
            self.canvas,
            text="Scan",
            font=tkfont.Font(family="Arial", size=16, weight="bold"),
            bg='#313438',
            fg='white',
            activebackground='#41464b',
            activeforeground='white',
            relief="flat",
            cursor="hand2",
            command=self.start_scan
        )
        self.canvas.create_window(125, 125, window=self.scan_button)

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress.place(relx=0.5, rely=0.65, anchor="center")
        
        self.animate_circle()

        # Bottom navigation bar
        self.bottom_frame = Frame(self.frame, bg='#202225', height=60)
        self.bottom_frame.pack(side=BOTTOM, fill=X)
        
        self.setup_navigation()

        # Version label
        self.version_label = Label(
            self.frame,
            text=f"Version: {get_version()}",
            font=("Helvetica", 10),
            fg='white',
            bg='#313438'
        )
        self.version_label.pack(side=BOTTOM, anchor="sw", padx=10, pady=5)

    def setup_navigation(self):
        """Set up the navigation bar with icons."""
        self.icons["home"] = load_icon("icons\\ACCEUIL.png")
        self.icons["graph"] = load_icon("icons\\stats.png")
        self.icons["ping"] = load_icon("icons\\ping.png")
        
        self.add_nav_button(self.icons["home"], self.app.show_home_page)
        self.add_nav_button(self.icons["graph"], self.app.show_stats_page)
        self.add_nav_button(self.icons["ping"], self.app.show_ping_page)

    def add_nav_button(self, icon, command):
        """Add a navigation button to the bottom frame."""
        button = Button(
            self.bottom_frame,
            image=icon,
            bg='#202225',
            relief="flat",
            activebackground='#41464b',
            bd=0,
            cursor="hand2",
            command=command
        )
        button.icon = icon  # Prevent garbage collection of the image
        button.pack(side=LEFT, padx=20, expand=True)

    def start_scan(self):
        """Trigger the scan functionality in the background."""
        scan_type = simpledialog.askstring("Scan Type", "Enter scan type:\n1 - Single IP\n2 - Subnet (current IP)")

        if scan_type == "1":
            ip_address = simpledialog.askstring("Single IP", "Enter the IP address to scan:")
            if ip_address:
                output_file = "single_ip_scan_results.json"
                threading.Thread(target=self.run_scan, args=(ip_address, output_file)).start()
        elif scan_type == "2":
            # Automatically detect local IP and calculate the subnet
            local_ip = self.get_local_ip()
            subnet = self.get_subnet_from_ip(local_ip)
            output_file = "subnet_scan_results.json"
            threading.Thread(target=self.run_scan, args=(subnet, output_file)).start()
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid scan type (1 or 2).")

    def run_scan(self, network_range, output_file):
        """Run the scan in a separate thread."""
        try:
            # Run scan and update the progress bar
            scan_network(network_range, output_file, progress_callback=self.update_progress)
            messagebox.showinfo("Scan Complete", f"Results saved to {output_file}.")
        except Exception as e:
            messagebox.showerror("Scan Error", f"An error occurred during the scan: {e}")

    def update_progress(self, progress):
        """Update the progress bar."""
        self.progress['value'] = progress
        self.root.update_idletasks()  # Update the GUI to reflect the progress change

    def get_local_ip(self):
        """Get the local IP address of the machine."""
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))  # This won't actually connect but will determine the local IP
            local_ip = s.getsockname()[0]
        except:
            local_ip = '127.0.0.1'  # Fallback to localhost if unable to detect the local IP
        finally:
            s.close()
        return local_ip

    def get_subnet_from_ip(self, local_ip):
        """Given a local IP address, calculate the subnet to scan."""
        import ipaddress
        network = ipaddress.IPv4Network(local_ip + '/24', strict=False)
        return str(network.network_address) + '/24'

    def animate_circle(self):
        """Animation for the pulsating circle."""
        self.canvas.coords(self.circle, 10, 10, 240, 240)
        self.canvas.after(1000, self.shrink_circle)

    def shrink_circle(self):
        """Shrink the circle in the pulsating animation."""
        self.canvas.coords(self.circle, 30, 30, 220, 220)
        self.canvas.after(1000, self.animate_circle)

    def show(self):
        """Show the Home Page."""
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        """Hide the Home Page."""
        self.frame.pack_forget()
