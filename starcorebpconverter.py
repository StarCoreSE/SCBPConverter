import os
import re
import tkinter as tk
from tkinter import messagebox, filedialog, IntVar

def process_blueprint_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_content = re.sub(r'<SubtypeName>(.*?)_(NRG|KIN)</SubtypeName>', r'<SubtypeName>\1</SubtypeName>', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)

def convert_blueprints(check_subfolders):
    selected_folder = filedialog.askdirectory(title="Select Blueprint Folder")
    
    if not selected_folder:
        return
    
    blueprint_folders = []
    modified_subtypes = set()
    
    if check_subfolders.get():
        blueprint_folders.append(selected_folder)
        for root, dirs, files in os.walk(selected_folder):
            if any(file.lower().endswith('.sbc') for file in files):
                blueprint_folders.append(root)
    else:
        blueprint_folders = [selected_folder]
    
    modified_count = 0

    for folder in blueprint_folders:
        bp_file_path = os.path.join(folder, 'bp.sbc')
        bp_b5_file_path = os.path.join(folder, 'bp.sbcB5')
        
        if os.path.exists(bp_file_path):
            with open(bp_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if re.search(r'<SubtypeName>.*?_(NRG|KIN).*?</SubtypeName>', content):
                    process_blueprint_file(bp_file_path)
                    modified_count += 1
                    modified_subtypes.add(folder)
                    
                    if os.path.exists(bp_b5_file_path):
                        os.remove(bp_b5_file_path)

    # Show conversion summary
    if modified_count == 0:
        messagebox.showinfo("No Blueprints with KIN/NRG Found", "No KIN/NRG blueprints were detected.")
    else:
        info_text = f"Blueprint conversion completed!\n\nModified {modified_count} blueprint(s)."
        if modified_subtypes:
            info_text += f"\n\nModified subtypes in the following folders:\n\n{', '.join(modified_subtypes)}"
        messagebox.showinfo("Conversion Complete", info_text)

# Create GUI window
root = tk.Tk()
root.title("Blueprint Conversion Tool")

# Add a label
label = tk.Label(root, text="Welcome to Blueprint Conversion Tool")
label.pack()

# Show a warning about making a backup
backup_warning = tk.Label(root, text="Please make a backup of your blueprints before proceeding!", fg="red")
backup_warning.pack()

# Add a checkbox for deep folder search
check_subfolders = IntVar()
subfolder_checkbox = tk.Checkbutton(root, text="Search Subfolders", variable=check_subfolders)
subfolder_checkbox.pack()

# Add a button to trigger conversion
convert_button = tk.Button(root, text="Convert Blueprints", command=lambda: convert_blueprints(check_subfolders))
convert_button.pack()

# Start GUI main loop
root.mainloop()
