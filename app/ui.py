# Colors and fonts for interface
BLUE = '\033[34m'
RED = '\033[31m'
YELLOW = '\033[33m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_start_page() -> None:
    """
    Print the start page for Rahem's Login Simulator.
    """

    # Command list for user to interact with
    commands = [
        f"{BLUE}================================================{RESET}",
        f"            {BOLD}Rahem's Login Simulator{RESET}",
        f"{BLUE}================================================{RESET}",
        f"",
        f"Enter your account information below.",
        f"",
        f"Commands:",
        f"  {RED}-{RESET} {YELLOW}New Account{RESET}       : Register a new account",
        f"  {RED}-{RESET} {YELLOW}Forgot Password{RESET}   : Reset your password",
        f"  {RED}-{RESET} {YELLOW}Login{RESET}             : Login to your account",
        f"  {RED}-{RESET} {YELLOW}Quit{RESET}              : Exit the program",
        f"  {RED}-{RESET} {YELLOW}Help{RESET}              : Show command list again",
    ]

    print("\n".join(commands))


def print_logged_in_page():
    """
    Print the logged in page for Rahem's Login Simulator.
    """

    # Command list for user to interact with
    commands = [
        f"{BLUE}================================================{RESET}",
        f"            {BOLD}Rahem's Login Simulator{RESET}",
        f"{BLUE}================================================{RESET}",
        f"",
        f"You have successfully logged in!",
        f"",
        f"Commands:",
        f"  {RED}-{RESET} {YELLOW}Update Password{RESET}           : Change your password",
        f"  {RED}-{RESET} {YELLOW}Change Email{RESET}              : Change your email",
        f"  {RED}-{RESET} {YELLOW}Delete Account{RESET}            : Delete your account",
        f"  {RED}-{RESET} {YELLOW}2FA{RESET}                       : Enable 2 Factor Authentication",
        f"  {RED}-{RESET} {YELLOW}Logout{RESET}                    : Log out of account",
        f"  {RED}-{RESET} {YELLOW}Quit{RESET}                      : Exit the program",
        f"  {RED}-{RESET} {YELLOW}Help{RESET}                      : Show command list again",
    ]

    print("\n".join(commands))
