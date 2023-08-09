from email import header
from email.base64mime import body_decode
import os
import email
import extract_msg
import tkinter.filedialog
from pymisp import PyMISP
from email.parser import Parser
from email.message import EmailMessage
import tkinter as tk
from tkinter import ttk



MISP_URL = 'https://your-misp-server-url'
MISP_KEY = 'your-misp-api-key'

class MISPDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyMISP Desktop Application")
        self.create_widgets()

    def create_widgets(self):
        # Create a Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=tk.YES, fill=tk.BOTH) # Pack the notebook to fill the entire window

        # Create frames for each tab
        self.event_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)
        self.upload_frame = ttk.Frame(self.notebook)
        self.attribute_frame = ttk.Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(self.event_frame, text='Event')
        self.notebook.add(self.search_frame, text='Search')
        self.notebook.add(self.attribute_frame, text='Attribute')

    # Configure the notebook to expand the frames
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)

        # Call methods to create widgets for each tab
        self.create_event_widgets()
        self.create_search_widgets()
        self.create_attribute_widgets()
        self.uploadtab()
        
    def create_attribute_widgets(self):
    # Attribute form
        self.attribute_type_label = tk.Label(self.attribute_frame, text="Attribute Type:") # Changed to attribute_frame
        self.attribute_type_label.grid(row=0, column=0, padx=5, pady=5)
        self.attribute_type_entry = tk.Entry(self.attribute_frame, width=30) # Changed to attribute_frame
        self.attribute_type_entry.grid(row=0, column=1, padx=5, pady=5)

        self.attribute_value_label = tk.Label(self.attribute_frame, text="Attribute Value:") # Changed to attribute_frame
        self.attribute_value_label.grid(row=1, column=0, padx=5, pady=5)
        self.attribute_value_entry = tk.Entry(self.attribute_frame, width=30) # Changed to attribute_frame
        self.attribute_value_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Button for the Attribute form
        self.submit_attribute_button = tk.Button(self.attribute_frame, text="Submit", command=self.add_attribute) # Changed to attribute_frame
        self.submit_attribute_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        
    def add_attribute(self):
        attribute_type = self.attribute_type_entry.get()
        attribute_value = self.attribute_value_entry.get()

        # Do something with the attribute data, such as sending it to MISP
        # You might call another method here or add the data to a list

        # Optionally, clear the entry fields
        self.attribute_type_entry.delete(0, tk.END)
        self.attribute_value_entry.delete(0, tk.END)
        
        pass

    def create_event_widgets(self):
        # Widgets for the Event tab
            self.event_title_label = tk.Label(self.event_frame, text="Event Title:")
            self.event_title_label.grid(row=2, column=0, padx=5, pady=5)
            self.event_title_entry = tk.Entry(self.event_frame, width=30)
            self.event_title_entry.grid(row=2, column=1, padx=5, pady=5)

            self.event_date_label = tk.Label(self.event_frame, text="Date YYYY-MM-DD:")
            self.event_date_label.grid(row=3, column=0, padx=5, pady=5)
            self.event_date_entry = tk.Entry(self.event_frame, width=30)
            self.event_date_entry.grid(row=3, column=1, padx=5, pady=5)

            self.event_description_label = tk.Label(self.event_frame, text="Event Description:")
            self.event_description_label.grid(row=4, column=0, padx=5, pady=5)
            self.event_description_entry = tk.Text(self.event_frame, width=30, height=5)
            self.event_description_entry.grid(row=4, column=1, padx=5, pady=5)

            self.category_label = tk.Label(self.event_frame, text="Category:")
            self.category_label.grid(row=5, column=0, padx=5, pady=5)
            self.category_combobox = ttk.Combobox(self.event_frame, values=["Attribute", "External analysis", "Internal reference"])
            self.category_combobox.grid(row=5, column=1, padx=5, pady=5)

            self.threat_level_label = tk.Label(self.event_frame, text="Threat Level:")
            self.threat_level_label.grid(row=6, column=0, padx=5, pady=5)
            self.threat_level_combobox = ttk.Combobox(self.event_frame, values=["High", "Medium", "Low"])
            self.threat_level_combobox.grid(row=6, column=1, padx=5, pady=5)

            self.analysis_label = tk.Label(self.event_frame, text="Analysis:")
            self.analysis_label.grid(row=7, column=0, padx=5, pady=5)
            self.analysis_combobox = ttk.Combobox(self.event_frame, values=["Initial", "Ongoing", "Completed"])
            self.analysis_combobox.grid(row=7, column=1, padx=5, pady=5)

            # Submit Button for the Event tab
            self.submit_event_button = tk.Button(self.event_frame, text="Submit", command=self.send_to_misp)
            self.submit_event_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)
    
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

            # Submit Button (Changed pack to grid)
            self.submit_button = tk.Button(self.search_frame, text="Search", command=self.search)
            self.submit_button.grid(row=2, column=1, padx=5, pady=5)


            # Display Box
            self.result_text = tk.Text(self.search_frame, width=50, height=20, wrap=tk.WORD)
            self.result_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
            
    def uploadtab(self):
        self.upload_frame = tk.Frame(self.notebook, width=600, height=600)
        self.notebook.add(self.upload_frame, text='Upload')

        # Add a button to allow users to select the .msg file
        self.upload_button = tk.Button(self.upload_frame, text="Upload .msg File", command=self.upload_msg)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)

        # Call the emailparse method to create the other widgets
        self.emailparse()

        # Define header and body_decode variables or retrieve them from elsewhere in your code
        header = "Your header text here"
        body_decode = "Your body text here"
        results = "Your results will be here"

        # Now you can insert the text into the widgets
        self.headers_text.insert(tk.END, header)
        self.body_text.insert(tk.END, body_decode)

        self.result_text.delete(1.0, tk.END)  # Clear previous content
        self.result_text.insert(tk.END, results) # Display the results

    def emailparse(self):
            # Add labels and text widgets to display the parsed email details
            self.headers_label = tk.Label(self.upload_frame, text="Headers:")
            self.headers_label.grid(row=1, column=0, padx=5, pady=5)
            self.headers_text = tk.Text(self.upload_frame, width=50, height=5)
            self.headers_text.grid(row=1, column=1, padx=5, pady=5)

            self.body_label = tk.Label(self.upload_frame, text="Body:")
            self.body_label.grid(row=2, column=0, padx=5, pady=5)
            self.body_text = tk.Text(self.upload_frame, width=50, height=10)
            self.body_text.grid(row=2, column=1, padx=5, pady=5)

            self.recipients_label = tk.Label(self.upload_frame, text="Recipients:")
            self.recipients_label.grid(row=3, column=0, padx=5, pady=5)
            self.recipients_text = tk.Text(self.upload_frame, width=50, height=5)
            self.recipients_text.grid(row=3, column=1, padx=5, pady=5)
            
        
    def send_to_misp(self):
        misp_url = MISP_URL
        misp_key = MISP_KEY

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

        # Send the event to MISP
        result = misp.add_event(event)
        if result['message'] == 'Event added.':
            print("Event added successfully!")
        else:
            print("Failed to add event.")

        for widget in self.winfo_children():
            widget.destroy()

        self.create_attribute_widgets()    

    def search(self):
        # Get the search term from the entry widget
        search_option = self.search_option_var.get()

        if search_option == "tags":
            # Fetch tags from the MISP server and display them in the Text widget
            tags = self.get_tags_from_misp()  # Implement this function to fetch tags from your MISP server
            results = "Tags available in the MISP server:\n" + "\n".join(f"• {tag}" for tag in tags)
        elif search_option == "attributes":
            # Fetch attributes from the MISP server and display them in the Text widget
            attributes = self.get_attributes_from_misp()  # Implement this function to fetch attributes from your MISP server
            results = "Attributes available in the MISP server:\n" + "\n".join(f"• {attr}" for attr in attributes)
        # Implement other options here (e.g., galaxies, taxonomies, etc.) using similar logic

        
    def get_tags_from_misp(self):
        # Implement this function to fetch tags from your MISP server
        # For example:
        misp = PyMISP(MISP_URL, MISP_KEY, False)
        tags = misp.get_all_tags()
        return [tag['name'] for tag in tags]
        # For this example, I'll just return a list of sample tags
        return ["Tag1", "Tag2", "Tag3"]
    
    def get_attributes_from_misp(self):
        # Implement this function to fetch attributes from your MISP server
        # For example:
        misp = PyMISP(MISP_URL, MISP_KEY, False)
        attributes = misp.get_all_attributes()
        return [attr['value'] for attr in attributes]
        # For this example, I'll just return a list of sample attributes
        return ["Attribute1", "Attribute2", "Attribute3"]


           
    
    def upload_msg(self):
        # Open a file dialog to select the .msg file
        file_path = tk.filedialog.askopenfilename(filetypes=[("MSG files", "*.msg")])

        # Use extract_msg to open the .msg file
        msg = extract_msg.Message(file_path)

        # Extract the headers, body, and recipients
        headers_list = []
        for key, value in msg.header.items():
            headers_list.append(f"{key}: {value}")
        headers = "\n".join(headers_list)
        body = msg.body
        recipients = ", ".join(msg.to)

        # Update the text widgets with the extracted information
        self.headers_text.delete(1.0, tk.END)
        self.headers_text.insert(tk.END, headers)
        self.body_text.delete(1.0, tk.END)
        self.body_text.insert(tk.END, body)
        self.recipients_text.delete(1.0, tk.END)
        self.recipients_text.insert(tk.END, recipients)



       
if __name__ == "__main__":
    app = MISPDesktopApp()
    app.mainloop()