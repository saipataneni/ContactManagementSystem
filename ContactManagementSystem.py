import tkinter as tk
from tkinter import filedialog, messagebox

MAX_TEXT_SIZE = 10000

class TextBuffer:
    def __init__(self):
        self.text = ""

class TextEditor:
    def __init__(self):
        self.buffer = TextBuffer()
        self.undo_stack = [TextBuffer() for _ in range(50)]
        self.redo_stack = [TextBuffer() for _ in range(50)]
        self.undo_top = -1
        self.redo_top = -1

    def init_text_editor(self):
        self.undo_top = -1
        self.redo_top = -1
        self.buffer.text = ""

    def make_change(self, new_text):
        if self.undo_top < 49:
            self.undo_top += 1
            self.undo_stack[self.undo_top].text = self.buffer.text
            self.buffer.text = new_text
            self.redo_top = -1

    def undo(self):
        if self.undo_top >= 0:
            self.redo_top += 1
            self.redo_stack[self.redo_top].text = self.buffer.text
            self.buffer.text = self.undo_stack[self.undo_top].text
            self.undo_top -= 1

    def redo(self):
        if self.redo_top >= 0:
            self.undo_top += 1
            self.undo_stack[self.undo_top].text = self.buffer.text
            self.buffer.text = self.redo_stack[self.redo_top].text
            self.redo_top -= 1

    def save_to_file(self, filename):
        try:
            with open(filename, "w") as file:
                file.write(self.buffer.text)
            return True
        except IOError:
            return False

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                self.buffer.text = file.read(MAX_TEXT_SIZE)
            self.undo_top = -1
            self.redo_top = -1
            return True
        except IOError:
            return False

class TextEditorGUI:
    def __init__(self, master):
        self.master = master
        self.editor = TextEditor()
        self.init_gui()

    def init_gui(self):
        self.master.title("Text Editor")

        self.text_area = tk.Text(self.master, wrap="word", width=80, height=20)
        self.text_area.pack(expand=tk.YES, fill=tk.BOTH)
        self.text_area.bind("<Key>", self.on_key_press)
        self.text_area.bind("<Button-1>", self.on_click)

        toolbar = tk.Frame(self.master)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.undo_button = tk.Button(toolbar, text="Undo", command=self.editor.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.redo_button = tk.Button(toolbar, text="Redo", command=self.editor.redo)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(toolbar, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.open_button = tk.Button(toolbar, text="Open", command=self.load_file)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.filename_label = tk.Label(toolbar, text="File: None")
        self.filename_label.pack(side=tk.LEFT, padx=5)

        status_bar = tk.Label(self.master, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.cursor_position_label = tk.Label(self.master, text="Cursor Position: 1, 1", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.cursor_position_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_status("Ready")

    def on_key_press(self, event):
        self.editor.make_change(self.text_area.get(1.0, tk.END))
        self.update_cursor_position()

    def on_click(self, event):
        self.update_cursor_position()

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            if self.editor.save_to_file(filename):
                self.update_status(f"Text saved to {filename}")
                self.update_filename(filename)

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            if self.editor.load_from_file(filename):
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.editor.buffer.text)
                self.update_status(f"Text loaded from {filename}")
                self.update_filename(filename)

    def update_filename(self, filename):
        self.filename_label.config(text=f"File: {filename}")

    def update_status(self, status):
        self.status_bar.config(text=f"Status: {status}")

    def update_cursor_position(self):
        cursor_position = self.text_area.index(tk.CURRENT)
        self.cursor_position_label.config(text=f"Cursor Position: {cursor_position}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = TextEditorGUI(root)
    root.mainloop()
