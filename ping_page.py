import os
import subprocess
from tkinter import *
from tkinter import font as tkfont
from tkinter import messagebox
from PIL import Image, ImageTk
import ipaddress

# Function to load icons with error handling
def load_icon(path, size=(50, 50)):
    """Function to load icons with error handling"""
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

class PingPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = Frame(self.root, bg='#313438')

        # Title frame from HomePage
        self.title_frame = Frame(self.frame, bg='#202225', width=600, height=100)
        self.title_frame.pack(side=TOP, fill=X)

        # Title label from HomePage
        self.label_titre = Label(
            self.title_frame,
            text="Bienvenue sur Seahawks Harvester",
            font=tkfont.Font(family="Helvetica", size=20, weight="bold"),
            fg='white',
            bg='#202225',
            wraplength=500,
            justify="center"
        )
        self.label_titre.pack(side=TOP, pady=20)

        # Subtitle for the current page (Ping)
        self.subtitle_label = Label(self.frame, text="You are on the Ping page", font=("Helvetica", 14), fg='white', bg='#313438')
        self.subtitle_label.pack(pady=10)

        # Entry for host or subnet
        self.host_entry_label = Label(self.frame, text="Enter Host/IP or Subnet (e.g., 192.168.1.0/24)", font=("Helvetica", 12), fg='white', bg='#313438')
        self.host_entry_label.pack(pady=5)
        
        self.host_entry = Entry(self.frame, font=("Helvetica", 14), width=30)
        self.host_entry.pack(pady=10)

        # Ping Button
        self.ping_button = Button(self.frame, text="Ping", font=("Arial", 14), bg='#4CAF50', fg='white', activebackground='#45a049', activeforeground='white', relief="flat", cursor="hand2", command=self.ping_host)
        self.ping_button.pack(pady=20)

        # Results display
        self.results_label = Label(self.frame, text="Results will be displayed here.", font=("Helvetica", 12), fg='white', bg='#313438')
        self.results_label.pack(pady=10)

        # Bottom frame for navigation (same as HomePage)
        self.bottom_frame = Frame(self.frame, bg='#202225', height=60)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # Icons for bottom buttons (same as HomePage)
        self.icons = {}
        self.icons["home"] = load_icon("icons\\ACCEUIL.png", (40, 40))
        self.icons["graph"] = load_icon("icons\\stats.png", (40, 40))
        self.icons["ping"] = load_icon("icons\\ping.png", (40, 40))

        # Create bottom buttons
        self.btn_home = Button(self.bottom_frame, image=self.icons["home"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_home_page)
        self.style_button_with_image(self.btn_home, self.icons["home"])
        self.btn_home.pack(side=LEFT, padx=20, expand=True)

        self.btn_graph = Button(self.bottom_frame, image=self.icons["graph"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_stats_page)
        self.style_button_with_image(self.btn_graph, self.icons["graph"])
        self.btn_graph.pack(side=LEFT, padx=20, expand=True)

        self.btn_ping = Button(self.bottom_frame, image=self.icons["ping"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=None)  # You can add functionality here later
        self.style_button_with_image(self.btn_ping, self.icons["ping"])
        self.btn_ping.pack(side=LEFT, padx=20, expand=True)

        self.show()

    def style_button_with_image(self, button, icon):
        """Style the buttons with images and ensure image retention."""
        button.icon = icon  # Save the image reference here to prevent garbage collection
        button.config(
            image=icon,
            relief="flat",
            bg='#ffffff',  
            bd=0,
            activebackground='#ffffff',
            activeforeground='white',
            width=50,
            height=50,
            cursor="hand2"
        )
        button.bind("<Enter>", lambda e: button.config(bg="#574f4f"))
        button.bind("<Leave>", lambda e: button.config(bg="#ffffff"))

    def ping_host(self):
        """Ping the entered host or subnet."""
        host = self.host_entry.get().strip()

        if not host:
            messagebox.showerror("Input Error", "Please enter a valid host or subnet.")
            return

        # Check if it's an IP address or subnet
        if "/" in host:  # Subnet address
            self.ping_subnet(host)
        else:  # Single host
            self.ping_single_host(host)

    def ping_single_host(self, host):
        """Ping a single host."""
        try:
            # Run the ping command with a timeout of 1 second and a single ping (-n 1)
            result = subprocess.run(
                ["ping", "-n", "1", "-w", "1000", host],  # -w sets the timeout in milliseconds
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.results_label.config(text=f"Host {host} is reachable.")
            else:
                self.results_label.config(text=f"Host {host} is not reachable.")
        except Exception as e:
            self.results_label.config(text=f"Error pinging {host}: {e}")

    def ping_subnet(self, subnet):
        """Ping all hosts in a subnet."""
        try:
            network = ipaddress.IPv4Network(subnet, strict=False)

            reachable_hosts = []
            for ip in network.hosts():
                result = subprocess.run(
                    ["ping", "-n", "1", "-w", "1000", str(ip)],  # Use a timeout of 1 second per ping
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    reachable_hosts.append(str(ip))

            if reachable_hosts:
                self.results_label.config(text=f"Reachable hosts: {', '.join(reachable_hosts)}")
            else:
                self.results_label.config(text="No hosts were reachable in the subnet.")
        except Exception as e:
            self.results_label.config(text=f"Error pinging subnet {subnet}: {e}")

    def show(self):
        """Display the Ping page."""
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        """Hide the Ping page."""
        self.frame.pack_forget()
