import os
import re
import shutil
import sys
import csv
import threading
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import webbrowser
import data_parser

from flask import Flask

import constants
from modules.StdRedirector import StdRedirector
from views.api import api

app = Flask(__name__)

gl_ip = ''
gl_port = 0


def check_ip(ip_address: str):
    if re.search(constants.ip_port_regex, ip_address):
        return True
    elif ip_address.split(":")[0] == 'localhost' and ip_address.split(":")[1] is not None:
        return True
    else:
        return False


def launch_app():
    app.debug = False
    app.register_blueprint(api)
    app.run(host='localhost', port=gl_port)


def open_browser():
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    url = 'http://' + gl_ip + ":" + str(gl_port)
    webbrowser.get(chrome_path).open(url)


def get_ip():
    ip: str = ip_entry.get()
    if check_ip(ip):
        global gl_ip
        global gl_port
        gl_ip, gl_port = ip.split(sep=":")
        ip_entry.config(state=tk.DISABLED)
        ip_button.config(state=tk.DISABLED)
        ip_browser_button.config(state=tk.NORMAL)
        flt.start()  # Фоновый процесс
    else:
        mb.showerror('Error', 'Your ip address is incorrect')
    return


def draw_lists():
    data_dir = os.listdir('data')
    indexes_listbox.config(state=tk.NORMAL)
    files_listbox.delete(0, tk.END)
    indexes_listbox.delete(0, tk.END)
    for file in data_dir:
        files_listbox.insert(tk.END, file)
    for filename in constants.filenames:
        indexes_listbox.insert(tk.END, filename)
    indexes_listbox.config(state=tk.DISABLED)


def add_file():
    files = get_files_to_path()
    try:
        if len(files) != 0:
            with open('filenames.csv', "r+") as filenames:
                for key, value in files.items():
                    shutil.copy(value, os.path.dirname(os.path.realpath(__file__)) + "/data/" + str(key) + ".xlsx")
                    filenames_list = filenames.read().rstrip().split(sep=',')
                    if str(key) in filenames_list:
                        print('Got it')
                        break
                    else:
                        filenames_list.append(str(key))
                        with open('filenames.csv', "w") as filetowrite:
                            filenames_factor = ','.join(filenames_list) + '\n'
                            filetowrite.write(filenames_factor)
                            filetowrite.close()
                            print('Added new file: ' + str(key) + '.xlsx')
                            break
        else:
            print("No suitable files found")
        filenames.close()
        data_parser.toReload = True
        constants.rescan_filenames()
        draw_lists()
        mb.showwarning('New file', 'A new file(s) has been added, if web app is opened, refresh the page.')
    except UnboundLocalError:
        pass


def get_files_to_path():
    files_to_add = fd.askopenfilenames()
    filenames_to_path = dict()
    if files_to_add:
        for file in files_to_add:
            filename_with_extenstion = os.path.basename(file)
            if filename_with_extenstion.split('.')[1] == 'xlsx':
                filenames_to_path[filename_with_extenstion.split('.')[0]] = file
            else:
                print("File " + filename_with_extenstion + " is not an xlsx table")
                pass
        return filenames_to_path
    return list()


def get_selected_file_in_filebox():
    try:
        file_to_remove = files_listbox.get(files_listbox.curselection())
    except Exception:
        print("You must select file to remove")
        return
    return file_to_remove


def remove_factor_from_listbox(factor):
    with open('filenames.csv', 'r') as file:
        filenames_factor = file.read().rstrip().split(sep=',')
        try:
            filenames_factor.remove(factor)
        except ValueError:
            mb.showerror(message='Factor is not found')
            return

    with open('filenames.csv', 'w') as filetowrite:
        filenames_factor = ','.join(filenames_factor) + '\n'
        filetowrite.write(filenames_factor)
    return filenames_factor


def remove_file():
    file = get_selected_file_in_filebox()
    if file is None:
        mb.showerror('Error', 'Select file to remove')
        return
    else:
        file_path = 'data/' + file
        answer = mb.askyesno("Delete file", 'Are you sure you want to delete: ' + file)
        if answer:
            os.remove(file_path)
            remove_factor_from_listbox(file.rstrip('.xlsx'))
            constants.rescan_filenames()
            draw_lists()
            print('File removed: ' + file)
            mb.showwarning('Removed file', 'A file has been removed, if web app is opened, refresh the page.')
        else:
            return
    pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Correlation analysis")

    main_canvas = tk.Canvas(root, width=700, height=400)
    main_canvas.pack()

    top_frame = tk.Frame(main_canvas)
    top_frame.pack(side='top')

    bottom_frame = tk.Frame(main_canvas)
    bottom_frame.pack(side='bottom')

    ip_frame = tk.Frame(top_frame)
    ip_frame.pack(side='left')

    lists_frame = tk.Frame(top_frame)
    lists_frame.pack(side='right')

    logs_frame = tk.Frame(bottom_frame)
    logs_frame.pack(side='bottom')

    logs_label = tk.Label(bottom_frame, text='Application logs:')
    logs_label.pack(side='left')
    logs_scroll = tk.Scrollbar(logs_frame)
    logs_text = tk.Text(logs_frame)
    logs_scroll.config(command=logs_text.yview)
    logs_text.config(yscrollcommand=logs_scroll.set)
    logs_scroll.pack(side='right')
    logs_text.pack(side='left')

    files_listbox = tk.Listbox(lists_frame)
    files_listbox.pack(side='left')

    indexes_listbox = tk.Listbox(lists_frame)
    indexes_listbox.pack(side='left')

    files_label = tk.Label(top_frame, text='Files and indexes')
    files_label.pack(side='top', pady=15)
    add_button = tk.Button(top_frame, text='Add file', command=add_file)  # add file function
    add_button.pack(side='top', pady=15)
    remove_button = tk.Button(top_frame, text='Remove file', command=remove_file)  # add file function
    remove_button.pack(side='top', pady=15)

    draw_lists()

    ip_entry = tk.Entry(ip_frame)
    ip_entry.insert(tk.END, 'localhost:8052')
    ip_entry.pack(side='top')

    ip_label = tk.Label(ip_frame, text='Enter desired Ip address to run')
    ip_label.pack(side='top')

    ip_button = tk.Button(ip_frame, text='Start', command=get_ip)
    ip_button.pack(side='left')
    ip_browser_button = tk.Button(ip_frame, command=open_browser, text='Open in default browser')
    ip_browser_button.pack(side='right')
    ip_browser_button.config(state=tk.DISABLED)

    sys.stdout = StdRedirector(logs_text)  # Запись логов из консоли в tk.text
    sys.stderr = StdRedirector(logs_text)  # Запись ошибок из консоли в tk.text

    flt = threading.Thread(target=launch_app)
    flt.daemon = True

    root.mainloop()  # Основной поток
