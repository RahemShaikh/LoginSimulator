from ui import BLUE, RED, YELLOW, BOLD, RESET, print_start_page
from auth import create_account, log_in
from user_actions import logged_in_page, forgot_password
import sys, state

def start_page() -> None:
    """
    Displays the start page and handles user interaction until the user logs in, quits, 
    or interrupts the program (e.g., via Ctrl+C).

    Available user commands:
        - "new account": Creates a new user account.
        - "forgot password": Initiates password recovery process.
        - "login": Prompts user login and navigates to logged-in page if successful.
        - "help": Displays the start page command list again.
        - "quit": Exits the application gracefully.
    """

    print_start_page()  # Print the initial command menu

    try:
        while True:
            # Display the header
            print(f"\n{BOLD}--->>>            {RED}START PAGE{RESET}            {BOLD}<<<---{RESET}\n")
            
            # Prompt user input
            user_choice = input(">>> ").lower()

            # Handle the input using match-case
            match user_choice:

                case "new account":
                    create_account()

                case "forgot password":
                    forgot_password()

                case "login":
                    log_in()
                    if state.user is not None:
                        logged_in_page()

                case "help":
                    print_start_page()

                case "quit":
                    print("Thank you for visiting Rahem's Login Simulator")
                    print("See you soon!")
                    sys.exit()

                case _:
                    print("Invalid command")  # Handle unrecognized input

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C interruption
        print(f"\n[{RED}!{RESET}] Program interrupted with Ctrl+C. Exiting...")
        print("Thank you for visiting Rahem's Login Simulator")
        print("See you soon!")


if __name__ == "__main__":
    start_page()