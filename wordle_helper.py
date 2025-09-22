import tkinter as tk
import re

with open("words.txt") as txt:
    words = txt.read().split("\n")

def get_possible(chars_matrix, colors_matrix):
    possible = []
    black_char = set()
    yellow_index = [[], [], [], [], []]
    green_index = ["", "", "", "", ""]
    for chars, colors in zip(chars_matrix, colors_matrix):
        for i, char_color in enumerate(zip(chars, colors)):
            char, color = char_color
            if color == "B":
                black_char.add(char)
            elif color == "Y":
                yellow_index[i].append(char)
            elif color == "G":
                green_index[i] = char

    in_chars = set(
    [item for sublist in yellow_index for item in sublist if item] + [item for item in green_index if item]
)

    word_reg = r""
    for i,g_y in enumerate(zip(green_index, yellow_index)):
        g,y = g_y
        if g != "":
            word_reg += g
        elif y != []:
            word_reg += f'[^{"".join(y)}]'
        else:
            word_reg += "[a-z]"
    word_reg = re.compile(word_reg)

    for word in words:
        for b_c in black_char - in_chars:
            if b_c in word:
                break
        else:
            for i_c in in_chars:
                if i_c not in word:
                    break
            else:
                if word_reg.match(word):
                    possible.append(word)

    return possible

class WordleCell(tk.Label):
    def __init__(self, master, row, col, gui):
        super().__init__(
            master,
            width=2,
            height=1,
            font=("Arial", 24, "bold"),
            relief="solid",
            bd=2,
            bg="black",
            fg="white",
            anchor="center"
        )
        self.grid(row=row, column=col, padx=5, pady=5)
        self.state = "B"
        self.char = ""
        self.row = row
        self.col = col
        self.gui = gui

        # Mouse toggles color
        self.bind("<Button-1>", self.activate, add="+")

    def toggle_color(self, event=None):
        if self.state == "B":
            self.state = "Y"
            self.config(bg="yellow", fg="black")
        elif self.state == "Y":
            self.state = "G"
            self.config(bg="green", fg="white")
        else:
            self.state = "B"
            self.config(bg="black", fg="white")

    def set_char(self, char):
        self.char = char.upper()
        self.config(text=self.char)

    def clear_char(self):
        self.char = ""
        self.config(text="")

    def get_letter(self):
        return self.char.lower() if self.char else " "

    def get_color(self):
        return self.state

    def activate(self, event=None):
        self.gui.current_row = self.row
        self.gui.current_col = self.col
        self.toggle_color() 
class WordleGUI:
    def __init__(self, root, max_rows=6):
        self.root = root
        self.root.title("Wordle Helper")

        self.rows = []
        self.max_rows = max_rows

        # Build grid
        for r in range(max_rows):
            row_cells = []
            for c in range(5):
                cell = WordleCell(root, r, c, self)
                row_cells.append(cell)
            self.rows.append(row_cells)

        # Submit button
        self.submit_btn = tk.Button(root, text="Submit", command=self.submit)
        self.submit_btn.grid(row=max_rows, column=0, columnspan=5, pady=10)

        # Scrollable results
        self.result_frame = tk.Frame(root)
        self.result_frame.grid(row=max_rows + 1, column=0, columnspan=5, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.result_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.result_list = tk.Listbox(
            self.result_frame,
            yscrollcommand=self.scrollbar.set,
            font=("Consolas", 14),
            height=10,
            width=20
        )
        self.result_list.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.result_list.yview)

        # Track typing position
        self.current_row = 0
        self.current_col = 0

        # Key bindings (global)
        root.bind("<Key>", self.key_handler)

    def key_handler(self, event):
        if event.keysym == "BackSpace":
            if self.current_col > 0:
                self.current_col -= 1
                self.rows[self.current_row][self.current_col].clear_char()
                
        elif event.char.isalpha() and len(event.char) == 1:
            if self.current_col < 5:
                self.rows[self.current_row][self.current_col].set_char(event.char)
                self.current_col += 1
        elif event.keysym == "Return":  # Enter = next row
            if self.current_row < self.max_rows - 1:
                self.current_row += 1
                self.current_col = 0
        elif event.char == " ":
            self.submit()

    def submit(self):
        chars_matrix = []
        colors_matrix = []

        for row in self.rows:
            word = "".join(cell.get_letter() for cell in row)
            colors = "".join(cell.get_color() for cell in row)
            if word.strip():
                chars_matrix.append(word)
                colors_matrix.append(colors)
        # print(chars_matrix, colors_matrix)

        possible_words = get_possible(chars_matrix, colors_matrix)
        # print(possible_words)

        # Update listbox
        self.result_list.delete(0, tk.END)
        for w in possible_words:
            self.result_list.insert(tk.END, w)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()
