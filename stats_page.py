from tkinter import *
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os

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

class StatsPage:
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

        # Subtitle for the current page (Dashboard)
        self.subtitle_label = Label(self.frame, text="You are on the Stats page", font=("Helvetica", 14), fg='white', bg='#313438')
        self.subtitle_label.pack(pady=10)

        # Bottom frame for navigation (same as HomePage)
        self.bottom_frame = Frame(self.frame, bg='#202225', height=60)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # Icons for bottom buttons (same as HomePage)
        self.icons = {}
        self.icons["home"] = load_icon("icons\\ACCEUIL.png", (40, 40))
        self.icons["graph"] = load_icon("icons\\stats.png", (40, 40))
        self.icons["dashboard"] = load_icon("icons\\rapport.png", (40, 40))
        self.icons["ping"] = load_icon("icons\\ping.png", (40, 40))

        # Create bottom buttons
        self.btn_home = Button(self.bottom_frame, image=self.icons["home"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_home_page)
        self.style_button_with_image(self.btn_home, self.icons["home"])
        self.btn_home.pack(side=LEFT, padx=20, expand=True)

        self.btn_graph = Button(self.bottom_frame, image=self.icons["graph"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=None)
        self.style_button_with_image(self.btn_graph, self.icons["graph"])
        self.btn_graph.pack(side=LEFT, padx=20, expand=True)

        self.btn_dashboard = Button(self.bottom_frame, image=self.icons["dashboard"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_dashboard_page)
        self.style_button_with_image(self.btn_dashboard, self.icons["dashboard"])
        self.btn_dashboard.pack(side=LEFT, padx=20, expand=True)

        self.btn_ping = Button(self.bottom_frame, image=self.icons["ping"], relief="flat", bg='#ffffff', bd=0, width=50, height=50, cursor="hand2", command=self.app.show_ping_page)  # You can add functionality here later
        self.style_button_with_image(self.btn_ping, self.icons["ping"])
        self.btn_ping.pack(side=LEFT, padx=20, expand=True)
        self.show()
        
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
        """Display the dashboard page"""
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        """Hide the dashboard page"""
        self.frame.pack_forget()
