import os
import tkinter as tk
from tkinter import filedialog, messagebox
import importlib
import markdown
from tkhtmlview import HTMLLabel
import emoji

# Function to display the content of the README.md file in the readme_text widget
def show_readme():
    readme_text.config(state=tk.NORMAL)
    readme_text.delete("1.0", tk.END)
    
    with open("README.md", "r") as f:
        readme_content = f.read()
    
    # Convert the Markdown content to HTML
    readme_html = markdown.markdown(readme_content)
    
    # Convert emoji codes to actual emojis in HTML
    readme_html = emoji.emojize(readme_html)
    
    # Insert the HTML content into the HTMLLabel
    readme_text.set_html(readme_html)
    readme_text.config(state=tk.DISABLED)
    
# Function to refresh the Available Plugins list
def refresh_plugin_list():
    # Clear the listbox
    plugin_listbox.delete(0, tk.END)

    # Load the available plugins from the "plugins" folder (excluding "__init__.py")
    plugin_folder = "plugins"
    if not os.path.exists(plugin_folder):
        os.makedirs(plugin_folder)
    for filename in os.listdir(plugin_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            plugin_name = filename[:-3]  # Get the plugin name without the ".py" extension
            plugin_listbox.insert(tk.END, plugin_name)

# Function to add a new plugin
def add_new_plugin():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if not file_path:
        return  # No file selected, do nothing

    plugin_name = os.path.basename(file_path).replace(".py", "")
    plugin_path = os.path.join("plugins", plugin_name + ".py")

    # Check if the plugin already exists
    if os.path.exists(plugin_path):
        answer = messagebox.askyesno("Plugin Exists",
                                     f"The '{plugin_name}' plugin already exists. Do you want to overwrite it?")
        if not answer:
            return  # User chose not to overwrite

    try:
        # Copy the selected file to the plugins folder
        with open(file_path, "r") as src_file, open(plugin_path, "w") as dest_file:
            dest_file.write(src_file.read())

        # Refresh the plugin list
        refresh_plugin_list()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add the plugin.\nError: {e}")

# Function to remove the selected plugin
def remove_plugin():
    selected_index = plugin_listbox.curselection()
    if not selected_index:
        return  # No selection, do nothing

    selected_plugin = plugin_listbox.get(selected_index)

    # Confirm the removal with a message box
    answer = messagebox.askyesno("Remove Plugin", f"Are you sure you want to remove the '{selected_plugin}' plugin?")
    if not answer:
        return  # User chose not to remove

    # Delete the selected plugin file
    plugin_file = os.path.join("plugins", selected_plugin + ".py")
    try:
        os.remove(plugin_file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove the plugin.\nError: {e}")
        return

    # Refresh the plugin list
    refresh_plugin_list()

# Function to edit the selected plugin
def edit_plugin():
    selected_index = plugin_listbox.curselection()
    if not selected_index:
        return  # No selection, do nothing

    selected_plugin = plugin_listbox.get(selected_index)

    plugin_file = os.path.join("plugins", selected_plugin + ".py")

    # Open the plugin file in the system default text editor
    try:
        os.startfile(plugin_file)  # Works on Windows
    except:
        try:
            os.system(f"xdg-open {plugin_file}")  # Works on Linux
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the plugin file for editing.\nError: {e}")

# Function to launch the selected plugin in a new window
def launch_plugin(root):
    selected_index = plugin_listbox.curselection()
    if not selected_index:
        return  # No selection, do nothing

    selected_plugin = plugin_listbox.get(selected_index)

    # Import the plugin module dynamically
    try:
        plugin_module = importlib.import_module(f"plugins.{selected_plugin}")
    except ImportError:
        messagebox.showerror("Error", f"Failed to import the selected plugin: {selected_plugin}")
        return

    # Execute the plugin function in a new window
    plugin_module.flashing_text(root)  # Pass the 'root' argument to the flashing_text() function

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Crypto Trading Bot")

    # Set the window size to be 50% of the screen size
    window_width = root.winfo_screenwidth() // 2
    window_height = root.winfo_screenheight() // 2
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a frame to hold the plugin launcher
    plugin_launcher_frame = tk.Frame(root, bg="gray80")
    plugin_launcher_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Add a label for "Available Plugins"
    plugin_label = tk.Label(plugin_launcher_frame, text="Available Plugins", font=("Arial", 12, "bold"), bg="gray80")
    plugin_label.pack(pady=5)

    # Create a listbox to show the available plugins
    global plugin_listbox
    plugin_listbox = tk.Listbox(plugin_launcher_frame, selectmode=tk.SINGLE, width=30)
    plugin_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # Load the available plugins from the "plugins" folder on application startup
    refresh_plugin_list()

    # Create buttons for the plugin launcher
    btn_add = tk.Button(plugin_launcher_frame, text="+", width=3, command=add_new_plugin)
    btn_subtract = tk.Button(plugin_launcher_frame, text="-", width=3, command=remove_plugin)
    btn_edit = tk.Button(plugin_launcher_frame, text="Edit", width=10, command=edit_plugin)
    btn_launch = tk.Button(plugin_launcher_frame, text="Launch", width=10, command=lambda: launch_plugin(root))

    # Center the buttons underneath the plugin listbox
    btn_add.pack(side=tk.LEFT, padx=2, pady=5)
    btn_subtract.pack(side=tk.LEFT, padx=2, pady=5)
    btn_edit.pack(side=tk.LEFT, padx=2, pady=5)
    btn_launch.pack(side=tk.LEFT, padx=2, pady=5)

    # Create a frame to hold the readme display
    global readme_box
    readme_box = tk.Frame(root)
    readme_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create an HTMLLabel widget to display the README.md content
    global readme_text
    readme_text = HTMLLabel(readme_box, font=("Arial", 12))
    readme_text.pack(fill=tk.BOTH, expand=True)

    # Display the content of README.md by default
    show_readme()

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
