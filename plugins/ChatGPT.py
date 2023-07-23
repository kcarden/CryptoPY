import tkinter as tk

def run_plugin(root):
    # Function to close the plugin window
    def close_plugin_window():
        plugin_window.destroy()

    # Create the plugin window
    plugin_window = tk.Toplevel(root)
    plugin_window.title("ChatGPT Plugin")
    plugin_window.geometry("400x200")

    # Create and configure the label for "Connect to ChatGPT?"
    label = tk.Label(plugin_window, text="Connect to ChatGPT?", font=("Arial", 16))
    label.pack(pady=20)

    # Function to start a new chat with ChatGPT
    def start_chat():
        # Your code to start a chat with ChatGPT goes here
        pass

    # Function to close the plugin window and do nothing
    def close_plugin():
        plugin_window.destroy()

    # Create buttons for "Yes" and "No"
    btn_yes = tk.Button(plugin_window, text="Yes", command=start_chat)
    btn_yes.pack(side=tk.LEFT, padx=10)
    btn_no = tk.Button(plugin_window, text="No", command=close_plugin)
    btn_no.pack(side=tk.LEFT, padx=10)
