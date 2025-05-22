import re

def email_valid_check(email, terminal_message) -> str:
    '''
    Validates the syntax of an email address using a regular expression.
    If the provided email is invalid, repeatedly prompts the user for a valid email.

    Args:
        email (str): The initial email address to validate.
        terminal_message (str): The prompt message displayed when asking for a new email input.

    Returns:
        str: A valid email address entered by the user.
    '''

    # Define the regex pattern for a valid email address
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Check if the initial email matches the pattern
    valid = re.match(pattern, email)

    # Keep prompting the user until a valid email is entered
    while not valid:
        print("Not valid E-Mail syntax. Try again")
        email = input(terminal_message)
        valid = re.match(pattern, email)

    # Return the valid email
    return email


def password_valid_check(password, terminal_message) -> str:
    '''
    Validates the syntax of a password by checking its length.
    If the provided password is invalid, repeatedly prompts the user for a valid password.
    
    Args:
        password (str): The initial password to validate.
        terminal_message (str): The prompt message displayed when asking for a new password input.

    Returns:
        str: A valid password entered by the user.
    '''

    # Loop until valid password is entered
    while len(password) <= 0:
        print("Password is of invalid length. Try again")
        password = input(terminal_message)
    
    # Return the valid password
    return password