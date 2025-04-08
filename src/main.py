import subprocess
import os
import msvcrt

while True:
    comp_name = os.environ["COMPUTERNAME"]
    login = os.getlogin()
    cur_path = os.getcwd()

    print(f"{login}@{comp_name}$ {cur_path} > ", end="", flush=True)

    usr_cmd = ""
    while True:
        char = msvcrt.getch()

        if char == b"\x1b":
            exit(0)

        elif char == b"\r":
            print()
            break

        elif char == b"\x08":
            if usr_cmd:
                usr_cmd = usr_cmd[:-1]
                print("\b \b", end="", flush=True)

        else:
            try:
                decoded_char = char.decode("utf-8")
                usr_cmd += decoded_char
                print(decoded_char, end="", flush=True)
            except UnicodeDecodeError:
                pass

    usr_cmd = usr_cmd.strip()

    cmd_parts = usr_cmd.split()

    if cmd_parts and cmd_parts[0].lower() == "cd":
        if len(cmd_parts) > 1:
            try:
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
        try:
            subprocess.run(["powershell.exe", "-Command", usr_cmd], shell=False)
        except Exception as e:
            print(f"Error executing command: {e}")
