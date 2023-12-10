import os
from datetime import datetime
import markdown

PASSWORD = "password"  # use this to gain entry

def authenticate(): 
    attempts = 3
    while attempts > 0:
        password_attempt = input("Enter password: ")
        if password_attempt == PASSWORD:
            return True
        else:
            attempts -= 1
            print(f"Incorrect password. {attempts} attempts remaining.")
    
    print("Authentication failed. Exiting.")
    return False

def write_entry():
    if not authenticate():
        return

    entry_lines = []
    
    print("Write your diary entry. Enter '!done' on a new line to finish.")
    
    while True:
        line = input()
        if line == '!done':
            break
        entry_lines.append(line)

    entry = '\n'.join(entry_lines)
    #add tags and categories for easier search later
    tags = input("Enter tags (comma-separated): ").split(',')
    categories = input("Enter categories (comma-separated): ").split(',')

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"diary_{date}.txt"

    with open(filename, "w") as file:
        file.write(f"Tags: {', '.join(tags)}\n")
        file.write(f"Categories: {', '.join(categories)}\n\n")
        file.write(entry)

    print(f"Entry saved to {filename}")

def read_entries():
    if not authenticate():
        return

    entries = [file for file in os.listdir() if file.startswith("diary_") and file.endswith(".txt")]

    if entries:
        print("\n--- Your Diary Entries ---")
        for i, entry in enumerate(entries, start=1):
            print(f"{i}. {entry}")

        selected_entry = input("\nEnter the number of the entry you want to open (or press Enter to skip): ").strip()

        if selected_entry.isdigit() and 1 <= int(selected_entry) <= len(entries):
            selected_entry_name = entries[int(selected_entry) - 1]
            with open(selected_entry_name, "r") as file:
                selected_entry_content = file.read()
                
                # Check if the entry has Markdown metadata
                if selected_entry_content.startswith("Tags:") and selected_entry_content.find("\n\n") != -1:
                    metadata, content = selected_entry_content.split("\n\n", 1)
                    tags_line = metadata.split("Tags:")[1].strip()
                    tags = [tag.strip() for tag in tags_line.split(",")]
                else:
                    content = selected_entry_content
                    tags = []

                # Render Markdown content
                rendered_content = markdown.markdown(content)

                print(f"\n--- Diary Entry: {selected_entry_name} ---\nTags: {', '.join(tags)}\n\n{rendered_content}")
        elif selected_entry:
            print("Invalid entry number. Please enter a valid number.")
        
        search_term = input("\nEnter a tag or category to search for entries (or press Enter to skip): ").strip()
        
        if search_term:
            matching_entries = [entry for entry in entries if search_term.lower() in entry.lower()]
            
            if matching_entries:
                print("\n--- Matching Entries ---")
                for entry in matching_entries:
                    print(f"\n{entry}")
            else:
                print("No matching entries found.")
    else:
        print("No diary entries found.")

if __name__ == "__main__":
    while True:
        print("\n1. Write Diary Entry")
        print("2. Read Diary Entries")
        print("3. Exit")

        choice = input("Select an option (1/2/3): ")

        if choice == "1":
            write_entry()
        elif choice == "2":
            read_entries()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")
