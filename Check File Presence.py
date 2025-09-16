import os
import datetime
import ctypes

def check_files_in_directory(directory):
    today = datetime.datetime.now().date()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            if file_mod_time == today:
                return True
    return False

def show_popup(message):
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    ctypes.windll.user32.MessageBoxW(0, message, "Dateiüberprüfung", 1)

def main():
    directory1 = r'Name'
    directory2 = r'Name'

    dir1_has_file = check_files_in_directory(directory1)
    dir2_has_file = check_files_in_directory(directory2)

    if not dir1_has_file or not dir2_has_file:
        message = ""
        if not dir1_has_file:
            message += f"In {directory1} wurde heute keine Datei abgelegt.\n"
        if not dir2_has_file:
            message += f"In {directory2} wurde heute keine Datei abgelegt.\n"
        show_popup(message)
    else:
        print("In beiden Verzeichnissen wurde heute eine Datei abgelegt. Alles i.O.")

    input("Enter drücken um zu schließen")

if __name__ == "__main__":
    main()
