from tkinter import *
from home_page import HomePage
from stats_page import StatsPage
from dashboard_page import DashboardPage
from ping_page import PingPage
import requests
import time
from home_page import HomePage

# Function to handle GitHub version retrieval with error handling and caching
class Application:
    def __init__(self, root):
        self.root = root
        self.pages = {
            "home": HomePage(self.root, self),
            "stats": StatsPage(self.root, self),
            "dashboard": DashboardPage(self.root, self),
            "ping": PingPage(self.root, self)
        }
        self.last_version_check = 0
        self.version_cache = None
        
        # Display the home page by default
        self.show_page("home")

    # Function to get version from GitHub with caching
    def get_version(self):
        current_time = time.time()
        if current_time - self.last_version_check > 3600:  # Refresh every hour
            self.last_version_check = current_time
            self.version_cache = self.fetch_version_from_github()
        return self.version_cache

    # Function to fetch the version from GitHub API
    def fetch_version_from_github(self):
        try:
            url = "https://github.com/SgBlood/MSPR_TPRE511/releases/latest"
            response = requests.get(url)
            response.raise_for_status()
            latest_release = response.json()
            if 'tag_name' in latest_release:
                return latest_release['tag_name']
            else:
                return "Unknown"
        except requests.exceptions.RequestException:
            return "Error retrieving version"

    # Show a page by its name
    def show_page(self, page_name):
        # Hide all pages
        for page in self.pages.values():
            page.hide()
        
        # Show the selected page
        self.pages[page_name].show()

    # Methods to show each specific page
    def show_home_page(self):
        self.show_page("home")

    def show_stats_page(self):
        self.show_page("stats")

    def show_dashboard_page(self):
        self.show_page("dashboard")

    def show_ping_page(self):
        self.show_page("ping")

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

# Running the Application
root = Tk()
root.geometry("600x700")
root.minsize(480, 360)
root.config(background='#313438')  # Background color for the window
app = Application(root)  # Create the application instance
root.mainloop()  # Run the application
