import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import csv
import textwrap
import re

class ThirukuralChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thirukural Chatbot")
        self.root.configure(bg='Blue')  # Set background color

        self.setup_styles()
        self.create_widgets()

        # Load Thirukural data
        self.verse_data = self.read_verse_data('C:\\Users\\svani\\Downloads\\archive (1)\\new_data_thirukural')

    def setup_styles(self):
        self.root.style = ttk.Style()
        self.root.style.configure('TFrame', background='blue')
        self.root.style.configure('Heading.TLabel', font=('Helvetica', 16, 'bold'), foreground='black')  # Set heading style
        self.root.style.configure('NormalText.TLabel', font=('Helvetica', 12), foreground='#333333')  # Set normal text style

    def create_widgets(self):
        # Text widget for chat history
        self.chat_history = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20, bg='skyblue', font=('Helvetica', 12))
        self.chat_history.pack(padx=10, pady=10)

        # Entry widget for user input
        self.user_input_entry = tk.Entry(self.root, width=40, font=('Helvetica', 12))
        self.user_input_entry.pack(padx=10, pady=10)

        # Button to submit user input
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.process_user_input, style='TButton')
        self.submit_button.pack(padx=10, pady=10)

    def read_verse_data(self, csv_file):
        verse_data = {}
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                verse_id = row['id'].lower()
                verse_data[verse_id] = {
                    'ChapterName': row['Chapter Name'],
                    'Verse': row['Verse'],
                    'Translation': row['Translation'],
                    'Explanation': row['Explanation']
                }
        return verse_data

    def clean_and_wrap(self, text):
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        return textwrap.fill(cleaned_text, width=40)

    def print_aligned(self, title, text, style='Heading.TLabel'):
        self.chat_history.insert(tk.END, f"{title}:\n", style)
        for line in textwrap.wrap(text, width=40):
            self.chat_history.insert(tk.END, f"{line}\n", 'NormalText.TLabel')

    def process_user_input(self):
        user_input = self.user_input_entry.get().lower()

        if user_input == 'exit':
            self.chat_history.insert(tk.END, "Chatbot: Exiting. Goodbye!\n", 'Heading.TLabel')
            self.root.destroy()
        elif user_input in self.verse_data:
            verse_info = self.verse_data[user_input]

            self.chat_history.insert(tk.END, "\nChatbot:\n", 'Heading.TLabel')
            self.print_aligned("Chapter Name", verse_info['ChapterName'])
            if 'Verse' in verse_info:
                self.print_aligned("Verse", self.clean_and_wrap(verse_info['Verse']))
            if 'Translation' in verse_info:
                self.print_aligned("Translation", self.clean_and_wrap(verse_info['Translation']))
            if 'Explanation' in verse_info:
                self.print_aligned("Explanation", self.clean_and_wrap(verse_info['Explanation']))
        else:
            self.chat_history.insert(tk.END, "Chatbot: I'm sorry, the provided ID was not found in the CSV file.\n", 'Heading.TLabel')

        # Clear user input entry
        self.user_input_entry.delete(0, 'end')  # Use 'end' instead of tk.END

if __name__ == "__main__":
    root = tk.Tk()
    app = ThirukuralChatbotApp(root)
    root.mainloop()
