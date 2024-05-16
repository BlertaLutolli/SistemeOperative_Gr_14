import tkinter as tk
from multiprocessing import Process, Pipe

def run_text_window(pipe, title):
    def copy_text():
        pipe.send(text.get(1.0, tk.END))
    
    def receive_text():
        if pipe.poll():
            received_text = pipe.recv()
            text.delete(1.0, tk.END)
            text.insert(tk.END, received_text)
        root.after(100, receive_text)

    root = tk.Tk()
    root.title(title)

    text = tk.Text(root, height=10, width=40)
    text.pack(padx=10, pady=5)

    button = tk.Button(root, text="Send Text", command=copy_text)
    button.pack(pady=5)

    receive_text()
    root.mainloop()

def main():
    parent_conn1, child_conn1 = Pipe()
    parent_conn2, child_conn2 = Pipe()

    p1 = Process(target=run_text_window, args=(child_conn1, "Window 1"))
    p2 = Process(target=run_text_window, args=(child_conn2, "Window 2"))

    p1.start()
    p2.start()

    def forward_message(pipe1, pipe2):
        if pipe1.poll():
            message = pipe1.recv()
            pipe2.send(message)
    
    try:
        while True:
            forward_message(parent_conn1, parent_conn2)
            forward_message(parent_conn2, parent_conn1)
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()

if __name__ == "__main__":
    main()
