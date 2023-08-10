# MISP Desktop Application

This is a simple desktop application written in Python that communicates with a MISP server using the pymisp library. The application provides a graphical user interface (GUI) where users can enter data and send it to the MISP server.

## Dependencies

Before running the application, make sure you have the following dependencies installed:

- Python 3.x
- Tkinter (included with most Python installations)
- pymisp (`pip install pymisp`)

## Installation and Setup

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Ashton-Gates/pymisp_app
cd misp-desktop-app

Install the required dependencies by running the install script:

For Linux/MacOS:
bash
Copy code
chmod +x install_dependencies.sh
./install_dependencies.sh

For Windows:
batch

Copy code
install_dependencies.bat

How to Use
Run the application:
bash
Copy code
python main.py
The application window will open. It contains three input fields for "example" and two drop-down menus labeled "example 1" with five options in each drop-down.

Enter the required data in the input fields and select options from the drop-down menus.

Click the "Submit" button to send the data to the MISP server.


License
This project is licensed under the MIT License - see the LICENSE file for details.

less
Copy code

Please make sure to replace `"https://your-misp-server-url"` and `"your-misp-api-ke
