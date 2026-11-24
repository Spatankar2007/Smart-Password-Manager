# Smart Password Manager and Encryptor

## Project Overview
Smart Password Manager and Encryptor is a Python-based desktop application developed using Tkinter. It is designed to help users securely manage their account passwords through master-password authentication, encryption, and password-management features.

The project was developed as part of Project Exhibition I.

## Features
- **Master Password Authentication:** Provides a login system to access the application.
- **Password Management:** Add, retrieve, search, update, and delete stored account passwords.
- **Password Generator:** Generates strong passwords.
- **Password Strength Checker:** Evaluates password strength.
- **Encryption and Decryption:** Uses Fernet symmetric encryption to protect stored passwords.
- **Encrypted Local Storage:** Stores password information locally in JSON format.
- **Activity Logging:** Maintains a record of application activities.

## Technologies Used
- Python
- Tkinter
- Cryptography (Fernet)
- JSON
- Visual Studio Code

## Project Structure
- `Login_Ver2.py` – Login interface.
- `Login_Dashboard_Ver2.py` – User dashboard.
- `menu_integrationVer2.py` – Integrated password-management functionality.
- `Password_generator.py` – Password generation module.
- `Strength_checker.py` – Password strength analysis module.

## Installation and Execution

1. Install Python on your computer.
2. Install the required cryptography library:

   `pip install cryptography`

3. Download or clone this repository.
4. Open the project folder in VS Code.
5. Run the login application:

   `python Login_Ver2.py`

*Note: The application may require its local data files and encryption configuration to be initialized. Follow the project's setup requirements before using it.*

## Security Note
This repository is intended for educational and demonstration purposes. Never upload real passwords, encryption keys, master-password hashes, or private user data to a public repository.

## Author
**Swarali Shailesh Patankar**

Integrated M.Tech – Computer Science and Engineering  
Computational and Data Science  
VIT Bhopal University