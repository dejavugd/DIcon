import icoextract, pkg_resources
import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk, Image
import os, locale, ctypes
from functools import lru_cache

Patch = os.getcwd()
locale.getdefaultlocale()
windll = ctypes.windll.kernel32
language = locale.windows_locale[windll.GetUserDefaultUILanguage()]

if 'ru_RU' == language:
    placeholder_text_file = 'Укажите путь сохранения файла.'
    text_exe = "Укажите путь к файлу '.exe'"
    placeholder_text_folder = 'Укажите папку в которую сохранить.'
else:
    placeholder_text_file = 'Specify the path to save the file'
    text_exe = "Specify the path to the '.exe' file"
    placeholder_text_folder = 'Specify the folder to save it to.'

@lru_cache(maxsize=None)
def find_exe_files(file_patch, output_patch):
    exe_files = []
    if output_patch != '':
        pass
    else:
        output_patch = f"{Patch}"
    if file_patch.endswith('.exe'):
        exe_files.append(os.path.join(file_patch))
        print(file_patch)
        print(output_patch)
        name, _ = file_patch.split(".exe")
        path, name = os.path.split(name)
        extractor = icoextract.IconExtractor(f"{file_patch}")
        print(name)
        try:
            file = extractor.export_icon(f"{output_patch}\\{name}.ico")
            # Write the BytesIO content to a file
        except Exception as e:
            print(f"Error: {e}")

def find_patch(entry):
    global Patch
    file_path = ctk.filedialog.askopenfilename(initialdir=Patch, filetypes=[("Exe files", "*.exe"), ("Files", "*.*")])
    if (file_path != "") and (entry.get() != ""):
        entry.delete(0, len(entry.get()))
        entry.insert(1, file_path)
    elif file_path != "":
        entry.insert(1, file_path)
    else:
        pass

def save_patch(entry, event):
    global Patch
    if event == "folder":
        save_path = ctk.filedialog.askdirectory(initialdir=Patch)
        if (save_path != "") and (entry.get() != ""):
            entry.delete(0, len(entry.get()))
            entry.insert(1, save_path)
        else:
            entry.insert(1, save_path)
    else:
        save_path = ctk.filedialog.asksaveasfilename(initialdir=Patch, filetypes=[("Icon files", "*.ico"), ("Files", "*.*")])
        if (save_path != "") and (entry.get() != ""):
            entry.delete(0, len(entry.get()))
            entry.insert(1, save_path)
        else:
            entry.insert(1, save_path)


def replace_holder(event, entry):
    global output_files
    if entry == "folder":
        output_files.configure(placeholder_text=placeholder_text_folder)
    else:
        output_files.configure(placeholder_text=placeholder_text_file)

ctk.set_appearance_mode("dark")
filename = "red.json"
favicon = pkg_resources.resource_filename(__name__, filename)
ctk.set_default_color_theme(favicon)
root = ctk.CTk()
root.geometry("400x400")
root.title("DIcon")

filename = "Dejavu.ico"
favicon = pkg_resources.resource_filename(__name__, filename)
# favicon = Image.open("patern.jpg")
root.iconbitmap(favicon)

filename = "patern.jpg"
favicon = pkg_resources.resource_filename(__name__, filename)
patern = ImageTk.PhotoImage(Image.open(favicon))
label_background = ctk.CTkLabel(root, text=None, image=patern, width=400, height=400, bg_color="transparent", corner_radius=20)
label_background.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

frame = ctk.CTkFrame(label_background, width=300, height=300, corner_radius=10, bg_color="transparent")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

label = ctk.CTkLabel(frame, text="Icon Extractor", font=("Neuropol Medium", 16))
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

patch_files = ctk.CTkEntry(frame, corner_radius=5, placeholder_text=text_exe, width=200)
patch_files.grid(row=1, column=0, padx=10, pady=10)

filename = "quit-noactive.png"
favicon = pkg_resources.resource_filename(__name__, filename)
button_image = ctk.CTkImage(Image.open(favicon))
button_files = ctk.CTkButton(frame, corner_radius=5, command = lambda entry=patch_files: find_patch(entry=entry), image=button_image, text=None, width=40)
button_files.grid(row=1, column=1, padx=10, pady=10)

global output_files
output_files = ctk.CTkEntry(frame, corner_radius=5, placeholder_text=placeholder_text_file, font=("Arial", 12), width=200)

radion_var = ctk.StringVar(value="file")
radion_button = ctk.CTkRadioButton(frame, text="Folder", variable=radion_var, value='folder')
radion_button.grid(row=2, column=0, padx=10, pady=10)
radion_button.bind('<Button-1>', command=lambda event: replace_holder(event, entry=radion_var.get()))

radion_button2 = ctk.CTkRadioButton(frame, text="File", variable=radion_var, value='file')
radion_button2.grid(row=2, column=1, padx=10, pady=10)
radion_button2.bind('<Button-1>', command=lambda event: replace_holder(event, entry=radion_var.get()))


output_files.grid(row=3, column=0, padx=10, pady=10)

filename = "quit-noactive.png"
favicon = pkg_resources.resource_filename(__name__, filename)
button_image = ctk.CTkImage(Image.open(favicon))
button_files = ctk.CTkButton(frame, corner_radius=5, command=lambda entry=output_files: save_patch(entry=entry, event=radion_var.get()), image=button_image, text=None, width=40)
button_files.grid(row=3, column=1, padx=10, pady=10)

filename = "save-noactive.png"
favicon = pkg_resources.resource_filename(__name__, filename)
button_image = ctk.CTkImage(Image.open(favicon))
extract_button = ctk.CTkButton(frame, corner_radius=5, command=lambda : find_exe_files(file_patch=patch_files.get(), output_patch=output_files.get()), image=button_image, text=None, width=40)
extract_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
