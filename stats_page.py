from tkinter import *
from tkinter import filedialog, messagebox
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
    def __init__(self, root, app, scan_results_dir):
        self.root = root
        self.app = app
        self.scan_results_dir = scan_results_dir
        self.frame = Frame(self.root, bg='#313438')

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

        # Subtitle for the current page (Stats)
        self.subtitle_label = Label(self.frame, text="You are on the Stats page", font=("Helvetica", 14), fg='white', bg='#313438')
        self.subtitle_label.pack(pady=10)

        # Add the Download TXT button
        self.download_button = Button(
            self.frame,
            text="Download Latest Scan Results",
            font=("Arial", 14),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief="flat",
            cursor="hand2",
            command=self.download_latest_scan_file
        )
        self.download_button.pack(pady=20)

        # Refresh button
        self.refresh_button = Button(
            self.frame,
            text="Refresh",
            font=("Arial", 14),
            bg='#FF9800',
            fg='white',
            activebackground='#ff8f00',
            activeforeground='white',
            relief="flat",
            cursor="hand2",
            command=self.refresh_page
        )
        self.refresh_button.pack(pady=10)

        # Bottom frame for navigation
        self.bottom_frame = Frame(self.frame, bg='#202225', height=60)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # Icons for bottom buttons
        self.icons = {}
        self.icons["home"] = load_icon("icons\\ACCEUIL.png", (40, 40))
        self.icons["graph"] = load_icon("icons\\stats.png", (40, 40))
        self.icons["ping"] = load_icon("icons\\ping.png", (40, 40))

        # Create bottom buttons
        button_bg_color = '#323739'  # Slightly lighter than the bottom frame's color

        # Home button
        self.btn_home = Button(self.bottom_frame, image=self.icons["home"], relief="flat", bg=button_bg_color, bd=0, width=50, height=50, cursor="hand2", command=self.app.show_home_page)
        self.style_button_with_image(self.btn_home, self.icons["home"])
        self.btn_home.pack(side=LEFT, padx=20, expand=True)

        # Graph button
        self.btn_graph = Button(self.bottom_frame, image=self.icons["graph"], relief="flat", bg=button_bg_color, bd=0, width=50, height=50, cursor="hand2", command=self.app.show_stats_page)
        self.style_button_with_image(self.btn_graph, self.icons["graph"])
        self.btn_graph.pack(side=LEFT, padx=20, expand=True)

        # Ping button
        self.btn_ping = Button(self.bottom_frame, image=self.icons["ping"], relief="flat", bg=button_bg_color, bd=0, width=50, height=50, cursor="hand2", command=self.app.show_ping_page)
        self.style_button_with_image(self.btn_ping, self.icons["ping"])
        self.btn_ping.pack(side=LEFT, padx=20, expand=True)

        # Check for available scan files and update the download button
        self.update_download_button()

        # Start the auto-refresh mechanism
        self.auto_refresh()

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

    def list_scan_files(self):
        """List available scan files in the specified scan results directory."""
        try:
            if not os.path.exists(self.scan_results_dir):
                print(f"Directory not found: {self.scan_results_dir}")
                return []
            
            files = [f for f in os.listdir(self.scan_results_dir) if f.endswith('.txt') or f.endswith('.json')]
            print(f"Files found: {files}")  # Debugging line
            return files
        except Exception as e:
            print(f"Error reading scan files: {e}")
            return []

    def update_download_button(self):
        """Update the download button based on available scan files."""
        files = self.list_scan_files()
        
        if files:
            self.download_button.config(text="Download Latest Scan Results")
            self.download_button.config(state=NORMAL)
        else:
            self.download_button.config(text="No Scan Files Available")
            self.download_button.config(state=DISABLED)

    def download_latest_scan_file(self):
        """Prompt the user to download the latest scan result file."""
        try:
            files = self.list_scan_files()
            if files:
                # Determine the most recent file based on creation time
                latest_file = max(
                    (os.path.join(self.scan_results_dir, f) for f in files), 
                    key=os.path.getctime
                )
                print(f"Latest file detected: {latest_file}")  # Debugging line
                
                # Prompt the user to save the file
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text Files", "*.txt")],
                    title="Save TXT Scan Results",
                    initialfile=os.path.basename(latest_file)
                )
                if file_path:
                    # Copy the content to the selected location
                    with open(latest_file, "r") as src_file:
                        content = src_file.read()
                    with open(file_path, "w") as dest_file:
                        dest_file.write(content)
                    messagebox.showinfo("Download Complete", f"Scan results have been saved to {file_path}.")
            else:
                messagebox.showerror("No Files", "No scan files found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading the file: {e}")

    def refresh_page(self):
        """Manually refresh the Stats page."""
        self.update_download_button()

    def auto_refresh(self):
        """Automatically refresh the page every 10 seconds."""
        self.update_download_button()
        self.root.after(30000, self.auto_refresh)  # Refresh every 10 seconds

    def show(self):
        """Display the Stats page."""
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        """Hide the Stats page."""
        self.frame.pack_forget()
