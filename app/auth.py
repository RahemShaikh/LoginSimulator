from validators import email_valid_check, password_valid_check
from email_utils import send_email
import db, state, bcrypt, pyodbc
from getpass import getpass
from random import randint
from ui import BLUE, RED, YELLOW, BOLD, RESET

def create_account() -> None:
    '''
    Handles the process of creating a new user account.
    Prompts the user for an email and password, validates them,
    hashes the password, and inserts the new account into the database.
    '''

    # Display the create account page heading
    print(f"\n{BOLD}--->>>        {RED}CREATE ACCOUNT PAGE{RESET}       {BOLD}<<<---{RESET}\n")

    # Prompt user for email input
    email = input("E-Mail for registration: ")

    # Validate email syntax
    email = email_valid_check(email, "E-Mail for registration: ")

    # Prompt user for password input
    password = input("Password for registration: ")

    # Validate password (non-empty)
    password = password_valid_check(password, "Password for registration: ")

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Connect to the database
    connection = db.get_connection_to_db()
    cursor = connection.cursor()

    try:
        # Attempt to insert the new account into the LoginInformation table
        cursor.execute('INSERT INTO LoginInformation (email, password_hash) VALUES (?,?)', (email, hashed_password))
        connection.commit()  # Commit the transaction to save changes
        print("Account sucessfully created!")

    except pyodbc.IntegrityError as acc_exists:
        # Handle case where the email already exists in the database
        print("Account with " + email + " already exists. Account creation failed.")  

    finally:
        # Always close the database connection
        db.close_connection(connection)


def log_in() -> str | None:
    """
    Authenticates a user by verifying their email and password.

    Prompts the user for login credentials, checks them against stored values in
    the database, and prints the result. If authentication is successful, the user's
    email is returned. Otherwise, None is returned.

    Returns:
        str | None: The email of the authenticated user, or None if authentication fails.
    """

    # Display the log in page heading
    print(f"\n{BOLD}--->>>            {RED}LOG IN PAGE{RESET}           {BOLD}<<<---{RESET}\n")

    # Prompt user for account information
    email = input("E-Mail: ")
    password = getpass("Password: ")

    # Connect to the database
    connection = db.get_connection_to_db()
    cursor = connection.cursor()

    try:
        # Fetch hashed password associated with the email
        cursor.execute("SELECT password_hash FROM LoginInformation WHERE email = ?", (email,))
        stored_hash = cursor.fetchone()[0]

        # Verify the inputted password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):

            cursor.execute('SELECT two_fa FROM LoginInformation WHERE email = ?', (email,))
            two_fa = cursor.fetchone()[0]
            
            # If account has 2fa enabled, verify with user
            if two_fa == 1:

                # Generate a random number for authentication
                authentication_number = randint(1, 1000)

                # Send code to email
                send_email(email, "Your Two Factor Authentication Code", "Two Factor Authentication Code: " + str(authentication_number))
                print("Two Factor Authentication code sent. Check your E-Mail.")

                # Compare user inputted code to generated authentication number
                if input("2-FA Code: ") == str(authentication_number):
                    print("Authentication successful")

                else:
                    print("Authentication Failed. Returning to start page.")
                    return
                
            state.user = email
            print("Login successful")

        else:
            print("Incorrect password")
            return
        
    except TypeError as acc_exists:
        # Handle case where the email was not found in the database
        print("E-Mail not found.")
        return
    
    finally:
        # Always close the database connection
        db.close_connection(connection)

    return email


def two_factor_authentication():
    """
    Enable Two-Factor Authentication (2FA) for the current user.

    Prompts the user for confirmation to enable 2FA. If confirmed,
    checks whether 2FA is already enabled. If not, updates the user's
    record in the database to enable 2FA.
    """

    # Display the two-factor authentication page heading
    print(f"\n{BOLD}--->>>            {RED}2-FA PAGE{RESET}              {BOLD}<<<---{RESET}\n")

    # Ask the user if they want to enable 2FA
    confirmation = input("Do you want to enable Two Factor Authentication? Y/N: ").lower()

    # Keep prompting until the user enters a valid input ('y' or 'n')
    while confirmation != 'y' and confirmation != 'n':
        print("Incorrect input. Try again.")
        confirmation = input("Do you want to enable Two Factor Authentication? Y/N: ").lower()

    # If the user declines, return to the logged-in page
    if confirmation == "n":
        print("You changed your mind. Returning to logged in page.")
        return  # User cancelled 2FA enable

    # Connect to the database
    connection = db.get_connection_to_db()
    cursor = connection.cursor()

    # Check if 2FA is already enabled for this user
    cursor.execute("SELECT two_fa FROM LoginInformation WHERE email = ?", (state.user,))
    validation = cursor.fetchone()[0]
    
    # If already enabled, inform the user and exit
    if validation == 1:
        print("Two Factor Authentication is already enabled. Returning to logged in page.")
        return

    # Enable 2FA for the user
    print("Enabling 2-FA...")
    cursor.execute('UPDATE LoginInformation SET two_fa = ? WHERE email = ?', (1, state.user))
    cursor.commit()
    print("2-FA is officially active.")

    # Close the database connection
    db.close_connection(connection)