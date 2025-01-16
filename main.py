import tkinter as tk
from tkinter import scrolledtext, ttk
from ollama import chat, pull
from discordrpc.utils import timestamp
import threading
import itertools
import time
import discordrpc

BG_COLOR = '#5AAA8C'
TEXT_INPUT_BG = '#478A71'
BUTTON_BG = '#3E7963'
FONT = ("Arial", 12)
loading_signal = threading.Event()
rpc = discordrpc.RPC(app_id=1329351249493098566)

MODEL_MAPPING = {
    "Tiny (2gb ram)": "qwen:0.5b",
    "Small (4gb ram)": "qwen:1.8b",
    "Medium (8gb ram)": "qwen:4b",
    "Large (16gb ram)": "qwen:7b",
    "Gigantic (24gb ram)": "qwen:14b"
}

current_mode = "Summarize Text"
system_message = "Summarize the following text:"

def discord_RPC():
    while True:
        
        rpc.set_activity(
            state="CAIT",
            details="CAIT - cool AI toolset",
            ts_start=timestamp,
            ts_end=1752426021,
            large_image="cait",
            large_text="cait",
            act_type=0,
        )
        time.sleep(1)

def switch_mode(event=None):
    """Update the GUI based on the selected mode."""
    global current_mode, system_message

    current_mode = mode_selector.get()
    text_input.delete("1.0", tk.END)
    text_output.delete("1.0", tk.END)
    loading_label.config(text="")

    if current_mode == "Summarize Text":
        system_message = "Summarize the following text:"
        label_input.config(text="Enter Text to Summarize:")
        summarize_button.config(text="Summarize", command=summarize_text)
    elif current_mode == "Analyze TOS":
        system_message = (
            "Analyze the following Terms of Service. "
            "Identify key clauses, risks, pros/cons, and potential red flags in deep detail:"
        )
        label_input.config(text="Enter Terms of Service:")
        summarize_button.config(text="Analyze", command=analyze_tos)
    elif current_mode == "Analyze Data":
        system_message = ""
        label_input.config(text="Enter Task for Data Analysis:")
        summarize_button.config(text="Set Task", command=set_analysis_task)


def set_analysis_task():
    """Set the task for data analysis."""
    global system_message
    task = text_input.get("1.0", tk.END).strip()

    if not task:
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "Please specify the task for data analysis.")
        return

    system_message = f"Perform the following task on the provided data: {task}"
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Task set. Now enter the data for analysis and click 'Analyze'.")
    text_input.delete("1.0", tk.END)
    label_input.config(text="Enter Data for Analysis:")
    summarize_button.config(text="Analyze", command=analyze_data)


def process_input(action):
    """Process input and start the specified action."""
    input_text = text_input.get("1.0", tk.END).strip()
    text_output.delete("1.0", tk.END)

    if not input_text:
        text_output.insert(tk.END, "Please enter valid input.")
        return

    selected_size = size_selector.get()
    if not selected_size:
        text_output.insert(tk.END, "Please select a model size.")
        return

    model = MODEL_MAPPING.get(selected_size)
    if not model:
        text_output.insert(tk.END, "Invalid model selection.")
        return

    loading_signal.clear()
    threading.Thread(target=loading_animation).start()
    threading.Thread(target=action, args=(input_text, model)).start()


def summarize_text():
    """Summarize the provided text."""
    process_input(lambda input_text, model: prepare_and_run(input_text, model, chat_summarizer))


def analyze_tos():
    """Analyze the provided Terms of Service."""
    process_input(lambda input_text, model: prepare_and_run(input_text, model, chat_summarizer))


def analyze_data():
    """Analyze data based on the task."""
    process_input(lambda input_text, model: prepare_and_run(input_text, model, chat_summarizer))


def prepare_and_run(input_text, model, action):
    """Prepare the model and run the action."""
    try:
        loading_label.config(text=f"Downloading: {model}")
        pull(model=model)
        action(input_text, model)
    except Exception as e:
        loading_signal.set()
        text_output.insert(tk.END, f"Error downloading model: {e}")


def chat_summarizer(input_text, model):
    """Send text to the AI for summarization or analysis."""
    try:
        stream = chat(
            model=model,
            messages=[{'role': 'user', 'content': f"{system_message}\n\n{input_text}"}],
            stream=True
        )
        for chunk in stream:
            text_output.insert(tk.END, chunk['message']['content'])
            text_output.yview(tk.END)
            time.sleep(0.05)
        loading_signal.set()
    except Exception as e:
        loading_signal.set()
        text_output.insert(tk.END, f"Error: {e}")


def loading_animation():
    """Show a loading animation while processing."""
    spinner = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    while not loading_signal.is_set():
        loading_label.config(text=f"Processing {next(spinner)}")
        time.sleep(0.1)
    loading_label.config(text="")


def setup_gui():

    """Set up the main GUI layout."""
    root = tk.Tk()
    root.title("CAIT - cool AI toolset")
    root.geometry("600x600")
    root.configure(bg=BG_COLOR)

    global mode_selector, label_input, text_input, size_selector, summarize_button, loading_label, text_output

    mode_selector = ttk.Combobox(root, font=("Arial", 10), state="readonly", width=30)
    mode_selector['values'] = ["Summarize Text", "Analyze TOS", "Analyze Data"]
    mode_selector.current(0)
    mode_selector.bind("<<ComboboxSelected>>", switch_mode)
    mode_selector.pack(pady=10)

    label_input = tk.Label(root, text="Enter Text to Summarize:", font=FONT, bg=BG_COLOR)
    label_input.pack(pady=5)

    text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70, font=("Arial", 10), bg=TEXT_INPUT_BG)
    text_input.pack(pady=10)

    size_frame = tk.Frame(root, bg=BG_COLOR)
    size_frame.pack(pady=5)

    tk.Label(size_frame, text="Select Model Size:", font=FONT, bg=BG_COLOR).grid(row=0, column=0, padx=5)
    size_selector = ttk.Combobox(size_frame, font=("Arial", 10), state="readonly", width=30)
    size_selector['values'] = list(MODEL_MAPPING.keys())
    size_selector.grid(row=0, column=1, padx=5)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=5)

    summarize_button = tk.Button(button_frame, text="Summarize", font=FONT, bg=BUTTON_BG, command=summarize_text)
    summarize_button.grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Clear", font=FONT, bg=BUTTON_BG, command=lambda: text_input.delete("1.0", tk.END)).grid(row=0, column=1, padx=5)

    loading_label = tk.Label(root, text="", font=FONT, bg=BG_COLOR, fg="white")
    loading_label.pack(pady=5)

    tk.Label(root, text="Output:", font=FONT, bg=BG_COLOR).pack(pady=5)
    text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70, font=("Arial", 10), bg=TEXT_INPUT_BG)
    text_output.pack(pady=10)

    thread = threading.Thread(target=discord_RPC)
    thread.daemon = True
    thread.start()

    return root


if __name__ == "__main__":
    app = setup_gui()
    app.mainloop()
