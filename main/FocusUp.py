import os
import platform
import ctypes
import sys

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
                if website == "www.x.com":
                    content += f"\n127.0.0.1 www.twitter.com"  # Block twitter.com when x.com is blocked
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
            blocked = False
            for website in gaming_websites + social_websites:
                if f"127.0.0.1 {website}" in line:
                    blocked = True
                    break
            if f"127.0.0.1 www.twitter.com" in line:
                blocked = True  # Ensure www.twitter.com is blocked
            if not blocked:
                file.write(line)
                websites_unblocked = True  # Set the flag to True if any website is unblocked
        if websites_unblocked:
            print("All websites are unblocked.")
        else:
            print("No websites to unblock.")

# Function to show blocked websites
def show_blocked_websites():
    blocked_sites = []

    with open(host_file_path, "r") as file:
        lines = file.readlines()
        for website in website_list:
            if any(f"127.0.0.1 {website}" in line for line in lines):
                blocked_sites.append(website)

    if blocked_sites:
        print(f"Number of Blocked websites: {len(blocked_sites)}")
        for site in blocked_sites:
            print(site)
    else:
        print("No websites are currently blocked.")

# Function to clear the terminal window
def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Define the Gaming category websites
gaming_websites = ["www.twitch.tv", "www.discord.com", "www.store.steampowered.com", "www.battle.net"]

# Define the Social category websites
social_websites = ["www.x.com", "www.youtube.com", "www.instagram.com", "www.tiktok.com"]

# Function to display category-specific websites and allow the user to select which ones to block
def select_category(category):
    selected_websites = []
    while True:
        clear_terminal()
        print(f"List of websites to block:")
        for index, website in enumerate(category, start=1):
            print(f"{index}. {website}")
        print("4. Add Custom Website")
        print("B. Back")

        try:
            choice = input("Enter the number of the website to block, '0' to apply blocked sites: ")
            if choice == '0':
                if selected_websites:
                    print("Blocking selected websites...")
                    blocked_websites = block_websites(selected_websites)
                    if blocked_websites:
                        print("Websites are blocked. To unblock them, select the 'Unblock All Websites' option.")
                    selected_websites = []
                input("Press Enter to continue...")
                break
            elif choice.lower() == '4':
                add_custom_website()
            elif choice.lower() == 'b':
                return  # Go back to the previous menu
            elif choice.isdigit() and 1 <= int(choice) <= len(category):
                selected_website = category[int(choice) - 1]
                if not is_website_blocked(selected_website):
                    selected_websites.append(selected_website)
                else:
                    print(f"{selected_website} is already blocked. Please select another option.")
            else:
                print("Invalid choice. Please enter a valid number or 'B' to go back.")
        except ValueError:
            print("Invalid input. Please enter a number or 'B' to go back.")

# Function to list all websites from different categories
def select_all_sites():
    clear_terminal()
    all_sites = gaming_websites + social_websites
    print("Main Menu:")
    print("3. All Sites")
    print("4. Add Custom Website")
    print("B. Back")

    selected_websites = []
    while True:
        try:
            choice = input("Enter the number of the website to block, '0' to apply blocked sites: ")
            if choice == '0':
                if selected_websites:
                    print("Blocking selected websites...")
                    blocked_websites = block_websites(selected_websites)
                    if blocked_websites:
                        print("Websites are blocked. To unblock them, select the 'Unblock All Websites' option.")
                    selected_websites = []
                input("Press Enter to continue...")
                break
            elif choice.lower() == '4':
                add_custom_website()
            elif choice.lower() == 'b':
                return  # Go back to the previous menu
            elif choice.isdigit() and 1 <= int(choice) <= len(all_sites):
                selected_website = all_sites[int(choice) - 1]
                if not is_website_blocked(selected_website):
                    selected_websites.append(selected_website)
                else:
                    print(f"{selected_website} is already blocked. Please select another option.")
            else:
                print("Invalid choice. Please enter a valid number or 'B' to go back.")
        except ValueError:
            print("Invalid input. Please enter a number or 'B' to go back.")

# Function for blocking websites from different categories
def block_websites_menu():
    while True:
        clear_terminal()
        print("Block Websites Menu:")
        print("1. Gaming")
        print("2. Social")
        print("3. All Sites")
        print("4. Add Custom Website")
        print("B. Back")

        choice = input("Enter your choice: ")

        if choice == '1':
            select_category(gaming_websites)
        elif choice == '2':
            select_category(social_websites)
        elif choice == '3':
            select_all_sites()
        elif choice.lower() == 'b':
            return  # Go back to the main menu
        elif choice.lower() == '4':
            add_custom_website()
        else:
            print("Invalid choice. Please enter a valid number or 'B' to go back.")

# Function to add custom websites to block
def add_custom_website():
    while True:
        clear_terminal()
        print("Add Custom Website to Block:")
        print("B. Back")

        website_to_block = input("Enter the custom website to block (e.g., example.com): ")
        if website_to_block.lower() == 'b':
            return  # Go back to the previous menu
        elif is_valid_domain(website_to_block):
            if not is_website_blocked(website_to_block):
                content = f"\n127.0.0.1 {website_to_block}"
                with open(host_file_path, "a") as file:
                    file.write(content)
                print(f"{website_to_block} is blocked.")
                input("Press Enter to continue...")
                return
            else:
                print(f"{website_to_block} is already blocked. Please select another option.")
        else:
            print("Invalid domain. Please enter a valid domain (e.g., example.com).")

# Function to check if a string is a valid domain
def is_valid_domain(domain):
    # Add your domain validation logic here
    # This is a simplified example, and you can add more checks as needed
    return '.' in domain

# Main program loop
while True:
    clear_terminal()
    print("FocusUp v0.05")
    print("Main Menu:")
    print("1. Block Websites")
    print("2. Show Blocked Websites")
    print("3. Unblock All Websites")
    print("0. Exit")

    main_choice = input("Enter your choice: ")

    if main_choice == '1':
        block_websites_menu()
    elif main_choice == '2':
        show_blocked_websites()
        input("Press Enter to continue...")
    elif main_choice == '3':
        unblock_all_websites()
        input("Press Enter to continue...")
    elif main_choice == '0':
        sys.exit()
    else:
        print("Invalid choice. Please enter a valid number.")
