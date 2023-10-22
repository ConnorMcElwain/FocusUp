import os
import platform
import ctypes
import sys

while True:  # Program loop
    # Check if the program is running with administrative privileges
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    # Request administrative privileges if not already running as admin
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # Predefined list of websites
    website_list = [
        "www.twitch.tv", "www.youtube.com", "www.x.com", "www.discord.com", "www.store.steampowered.com", "www.battle.net"
    ]

    # Get the system's host file path
    if platform.system() == "Windows":
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
    else:
        print("This script is for Windows only.")
        exit()

    # Function to check if a website is already blocked
    def is_website_blocked(website):
        with open(host_file_path, "r") as file:
            content = file.read()
            return f"127.0.0.1 {website}" in content

    # Function to block websites
    def block_websites(websites_to_block):
        blocked_websites = []
        with open(host_file_path, "r") as file:
            content = file.read()
            for website in websites_to_block:
                if not is_website_blocked(website):
                    blocked_websites.append(website)
                    content += f"\n127.0.0.1 {website}"
            if blocked_websites:
                with open(host_file_path, "w") as file:
                    file.write(content)
                print("Blocked websites: ", blocked_websites)
            return blocked_websites

    # Function to unblock all websites with administrative privileges
    def unblock_all_websites():
        with open(host_file_path, "r") as file:
            lines = file.readlines()
        with open(host_file_path, "w") as file:
            websites_unblocked = False  # Flag to track whether websites were unblocked
            for line in lines:
                if all(website not in line for website in website_list):
                    file.write(line)
                    websites_unblocked = True  # Set the flag to True if any website is unblocked
            if websites_unblocked:
                print("All websites are unblocked.")
            else:
                print("No websites to unblock.")

    # Function to clear the terminal window
    def clear_terminal():
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    # Display the list of websites and allow the user to select which ones to block
    while True:
        clear_terminal()
        print("List of websites to block:")
        for index, website in enumerate(website_list, start=1):
            print(f"{index}. {website}")

        selected_websites = []
        while True:
            try:
                choice = input("Enter the number of the website to block (0 to apply blocked sites, -1 to unblock all, 'exit' to close program): ")
                if choice == '0':
                    if selected_websites:
                        print("Blocking selected websites...")
                        blocked_websites = block_websites(selected_websites)
                        if blocked_websites:
                            print("Websites are blocked. To unblock them, run the program again and select 'unblock'.")
                        selected_websites = []
                    input("Press Enter to continue...")
                    break
                elif choice == '-1':
                    unblock_all_websites()
                    selected_websites = []  # Clear the list of selected websites
                elif choice.lower() == 'exit':
                    break
                elif choice.isdigit() and 1 <= int(choice) <= len(website_list):
                    selected_website = website_list[int(choice) - 1]
                    if not is_website_blocked(selected_website):
                        selected_websites.append(selected_website)
                    else:
                        print(f"{selected_website} is already blocked. Please select another option.")
                else:
                    print("Invalid choice. Please enter a valid number or type 'exit'.")
            except ValueError:
                print("Invalid input. Please enter a number or type 'exit'.")
        if choice == 'exit':
            break  # Exit the program loop

    # Display the notification message when a blocked website is accessed
    notification_message = "Hey! Focus up and get back to work."
    user_input = input("Press Enter to continue or type 'exit' again to close the program: ")
    if user_input.lower() == 'exit':
        break  # Exit the program loop
