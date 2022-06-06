import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import messagebox

with open('config.json') as json_file:
    config = json.load(json_file)


def receive():
    while True:
        try:
            msg = CLIENT.recv(BUFSIZE).decode("utf8")
            n = 60
            for i in range(0, len(msg), 60):
                msg_list.insert(tk.END, msg[i:(i + n)])
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    # Czyszczenie pola wprowadzania wiadomości
    my_msg.set('')
    CLIENT.send(bytes(msg, 'utf8'))


def on_closing(event=None):
    if messagebox.askokcancel('Quit', 'Czy chcesz zakończyć?'):
        my_msg.set('{quit}')
        send()
        CLIENT.close()
        main_window.quit()


main_window = tk.Tk()
main_window.title('Chat')
main_window.geometry('450x450')
main_window.resizable(False, False)

main_window.option_add('*Font', '{Calibri} 10')
main_window.option_add('*Background', 'white')

# pole tekstowe do wprowadzania wiadomości
message_frame = tk.Frame(main_window)
my_msg = tk.StringVar()
scrollbar = tk.Scrollbar(message_frame)

msg_list = tk.Listbox(message_frame, height=20, width=60, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
message_frame.pack()

entry_field = tk.Entry(main_window, width=62, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(main_window, text="Wyślij", width=15, command=send)
send_button.pack()

main_window.protocol("WM_DELETE_WINDOW", on_closing)

HOST = config['ip']
PORT = config['port']
BUFSIZE = 1024
ADDR = (HOST, PORT)

CLIENT = socket(AF_INET, SOCK_STREAM)
CLIENT.connect(ADDR)

RECEIVE_THREAD = Thread(target=receive)
RECEIVE_THREAD.start()

main_window.mainloop()
