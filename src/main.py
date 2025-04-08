import subprocess
import os
import msvcrt

while True:
    comp_name = os.environ["COMPUTERNAME"]
    login = os.getlogin()
    cur_path = os.getcwd()

    # Display the prompt
    print(f"{login}@{comp_name}$ {cur_path} > ", end="", flush=True)

    # Collect user input character by character
    usr_cmd = ""
    while True:
        char = msvcrt.getch()  # Get a single character without requiring Enter

        # Check for Esc key (ASCII 27)
        if char == b"\x1b":  # Esc key
            print("\nExiting...")
            exit(0)

        # Check for Enter key (ASCII 13)
        elif char == b"\r":  # Enter key
            print()  # Move to next line after command
            break

        # Handle backspace (ASCII 8)
        elif char == b"\x08":  # Backspace key
            if usr_cmd:  # Only process if there's something to delete
                usr_cmd = usr_cmd[:-1]  # Remove last character
                print(
                    "\b \b", end="", flush=True
                )  # Move cursor back, overwrite with space, move back again

        # Handle printable characters
        else:
            try:
                decoded_char = char.decode("utf-8")
                usr_cmd += decoded_char
                print(decoded_char, end="", flush=True)  # Echo the character
            except UnicodeDecodeError:
                pass  # Ignore non-UTF-8 characters

    # Clean up the command input
    usr_cmd = usr_cmd.strip()

    # Split the input into command and arguments
    cmd_parts = usr_cmd.split()

    # Handle 'cd' command separately
    if cmd_parts and cmd_parts[0].lower() == "cd":
        if len(cmd_parts) > 1:
            try:
                # Change directory using os.chdir
                os.chdir(cmd_parts[1])
            except FileNotFoundError:
                print(f"Directory not found: {cmd_parts[1]}")
            except PermissionError:
                print(f"Permission denied: {cmd_parts[1]}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Please specify a directory to change to.")
    else:
        # Run other commands using subprocess
        try:
            subprocess.run(usr_cmd, shell=True)
        except Exception as e:
            print(f"Error executing command: {e}")
