# plugins/test_plugin.py
import tkinter as tk

def flashing_text(root):
    # Function to close the plugin window
    def close_plugin_window():
        plugin_window.destroy()

    # Function to update the flashing text
    def update_text():
        if text_label["foreground"] == "black":
            text_label.config(foreground="red")
        else:
            text_label.config(foreground="black")
        root.after(500, update_text)

    # Create the plugin window
    plugin_window = tk.Toplevel(root)
    plugin_window.title("Test Plugin")
    plugin_window.geometry("400x200")

    # Create and configure the text label
    text_label = tk.Label(plugin_window, text="THIS IS A TEST!", font=("Arial", 25, "bold"))
    text_label.pack(expand=True, fill=tk.BOTH)

    # Call the update_text function to start flashing the text
    update_text()

    # Add a close button to the plugin window
    close_button = tk.Button(plugin_window, text="Close Plugin", command=close_plugin_window)
    close_button.pack()
