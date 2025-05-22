import bcrypt, pyodbc, sys, db, state
from validators import email_valid_check, password_valid_check
from getpass import getpass
from ui import BLUE, RED, YELLOW, BOLD, RESET, print_logged_in_page
from auth import two_factor_authentication
from random import randint
from email_utils import send_email

def logged_in_page():
    """
    Displays the logged-in user interface and handles user actions in a loop until logout or quit.

    Available user commands:
        - "update password": Initiates the password update process.
        - "change email": Initiates the email change process.
        - "delete account": Deletes the current user account and exits to login page if successful.
        - "2fa": Configures or verifies two-factor authentication.
        - "logout": Logs the user out and returns to the login page.
        - "help": Reprints the available commands for reference.
        - "quit": Logs the user out and exits the program.
    """

    print_logged_in_page()  # Show command menu initially

    while True:
        # Display page heading and current user
        print(f"\n{BOLD}--->>>            {RED}LOGGED IN PAGE{RESET}         {BOLD}<<<---{RESET}\n")
        print(f"User: {state.user}")

        # Take user input and handle it using match-case
        user_choice = input(">>> ").lower()

        match user_choice:

            case "update password":
                update_password()
                
            case "change email":
                change_email()

            case "delete account":
                if delete_account():  # If account deletion is confirmed
                    return  # Exit page and return to start page
                
            case "2fa":
                two_factor_authentication()

            case "logout":
                log_out()
                return  # Exit to login
            
            case "help":
                print_logged_in_page()

            case "quit":
                log_out()
                print("Thank you for visiting Rahem's Login Simulator")
                print("See you soon!")
                sys.exit()

            case _:
                print("Invalid command")  # Fallback for unknown input


def update_password():
    """
    Update the password for the user.

    Prompts the user for a new password and update existing password.
    """
    # Display the update password page heading
    print(f"\n{BOLD}--->>>        {RED}UPDATE PASSWORD PAGE{RESET}       {BOLD}<<<---{RESET}\n")

    # Connect to the database
    connection = db.get_connection_to_db()
    cursor = connection.cursor()

    # Prompt user for a new password that passes password validation
    new_password = input("New Password: ")
    new_password = password_valid_check(new_password, "New Password: ")
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    # Commit changes to the database
    cursor.execute('UPDATE LoginInformation SET password_hash = ? WHERE email = ?', (hashed_password, state.user))
    connection.commit()

    print("Password is now updated.")

    # Always close the database connection
    db.close_connection(connection)


def forgot_password() -> None:
    """
    Reset the password for a given user.

    Prompts the user for an email and sends the given email a verification code.
    If the verification code matches then user is allowed to change the password for the given email.
    Else fail the authentication and send them to the home page
    """
    
    # Display the forgot password page heading
    print(f"\n{BOLD}--->>>       {RED}FORGOT PASSWORD PAGE{RESET}       {BOLD}<<<---{RESET}\n")

    # Prompt user for an email
    email = input("E-Mail: ")

    # Connect to the database
    connection = db.get_connection_to_db()
    cursor = connection.cursor()

    try:
        # Fetch email from the database
        cursor.execute('SELECT email FROM LoginInformation WHERE email = ?', (email,))
        cursor.fetchone()[0]
        
        # Generate a random number for authentication
        authentication_number = randint(1, 1000)

        # Send an authentication code to the provided email  
        send_email(email, "Your Authentication Code", "Authentication Code: " + str(authentication_number))
        print("Authentication code sent. Check your E-Mail.")

        # Compare user inputted code to generated authentication number
        if input("Code: ") == str(authentication_number):

            print("Authentication successful")

            # Prompt user for a new password that passes password validation
            new_password = input("New Password: ")
            new_password = password_valid_check(new_password, "New Password: ")
            hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

            # Commit changes to the database
            cursor.execute('UPDATE LoginInformation SET password_hash = ? WHERE email = ?', (hashed_password, email))
            connection.commit()

            print("Password is now updated.")

        else:
            # Send user back to homepage if code did not match authentication number
            print("Authentication failed. Going back to main menu")
            return
        
    except TypeError as acc_exists:
        # Handle case where the email was not found in the database
        print("E-Mail does not exist within database. Going back to main menu")

    finally:
        # Always close the database connection
        db.close_connection(connection)


def change_email():
    """
    Change the email for the user.

    Prompts the user for a new email and update existing email associated with user.
    """
    
    # Display the change email page heading
    print(f"\n{BOLD}--->>>         {RED}CHANGE EMAIL PAGE{RESET}         {BOLD}<<<---{RESET}\n")
    
    # Connect to the database
    connection = db.get_connection_to_db()
    cursor = connection.cursor()

    try:
        # Prompt user for email input
        newEmail = input("New E-Mail: ")

        # Validate email
        newEmail = email_valid_check(newEmail, "New E-Mail: ")

        # Update the database with the new email
        cursor.execute('UPDATE LoginInformation SET email = ? WHERE email = ?', (newEmail, state.user))
        connection.commit()
        state.user = newEmail

        print("Email updated successfuly!")

    except pyodbc.IntegrityError as accErr:
        # Handle case where the email already exists in the database
        print("Email is already asssociated with another account. Returning to logged in page.")

    finally:
        # Always close the database connection
        connection.close()


def delete_account() -> bool:
    """
    Delete the user's account.

    Prompts the user for confirmation on deleting the account. If confirmed,
    it then prompts for the user's password as a final precaution.
    Deletes the account if all validations pass.

    Returns:
        bool: True if account deletion was successful, False otherwise.
    """

    # Display the delete account page heading
    print(f"\n{BOLD}--->>>         {RED}DELETE ACCOUNT PAGE{RESET}       {BOLD}<<<---{RESET}\n")

    # Prompt the user for confirmation and convert the input to lowercase
    confirmation = input("ARE YOU SURE YOU WANT TO DELETE YOUR ACCOUNT? Y/N: ").lower()

    # Keep prompting until the user enters a valid input ('y' or 'n')
    while confirmation != 'y' and confirmation != 'n':
        print("Incorrect input. Try again.")
        confirmation = input("ARE YOU SURE YOU WANT TO DELETE YOUR ACCOUNT? Y/N: ").lower()

    # If the user chooses 'n', cancel the deletion process
    if confirmation == "n":
        print("You changed your mind. Returning to logged in page.")
        return False  # User cancelled the deletion

    # Prompt the user for their password
    password = getpass("Password: ")

    # Connect to the database
    connection = db.get_connection_to_db()
    cursor = connection.cursor()

    # Fetch the stored hashed password for the current user
    cursor.execute('SELECT password_hash FROM LoginInformation WHERE email = ?', (state.user,))
    stored_hash = cursor.fetchone()[0]

    # Check if the entered password matches the stored hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):

        print("Password accepted. Terminating account...")

        # Delete the user’s account from the database
        cursor.execute('DELETE FROM LoginInformation WHERE email = ?', (state.user,))
        connection.commit()  # Make sure the deletion is saved

        # Confirm deletion and log the user out
        print("I hope you make another account with us :(")
        log_out()
        return True
    
    else:
        # Password did not match
        print("Incorrect password. Returning to logged in page.")

    return False  # Deletion failed


def log_out():
    """
    Log out the currently logged-in user.

    Resets the global 'user' variable to None, effectively ending the session.
    """

    state.user = None  # Clear the user to log out