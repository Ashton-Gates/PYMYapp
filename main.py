import os
import logging
from email import header
from email.base64mime import body_decode
import extract_msg
from pymisp import PyMISP
from email.parser import Parser
from email.message import EmailMessage
from secure_storage import generate_key, encrypt_data, decrypt_data, save_encrypted_data, load_encrypted_data
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

def generate_key(password): pass
def encrypt_data(data, key): pass
def decrypt_data(data, key): pass
def save_encrypted_data(file_path, data): pass
def load_encrypted_data(file_path): pass


class MISPDesktopApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title("PYMYApp")
        self.icon()
        self.set_window_icon()
        self.create_widgets()
        self.api_url = None
        self.api_key = None


        # Logging statement
        logging.info("Initializing MISPDesktopApp")
        
    def icon(self):
        img = Image.open('C:\\Portfolio\\MYPYapp\\PMA.png')
        photo = ImageTk.PhotoImage(img)
        self.iconphoto(True, photo)
        
    def set_window_icon(self):
        self.iconbitmap('C:\\Portfolio\\MYPYapp\\16x16.ico')

    def create_widgets(self):
        # Create a Notebook
        self.notebook = ttk.Notebook(self)

        # Frames for the tabs
        self.home_frame = ttk.Frame(self.notebook)
        self.event_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)
        self.upload_frame = ttk.Frame(self.notebook)
        self.attribute_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        self.documents_frame = ttk.Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(self.home_frame, text='Home')
        self.notebook.add(self.event_frame, text='Event')
        self.notebook.add(self.search_frame, text='Search')
        self.notebook.add(self.attribute_frame, text='Attribute')
        self.notebook.add(self.documents_frame, text="Documents")
        self.notebook.add(self.upload_frame, text="Email Parsing")
        self.notebook.add(self.settings_frame, text='Settings')

        # Pack the notebook to fill the entire window
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Configuration of the notebook to expand the frames
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)
        
        # Calling widgets for each tab
        self.create_home_widgets(self.home_frame)
        self.create_event_widgets()
        self.create_search_widgets()
        self.emailtab()
        self.create_attribute_widgets()
        self.documents_tab()
        self.create_settings_widgets()


    def create_home_widgets(self, tab):
          # Path to your logo image
        logo_path = 'C:/Portfolio/MYPYapp/PYMYapp.jpg'

        # Open the image
        logo_image = Image.open(logo_path)

        # Convert the image to a PhotoImage object
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Create a label to hold the image
        logo_label = tk.Label(tab, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference to the image to prevent garbage collection
        logo_label.pack() 
        
        description = """
        
        Welcome to PYMYApp!
            
        This application is a user-friendly tool that allows you to manage events, search attributes, upload files, and configure settings from the comfort of your own desktop. All you need is the API URL and API key for your MISP server :)

        Instructions:
        
        1. Navigate through the tabs to access different features!
        
        
        3. Use the 'Search' tab to find specific attributes.
        
        
        2. Use the 'Event' tab to manage your events.
        
        
        4. Use the 'Upload' tab to add files to the system. 
        
        The files will be parsed and the contents will be displayed in the fields based on the Headers, Body and Recipients. 
        
        You will have the option to connect the .msg with the UUID or IOC's with an event being made OR that has already been made.
        
        
        5. Configure the application settings using the 'Settings' tab.

        If you need help, please refer to the user manual or contact support.......which we don't have just yet ;)
        
        """
        description_label = tk.Label(tab, text=description, wraplength=1000) # wraplength to wrap the text
        description_label.pack(anchor='center')
    
    def create_event_widgets(self):
        # Widgets for the Event tab
            self.event_title_label = tk.Label(self.event_frame, text="Event Title:")
            self.event_title_label.grid(row=2, column=0, padx=5, pady=5,sticky='nsew')
            self.event_title_entry = tk.Entry(self.event_frame, width=30)
            self.event_title_entry.grid(row=2, column=1, padx=5, pady=5,sticky='nsew')

            self.event_date_label = tk.Label(self.event_frame, text="Date YYYY-MM-DD:")
            self.event_date_label.grid(row=3, column=0, padx=5, pady=5,sticky='nsew')
            self.event_date_entry = tk.Entry(self.event_frame, width=30)
            self.event_date_entry.grid(row=3, column=1, padx=5, pady=5,sticky='nsew')

            self.event_description_label = tk.Label(self.event_frame, text="Event Description:")
            self.event_description_label.grid(row=4, column=0, padx=5, pady=5,sticky='nsew')
            self.event_description_entry = tk.Text(self.event_frame, width=30, height=5)
            self.event_description_entry.grid(row=4, column=1, padx=5, pady=5,sticky='nsew')

            self.category_label = tk.Label(self.event_frame, text="Category:")
            self.category_label.grid(row=5, column=0, padx=5, pady=5,sticky='nsew')
            self.category_combobox = ttk.Combobox(self.event_frame, values=["Attribute", "External analysis", "Internal reference"])
            self.category_combobox.grid(row=5, column=1, padx=5, pady=5,sticky='nsew')

            self.threat_level_label = tk.Label(self.event_frame, text="Threat Level:")
            self.threat_level_label.grid(row=6, column=0, padx=5, pady=5,sticky='nsew')
            self.threat_level_combobox = ttk.Combobox(self.event_frame, values=["High", "Medium", "Low"])
            self.threat_level_combobox.grid(row=6, column=1, padx=5, pady=5,sticky='nsew')

            self.analysis_label = tk.Label(self.event_frame, text="Analysis:")
            self.analysis_label.grid(row=7, column=0, padx=5, pady=5,sticky='nsew')
            self.analysis_combobox = ttk.Combobox(self.event_frame, values=["Initial", "Ongoing", "Completed"])
            self.analysis_combobox.grid(row=7, column=1, padx=5, pady=5,sticky='nsew')
            
            # IOC input label and entry field
            self.ioc_label_event = tk.Label(self.event_frame, text="IOC:")
            self.ioc_label_event.grid(row=9, column=0, padx=5, pady=5,sticky='nsew')
            self.ioc_entry_event = tk.Entry(self.event_frame, width=50)
            self.ioc_entry_event.grid(row=9, column=1, padx=5, pady=5,sticky='nsew')

            # Submit Button for the Event tab
            self.submit_event_button = tk.Button(self.event_frame, text="Submit", command=self.send_to_misp)
            self.submit_event_button.grid(row=10, column=0, columnspan=2, padx=5, pady=10,sticky='nsew')
            
            self.event_status_label = tk.Label(self.event_frame, text="")
            self.event_status_label.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

            
            # Row configurations for scalable behavior
            for row in range(11):  # Range based on the number of rows you have
                self.event_frame.grid_rowconfigure(row, weight=1)

            # Column configurations for scalable behavior
            self.event_frame.grid_columnconfigure(0, weight=1)  # For labels
            self.event_frame.grid_columnconfigure(1, weight=3)     
            
    def create_attribute_widgets(self):
        # Attribute form

        self.attribute_type_label = tk.Label(self.attribute_frame, text="Attribute Type:")
        self.attribute_type_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.attribute_type_entry = tk.Entry(self.attribute_frame, width=30)
        self.attribute_type_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.attribute_value_label = tk.Label(self.attribute_frame, text="Attribute Value:")
        self.attribute_value_label.grid(row=1, column=0, padx=5, pady=5)
        self.attribute_value_entry = tk.Entry(self.attribute_frame, width=30)
        self.attribute_value_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # IOC input label and entry field
        self.ioc_label = tk.Label(self.attribute_frame, text="IOC:")
        self.ioc_label.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.ioc_entry = tk.Entry(self.attribute_frame, width=30)
        self.ioc_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        # Submit Button for the Attribute form
        self.submit_attribute_button = tk.Button(self.attribute_frame, text="Submit", command=self.add_attribute)
        self.submit_attribute_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky='ew')

        self.attribute_status_label = tk.Label(self.attribute_frame, text="")
        self.attribute_status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def add_attribute(self):
        logging.debug("Adding attribute.")
        attribute_type = self.attribute_type_entry.get()
        attribute_value = self.attribute_value_entry.get()
        ioc_value = self.ioc_entry.get()
        self.process_ioc(ioc_value)
        self.attribute_type_entry.delete(0, tk.END)
        self.attribute_value_entry.delete(0, tk.END)
        self.ioc_entry.delete(0, tk.END)

    def get_attributes_from_misp(self):
        MISP_URL = self.api_url
        MISP_KEY = self.api_key
        misp = PyMISP(MISP_URL, MISP_KEY, False)
        attributes = misp.search(controller='attributes')  # You may need to adjust the search parameters

        # Enumerate through the attributes and format each one with its index (starting from 1)
        formatted_attributes = [f"{index}. {attr['Attribute']['value']}" for index, attr in enumerate(attributes['response'], start=1)]
        return formatted_attributes
                       
    def emailtab(self):
  


        # Button to allow users to select the .msg file
        self.upload_button = tk.Button(self.upload_frame, text="Upload .msg File", command=self.upload_msg)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)
        
        
        self.upload_frame.grid_rowconfigure(1, weight=1)  # Makes row 1 expandable
        self.upload_frame.grid_columnconfigure(1, weight=1)  # Makes column 1 expandable
        
        # Labels and text widgets to display the parsed email details
        self.headers_label = tk.Label(self.upload_frame, text="Headers:")
        self.headers_label.grid(row=1, column=0, padx=5, pady=5)

        # Text widget
        self.headers_text = tk.Text(self.upload_frame, width=50, height=10, wrap=tk.WORD)
        self.headers_text.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        # Scrollbar and set it next to the Text widget
        self.scrollbar = tk.Scrollbar(self.upload_frame, command=self.headers_text.yview)
        self.scrollbar.grid(row=1, column=2, sticky='ns')

        # Scrollbar with the Text widget
        self.headers_text.config(yscrollcommand=self.scrollbar.set)

        self.body_label = tk.Label(self.upload_frame, text="Body:")
        self.body_label.grid(row=2, column=0, padx=5, pady=5)
        self.body_text = tk.Text(self.upload_frame, width=50, height=10)
        self.body_text.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        self.recipients_label = tk.Label(self.upload_frame, text="Recipients:")
        self.recipients_label.grid(row=3, column=0, padx=5, pady=5)
        self.recipients_text = tk.Text(self.upload_frame, width=50, height=10)
        self.recipients_text.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')
        
        # IOC input label and entry field
        self.ioc_label = tk.Label(self.upload_frame, text="IOC:")
        self.ioc_label.grid(row=4, column=0, padx=5, pady=5)
        self.ioc_entry = tk.Entry(self.upload_frame, width=50)
        self.ioc_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Button to process the IOC
        self.ioc_button = tk.Button(self.upload_frame, text="Process IOC", command=self.process_ioc)
        self.ioc_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5) 
        
        self.email_status_label = tk.Label(self.upload_frame, text="")
        self.email_status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
        header = "Your header text here"
        body_decode = "Your body text here"
        results = "Your results will be here"
        
        # Copy/Paste into text widgets
        self.headers_text.insert(tk.END, header)
        self.body_text.insert(tk.END, body_decode)

        self.result_text.delete(1.0, tk.END)  # Clear previous content
        self.result_text.insert(tk.END, results) # Display the results
 
    def upload_msg(self):
        # Selecting the .msg file
        file_path = tk.filedialog.askopenfilename(filetypes=[("MSG files", "*.msg")])
        print("Selected file path:", file_path)  # Debugging line

        # Use extract_msg to open the .msg file
        msg = extract_msg.Message(file_path)
        # Extract the headers, body, and recipients
        headers_list = []
        for key, value in msg.header.items():
            headers_list.append(f"{key}: {value}")
        headers = "\n".join(headers_list)
        body = msg.body
        recipients = " ".join(msg.to)

        self.headers_text.delete(1.0, tk.END)
        self.headers_text.insert(tk.END, headers)
        self.body_text.delete(1.0, tk.END)
        self.body_text.insert(tk.END, body)
        self.recipients_text.delete(1.0, tk.END)
        self.recipients_text.insert(tk.END, recipients)
        
        self.email_status_label.config(text="This email has been connected to the IOC successfully!")
    
    def documents_tab(self):

        # Button to allow users to select a document
        self.document_button = tk.Button(self.documents_frame, text="Upload Document", command=self.upload_document)
        self.document_button.grid(row=0, column=0, padx=5, pady=5)

        # Label to display the selected file name
        self.selected_file_label = tk.Label(self.documents_frame, text="Selected File:")
        self.selected_file_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # IOC/UUID input label and entry field
        self.ioc_label = tk.Label(self.documents_frame, text="IOC/UUID:")
        self.ioc_label.grid(row=3, column=0, padx=5, pady=5)
        self.ioc_entry = tk.Entry(self.documents_frame, width=50)
        self.ioc_entry.grid(row=3, column=1, padx=5, pady=5)

        # "Submit" button inside the documents frame
        self.submit_event_button = tk.Button(self.documents_frame, text="Submit", command=self.submit_document)
        self.submit_event_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        self.document_status_label = tk.Label(self.documents_frame, text="")
        self.document_status_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


        
        
    def upload_document(self):
        ioc_uuid = None  # Initialize to None
        try:
            # Open a file dialog to select the document
            self.selected_file_path = tk.filedialog.askopenfilename(filetypes=[("Document files", "*.pdf;*.doc;*.docx;*.xls;*.xlsx")])

            # Check if user canceled the file dialog
            if not self.selected_file_path:
                logging.info("File dialog was canceled by the user.")
                return  # Exit the function if no file was selected

            # Extract the file name from the file path
            file_name = os.path.basename(self.selected_file_path)

            # Update the label to display the selected file name
            self.selected_file_label.config(text=f"Selected file: {file_name}")

            # Retrieve the IOC/UUID from the entry widget
            ioc_uuid = self.ioc_entry.get()
            logging.info(f"Select file path: {self.selected_file_path}, IOC/UUID: {ioc_uuid}")

            # Optionally, clear the IOC/UUID field for the next upload
            self.ioc_entry.delete(0, tk.END)

            # Delay the execution of submit_to_misp slightly to give GUI time to update
            self.after(100, lambda: self.submit_to_misp(self.selected_file_path, ioc_uuid))
        except Exception as e:
            logging.error(f"Error during document upload: {e}")

    def submit_document(self):
        logging.debug("Submitting document.")
        ioc_uuid = self.ioc_entry.get()  # Retrieve the IOC/UUID from the entry widget
        if hasattr(self, 'selected_file_path') and ioc_uuid:  # Check if selected_file_path and ioc_uuid are defined
            self.submit_to_misp(self.selected_file_path, ioc_uuid)  # Call submit_to_misp
            
            self.document_status_label.config(text="This document has been connected to the IOC successfully!")
        elif not ioc_uuid:
            logging.warning("No IOC/UUID provided.")
        else:
            logging.warning("No file has been selected yet.")
      


    def create_search_widgets(self):
            # Widgets for the Search tab
            self.search_label = tk.Label(self.search_frame, text="Search:")
            self.search_label.grid(row=0, column=0, padx=5, pady=5)

            self.search_entry = tk.Entry(self.search_frame, width=30)
            self.search_entry.grid(row=0, column=1, padx=5, pady=5)

            self.search_button = tk.Button(self.search_frame, text="Search", command=self.search)
            self.search_button.grid(row=0, column=2, padx=5, pady=5)

            # Dropdown menu with options
            self.search_option_var = tk.StringVar(self.search_frame)
            self.search_option_var.set("tags")
            self.search_option_menu = ttk.OptionMenu(self.search_frame, self.search_option_var, "Tags", "Tags", "Attributes",
                                                    "Tag Collections", "Proposals", "Taxonomies", "Galaxies")
            self.search_option_menu.grid(row=1, column=0, padx=5, pady=5, columnspan=3)


            # Display Box
            self.result_text = tk.Text(self.search_frame, width=50, height=20, wrap=tk.WORD)
            self.result_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
            
            for row in range(4):  # Adjust the range based on the number of rows you have
                self.search_frame.grid_rowconfigure(row, weight=1)

            # Adjust column configurations for scalable behavior
            self.search_frame.grid_columnconfigure(0, weight=1)  # For labels
            self.search_frame.grid_columnconfigure(1, weight=3)  # For entry boxes and buttons
            self.search_frame.grid_columnconfigure(2, weight=1)  # For other buttons
    
    def search(self):
        # Get the search term from the entry widget
        search_option = self.search_option_var.get()

        if search_option == "tags":
            # Fetch tags from the MISP server and display them in the Text widget
            tags = self.get_tags_from_misp()  # Implement this function to fetch tags from your MISP server
            results = "Tags available in the MISP server:\n" + "\n".join(tags)
        elif search_option == "attributes":
            # Fetch attributes from the MISP server and display them in the Text widget
            attributes = self.get_attributes_from_misp()  # Implement this function to fetch attributes from your MISP server
            results = "Attributes available in the MISP server:\n" + "\n".join(attributes)
        # Implement other options here (e.g., galaxies, taxonomies, etc.)

        # Results into the 'result_text' widget:
        self.result_text.delete(1.0, tk.END)  # Clear previous content
        self.result_text.insert(tk.END, results)  # Insert new results

    
    def create_settings_widgets(self):
        # API Configuration Button
        self.api_config_button = tk.Button(self.settings_frame, text="API Configuration", command=self.open_api_config_window)
        self.api_config_button.grid(row=0, column=5, padx=5, pady=10)

        # Language selection
        #self.language_label = tk.Label(self.settings_frame, text="Language:")
        #self.language_label.grid(row=1, column=0, padx=5, pady=5)
        #self.language_combobox = ttk.Combobox(self.settings_frame, values=["English", "Spanish", "French"])
        #self.language_combobox.grid(row=1, column=1, padx=5, pady=5)

         # API selection
        self.api_label = tk.Label(self.settings_frame, text="\n\n\n\n\nSelect API:\n\n\n\n\n")
        self.api_label.grid(row=7, column=5, padx=5, pady=5)
        self.api_combobox = ttk.Combobox(self.settings_frame, values=[])
        self.api_combobox.grid(row=7, column=6, padx=5, pady=5)
        
        #About Me :)
        self.about_me = tk.Label(self.settings_frame, text="About Me :\n\nVersion: 1.0\n\nAuthor: Ashton Kinnell")
        self.about_me.grid(row=10, column=5, padx=5, pady=5)
        
    def open_api_config_window(self):
        self.api_config_window = tk.Toplevel(self)
        self.api_config_window.title("API Configuration")
        self.api_config_button.pack(side=tk.TOP, expand=True)

        # API URL
        self.api_url_label = tk.Label(self.api_config_window, text="API URL:")
        self.api_url_label.grid(row=0, column=0, padx=5, pady=5)
        self.api_url_entry = tk.Entry(self.api_config_window, width=50)
        self.api_url_entry.grid(row=0, column=1, padx=5, pady=5)

        # API Key
        self.api_key_label = tk.Label(self.api_config_window, text="API Key:")
        self.api_key_label.grid(row=1, column=0, padx=5, pady=5)
        self.api_key_entry = tk.Entry(self.api_config_window, width=50)
        self.api_key_entry.grid(row=1, column=1, padx=5, pady=5)

        # Save Button
        self.save_api_button = tk.Button(self.api_config_window, text="Save", command=self.save_api_credentials)
        self.save_api_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        MISP_URL = self.api_url_entry.get()
        MISP_KEY = self.api_key_entry.get()
        # Save the credentials
        print(f"Saved URL: {MISP_URL}, Key: {MISP_KEY}")
        
        pass
        
        self.show_about()
        
        
    



    def open_api_config_window(self):
        api_config_window = tk.Toplevel(self)
        api_config_window.title("API Configuration")

        api_name_label = tk.Label(api_config_window, text="API Name:")
        api_name_label.grid(row=0, column=0, padx=5, pady=5)
        api_name_entry = tk.Entry(api_config_window, width=50)
        api_name_entry.grid(row=0, column=1, padx=5, pady=5)

        api_url_label = tk.Label(api_config_window, text="API URL:")
        api_url_label.grid(row=1, column=0, padx=5, pady=5)
        api_url_entry = tk.Entry(api_config_window, width=50)
        api_url_entry.grid(row=1, column=1, padx=5, pady=5)

        api_key_label = tk.Label(api_config_window, text="API Key:")
        api_key_label.grid(row=2, column=0, padx=5, pady=5)
        api_key_entry = tk.Entry(api_config_window, width=50)
        api_key_entry.grid(row=2, column=1, padx=5, pady=5)

        save_api_button = tk.Button(api_config_window, text="Save", command=lambda: self.save_api_credentials(api_name_entry.get(), api_url_entry.get(), api_key_entry.get()))
        save_api_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        pass
        
    

    def save_api_credentials(self, api_name, api_url, api_key):
        logging.debug(f"Saving API credentials for: {api_name}.")
        self.api_name = api_name
        self.api_url = api_url
        self.api_key = api_key
        current_values = self.api_combobox['values']
        self.api_combobox['values'] = current_values + (api_name,)


    def get_tags_from_misp(self):
        MISP_URL = self.api_url
        MISP_KEY = self.api_key
        misp = PyMISP(MISP_URL, MISP_KEY, False)
        tags = misp.get_all_tags()

        # Enumerate through the tags and format each one with its index (starting from 1)
        formatted_tags = [f"{index}. {tag['name']}" for index, tag in enumerate(tags, start=1)]
        return formatted_tags
     
    def process_ioc(self):
        ioc_value = self.ioc_entry.get() # Retrieve the value from the entry widget
        # Handle the IOC value as needed, such as triggering an event or processing the data
        
        # Update the status label with the success message
        self.email_status_label.config(text="This email has been connected to the IOC successfully!")
    
    def send_to_misp(self):
        logging.debug("Initiating send to MISP.")
        print("Sending to MISP")
        
    def submit_to_misp(self, file_path, ioc_uuid):
        try:
            misp_url = MISP_URL
            misp_key = MISP_KEY
            MISP_URL = self.api_url
            MISP_KEY = self.api_key

            event_title = self.event_title_entry.get()
            event_date = self.event_date_entry.get()
            event_description = self.event_description_entry.get("1.0", tk.END)
            category = self.category_combobox.get()
            threat_level = self.threat_level_combobox.get()
            analysis = self.analysis_combobox.get()

            # Create a MISP connection
            misp = PyMISP(misp_url, misp_key, False)

            # Create the MISP event
            event = misp.new_event(threat_level_id=threat_level, analysis=analysis)
            event.info = event_title
            event.date = event_date
            event.description = event_description.strip()

            # Add attributes to the event
            event.add_attribute("category", category)

            # Attach the document to the event
            misp.add_named_attribute(event, 'malware-sample', value=file_path)

            # Add the IOC/UUID as an attribute if provided
            if ioc_uuid:
                misp.add_named_attribute(event, 'text', value=ioc_uuid, comment="Associated IOC/UUID")

            # Send the event to MISP
            result = misp.add_event(event)
            if result['message'] == 'Event added.':
                print("Event and document added successfully!")
            else:
                print("Failed to add event and document.")
            
            if result['message'] == 'Event added.':
                logging.info("Event and document added successfully!")
            
            else:
                logging.warning(f"Failed to add event and document: {result['message']}")
                
        except Exception as e:
            logging.error(f"Error during MISP submission: {e}")  
    
    

if __name__ == "__main__":
       
    app = MISPDesktopApp()
    app.mainloop()
