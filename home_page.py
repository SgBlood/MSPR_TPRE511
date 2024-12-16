from tkinter import *
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os
import requests
from utils import get_version

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

class HomePage:
    def __init__(self, root, app):  # Accepting the 'app' instance here
        self.root = root
        self.app = app  # Storing the app instance

        # Frame for home page content
        self.frame = Frame(self.root, bg='#313438')
        
        # Store icons to prevent them from being garbage collected
        self.icons = {}

        # Title frame
        self.title_frame = Frame(self.frame, bg='#202225', width=600, height=100)
        self.title_frame.pack(side=TOP, fill=X)

        # Title label
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

        # Bottom frame for navigation
        self.bottom_frame = Frame(self.frame, bg='#202225', height=60)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # Icons for bottom buttons
        self.icons["home"] = load_icon("icons\\ACCEUIL.png", (40, 40))
        self.icons["graph"] = load_icon("icons\\stats.png", (40, 40))
        self.icons["dashboard"] = load_icon("icons\\rapport.png", (40, 40))
        self.icons["ping"] = load_icon("icons\\ping.png", (40, 40))

        # Create bottom buttons and ensure they're using the correct loaded icons
        self.btn_home = Button(self.bottom_frame, image=self.icons["home"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_home_page)
        self.style_button_with_image(self.btn_home, self.icons["home"])
        self.btn_home.pack(side=LEFT, padx=20, expand=True)

        self.btn_graph = Button(self.bottom_frame, image=self.icons["graph"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_stats_page)
        self.style_button_with_image(self.btn_graph, self.icons["graph"])
        self.btn_graph.pack(side=LEFT, padx=20, expand=True)

        self.btn_dashboard = Button(self.bottom_frame, image=self.icons["dashboard"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_dashboard_page)
        self.style_button_with_image(self.btn_dashboard, self.icons["dashboard"])
        self.btn_dashboard.pack(side=LEFT, padx=20, expand=True)

        self.btn_ping = Button(self.bottom_frame, image=self.icons["ping"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command = self.app.show_ping_page)
        self.style_button_with_image(self.btn_ping, self.icons["ping"])
        self.btn_ping.pack(side=LEFT, padx=20, expand=True)

        # Version label
        self.version_label = Label(self.frame, text=f"Version: {get_version()}", font=("Helvetica", 12), fg='white', bg='#313438')
        self.version_label.pack(side=BOTTOM, anchor="sw", padx=20, pady=5)

        # Canvas with pulsating circle
        self.canvas = Canvas(self.frame, width=250, height=250, bg='#313438', bd=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")  # Center the canvas in the frame
        self.circle = self.canvas.create_oval(30, 30, 220, 220, outline="white", width=4)

        # Add "Scan" text to the center of the circle
        self.scan_text = self.canvas.create_text(125, 125, text="Scan", fill="white", font=("Arial", 20))

        self.animate_circle()

    def style_button_with_image(self, button, icon):
        """Style the buttons with images and ensure image retention."""
        # Store the icon in the button's attribute
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
        
    def show(self):
        """Display the home page"""
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        """Hide the home page"""
        self.frame.pack_forget()
        
    def animate_circle(self):
        """Animation for the pulsating circle"""
        self.canvas.coords(self.circle, 10, 10, 240, 240)  # Expand circle
        self.canvas.after(1000, self.shrink_circle)
 
    def shrink_circle(self):
        """Shrink the circle in the pulsating animation"""
        self.canvas.coords(self.circle, 30, 30, 220, 220)  # Shrink circle
        self.canvas.after(1000, self.animate_circle)
