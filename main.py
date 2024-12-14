import tkinter as tk
from tkinter import scrolledtext
from ollama import chat
from ollama import ChatResponse
import threading
import itertools
import time

BG_COLOR = '#5AAA8C'
TEXT_INPUT_BG = '#478A71'
BUTTON_BG = '#3E7963'
FONT = ("Arial", 12)

loading_signal = threading.Event()

def summarize_text():
    input_text = text_input.get("1.0", tk.END).strip()
    text_output.delete("1.0", tk.END)

    if not input_text:
        text_output.insert(tk.END, "enter text to summarize.")
        return


    loading_signal.clear()
    threading.Thread(target=loading_animation).start()

    threading.Thread(target=call_ai_summarizer, args=(input_text,)).start()

def call_ai_summarizer(input_text):
    try:
        response: ChatResponse = chat(model='qwen2:1.5b', messages=[
            {
                'role': 'user',
                'content': (
                    f"Summarize the following text into a concise and coherent summary, "
                    f"capturing the main ideas and key details. Avoid repetition, maintain a neutral tone, "
                    f"and keep it short but accurate.\n\nText: {input_text}"
                ),
            },
        ])
        summary = response.message.content
        loading_signal.set()
        text_output.insert(tk.END, summary)
    except Exception as e:
        loading_signal.set()
        text_output.insert(tk.END, f"error: {e}")

def loading_animation():
    spinner = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    while not loading_signal.is_set():
        loading_label.config(text=f"Processing {next(spinner)}")
        time.sleep(0.1)
    loading_label.config(text="")

def clear_input():
    text_input.delete("1.0", tk.END)

def setup_gui():
    root = tk.Tk()
    root.title("sumAI")
    root.geometry("600x500")
    root.configure(bg=BG_COLOR)

    label_input = tk.Label(root, text="Enter Text to Summarize:", font=FONT, bg=BG_COLOR)
    label_input.pack(pady=5)

    global text_input
    text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70, font=("Arial", 10), bg=TEXT_INPUT_BG)
    text_input.pack(pady=10)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=5)

    summarize_button = tk.Button(button_frame, text="Summarize", font=FONT, bg=BUTTON_BG, command=summarize_text)
    summarize_button.grid(row=0, column=0, padx=5)

    clear_button = tk.Button(button_frame, text="Clear", font=FONT, bg=BUTTON_BG, command=clear_input)
    clear_button.grid(row=0, column=1, padx=5)

    global loading_label
    loading_label = tk.Label(root, text="", font=FONT, bg=BG_COLOR, fg="white")
    loading_label.pack(pady=5)

    label_output = tk.Label(root, text="Summary:", font=FONT, bg=BG_COLOR)
    label_output.pack(pady=5)

    global text_output
    text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70, font=("Arial", 10), bg=TEXT_INPUT_BG)
    text_output.pack(pady=10)

    return root

if __name__ == "__main__":
    app = setup_gui()
    app.mainloop()
