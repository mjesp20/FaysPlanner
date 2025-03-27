import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import random
import os

# Define class-to-role mapping
class_roles = {
    "warrior": "m",  # Melee DPS
    "priest": "h",  # Healer
    "druid": "m",  # Melee DPS
    "mage": "r",  # Ranged DPS
    "warlock": "r",  # Ranged DPS
    "hunter": "r",  # Ranged DPS
    "paladin": "m",  # Melee DPS
    "shaman": "h",  # Healer
    "rogue": "m"  # Melee DPS
}

# Define class colors
class_colors = {
    "druid": "#FF7C0A",
    "hunter": "#AAD372",
    "mage": "#3FC7EB",
    "paladin": "#F48CBA",
    "priest": "#FFFFFF",
    "rogue": "#FFF468",
    "shaman": "#0070DD",
    "warlock": "#8788EE",
    "warrior": "#C69B6D"
}

# Dictionary to store player classes
player_classes = {}

# Dictionary to store selected values for each row
selected_values = {}

# Configuration file for saving last used path
CONFIG_FILE = "faysplanner_config.txt"


# Function to save last used file path
def save_last_path(path):
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(path)
    except Exception as e:
        print(f"Error saving config: {e}")


# Function to load last used file path
def load_last_path():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return f.read().strip()
    except Exception as e:
        print(f"Error loading config: {e}")
    return ""


# Function to handle file import
def import_file():
    last_path = load_last_path()
    filename = filedialog.askopenfilename(
        title="Select Player Data File",
        initialdir=os.path.dirname(last_path) if last_path else os.getcwd(),
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if filename:
        save_last_path(filename)
        try:
            with open(filename, 'r') as f:
                data = f.read()
            process_player_data(data)
        except Exception as e:
            tk.messagebox.showerror("Import Error", f"Could not read file: {e}")


# Function to handle the paste data window
def create_paste_window():
    paste_window = tk.Toplevel()
    paste_window.title("Paste Player Data")
    paste_window.geometry("600x600")
    paste_window.transient(window)  # Make it modal (stay on top of main window)
    paste_window.grab_set()  # Force focus on this window

    # Instructions label
    instruction_label = tk.Label(paste_window, text="Paste player data in format: name,class (one per line)")
    instruction_label.pack(pady=10)

    # Text area for pasting
    text_area = scrolledtext.ScrolledText(paste_window, width=50, height=20)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Button frame
    button_frame = tk.Frame(paste_window)
    button_frame.pack(pady=10, fill=tk.X)

    # Done button (Submit)
    def submit_data():
        data = text_area.get("1.0", tk.END).strip()
        process_player_data(data)
        paste_window.destroy()

    done_btn = tk.Button(button_frame, text="Done", command=submit_data, width=10)
    done_btn.pack(side=tk.RIGHT, padx=10)

    # Cancel button
    def cancel():
        paste_window.destroy()

    cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel, width=10)
    cancel_btn.pack(side=tk.RIGHT, padx=10)

    # Set focus on text area
    text_area.focus_set()


# Function to process the pasted player data
def process_player_data(data):
    # Clear existing data
    for item in tree.get_children():
        tree.delete(item)

    player_classes.clear()
    selected_values.clear()

    # Process each line
    lines = data.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            # Parse CSV line
            parts = line.split(',')
            if len(parts) >= 2:
                name = parts[0].strip()
                player_class = parts[1].strip().lower()

                # Store player class for color reference
                player_classes[name] = player_class

                # Set default role based on class
                default_role = class_roles.get(player_class, None)

                # Create values with radio buttons
                values = [name, "○", "○", "○"]

                # Set the default role if one exists
                if default_role:
                    if default_role == "m":
                        values[1] = "●"  # Melee DPS
                    elif default_role == "h":
                        values[2] = "●"  # Healer
                    elif default_role == "r":
                        values[3] = "●"  # Ranged DPS

                # Insert into tree and store selection
                item_id = tree.insert('', 'end', values=values, tags=(player_class,))
                selected_values[item_id] = default_role


# Function to handle click events for radio button behavior
def handle_click(event):
    # Get the clicked item and column
    item_id = tree.identify_row(event.y)
    if not item_id:
        return

    column = tree.identify_column(event.x)
    column_idx = int(column[1:]) - 1  # Convert '#2' to 1 (0-based index)

    # Only process clicks on columns m, h, or r (indexes 1, 2, 3)
    if column_idx < 1 or column_idx > 3:
        return

    # Get current values
    values = list(tree.item(item_id, "values"))

    # Column names corresponding to indices
    col_names = ["Name", "m", "h", "r"]
    selected_col = col_names[column_idx]

    # Reset all radio buttons in this row
    values[1] = "○"  # m
    values[2] = "○"  # h
    values[3] = "○"  # r

    # Set the clicked one as selected
    values[column_idx] = "●"

    # Update the tree
    tree.item(item_id, values=values)

    # Store the selected value
    selected_values[item_id] = selected_col

    print(f"Player: {values[0]}, Role: {selected_col}")


# Function to get all current selections
def get_selections():
    result = {}
    for item_id in selected_values:
        name = tree.item(item_id, "values")[0]
        role = selected_values[item_id]
        if role:  # Only include players with a selected role
            result[name] = role
    return result


# Function to create a header for our custom grid tables
def create_header(parent, titles):
    header_frame = ttk.Frame(parent)
    header_frame.pack(fill=tk.X, padx=2, pady=2)

    # Create equally spaced columns
    for i, title in enumerate(titles):
        header_label = ttk.Label(header_frame, text=title, font=('Helvetica', 10, 'bold'))
        header_label.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
        header_frame.grid_columnconfigure(i, weight=1)

    return header_frame


# Function to clear both custom grid tables
def clear_tables():
    # Clear group1_4 table
    for row in table1_cells:
        for cell in row:
            if cell:
                cell.destroy()

    # Clear group5_8 table
    for row in table2_cells:
        for cell in row:
            if cell:
                cell.destroy()

    # Reset the cell arrays
    table1_cells.clear()
    table2_cells.clear()


# Function to generate groups based on selections
def generate_button_clicked():
    selections = get_selections()

    # Sort players by role
    melee_dps = []
    healers = []
    ranged_dps = []

    for name, role in selections.items():
        if role == "m":
            melee_dps.append(name)
        elif role == "h":
            healers.append(name)
        elif role == "r":
            ranged_dps.append(name)

    # Shuffle players within each role for randomness
    random.shuffle(melee_dps)
    random.shuffle(healers)
    random.shuffle(ranged_dps)

    # Create 8 groups
    groups = [[] for _ in range(8)]

    # Check 1 melee mode checkbox
    one_melee_mode = one_melee_var.get()

    # Assign 1 or 2 melee DPS per group
    melee_assignments = 1 if one_melee_mode else 2
    for _ in range(melee_assignments):
        for i in range(min(8, len(melee_dps))):
            groups[i].append(melee_dps.pop(0))

    # Assign 1 healer per group (up to 8)
    for i in range(min(8, len(healers))):
        groups[i].append(healers.pop(0))

    # Assign remaining healers randomly
    for healer in healers:
        # Find group with fewest members
        group_idx = min(range(8), key=lambda i: len(groups[i]))
        groups[group_idx].append(healer)

    # Assign ranged DPS randomly to fill groups
    for ranged in ranged_dps:
        # Find group with fewest members
        group_idx = min(range(8), key=lambda i: len(groups[i]))
        groups[group_idx].append(ranged)

    # Assign remaining melee DPS randomly (these will be sitting out if all groups are full)
    for melee in melee_dps:
        # Find group with fewest members
        group_idx = min(range(8), key=lambda i: len(groups[i]))
        groups[group_idx].append(melee)

    # Clear existing tables
    clear_tables()

    # Calculate how many rows we need in the tables
    max_group_size = max(len(group) for group in groups)

    # Fill tables with group assignments using colored cells
    for row_idx in range(max_group_size):
        # Create a new row of cells for table1
        table1_row = []
        for col_idx in range(4):
            group_idx = col_idx
            if row_idx < len(groups[group_idx]):
                player_name = groups[group_idx][row_idx]
                player_class = player_classes.get(player_name, "").lower()
                bg_color = class_colors.get(player_class, "#f0f0f0")  # Default gray if class not found

                # Create a frame for the cell with the correct background color
                cell_frame = tk.Frame(group1_4_content, bg=bg_color, bd=1, relief=tk.SOLID)
                cell_frame.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

                # Create a label inside the frame
                cell_label = tk.Label(cell_frame, text=player_name, bg=bg_color)
                cell_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

                table1_row.append(cell_frame)
            else:
                # Empty cell
                cell_frame = tk.Frame(group1_4_content, bg="#f0f0f0", bd=1, relief=tk.SOLID)
                cell_frame.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

                # Create an empty label
                cell_label = tk.Label(cell_frame, text="", bg="#f0f0f0")
                cell_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

                table1_row.append(cell_frame)

        table1_cells.append(table1_row)

        # Create a new row of cells for table2
        table2_row = []
        for col_idx in range(4):
            group_idx = col_idx + 4
            if row_idx < len(groups[group_idx]):
                player_name = groups[group_idx][row_idx]
                player_class = player_classes.get(player_name, "").lower()
                bg_color = class_colors.get(player_class, "#f0f0f0")  # Default gray if class not found

                # Create a frame for the cell with the correct background color
                cell_frame = tk.Frame(group5_8_content, bg=bg_color, bd=1, relief=tk.SOLID)
                cell_frame.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

                # Create a label inside the frame
                cell_label = tk.Label(cell_frame, text=player_name, bg=bg_color)
                cell_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

                table2_row.append(cell_frame)
            else:
                # Empty cell
                cell_frame = tk.Frame(group5_8_content, bg="#f0f0f0", bd=1, relief=tk.SOLID)
                cell_frame.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

                # Create an empty label
                cell_label = tk.Label(cell_frame, text="", bg="#f0f0f0")
                cell_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

                table2_row.append(cell_frame)

        table2_cells.append(table2_row)

    # Make sure rows expand properly
    for i in range(max_group_size):
        group1_4_content.grid_rowconfigure(i, weight=1)
        group5_8_content.grid_rowconfigure(i, weight=1)

    # Print group assignments for debugging
    print("\nGroup assignments:")
    for i, group in enumerate(groups):
        print(f"Group {i + 1}: {group}")


# Initialize main application
window = tk.Tk()
window.title("FaysPlanner")
window.geometry("1400x900")

# Create a style
style = ttk.Style()
style.configure("Treeview", font=('Helvetica', 10))

# Main frame to hold the left and right sections
main_frame = ttk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left frame for the PlayerTable
left_frame = ttk.Frame(main_frame, width=600)
left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
left_frame.pack_propagate(False)  # Prevent frame from resizing to fit contents

# Right frame for the two stacked tables
right_frame = ttk.Frame(main_frame, width=800)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
right_frame.pack_propagate(False)  # Prevent frame from resizing to fit contents

# Player Table (left side) with radio button behavior
tree = ttk.Treeview(left_frame, columns=("Name", "m", "h", "r"), show='headings')
tree.pack(fill=tk.BOTH, expand=True)

tree.heading("Name", text="Name")
tree.heading("m", text="Melee DPS")
tree.heading("h", text="Healer")
tree.heading("r", text="Ranged DPS")

tree.column("Name", width=150, minwidth=100)
tree.column("m", width=80, anchor=tk.CENTER)
tree.column("h", width=80, anchor=tk.CENTER)
tree.column("r", width=80, anchor=tk.CENTER)

# Create tags for each class with their color
for class_name, color in class_colors.items():
    tree.tag_configure(class_name, background=color)

# Top section for groups 1-4
top_frame = ttk.Frame(right_frame)
top_frame.pack(fill=tk.BOTH, expand=True)

# Bottom section for groups 5-8
bottom_frame = ttk.Frame(right_frame)
bottom_frame.pack(fill=tk.BOTH, expand=True)

# Create headers for both tables
group1_4_header = create_header(top_frame, ["Group 1", "Group 2", "Group 3", "Group 4"])
group5_8_header = create_header(bottom_frame, ["Group 5", "Group 6", "Group 7", "Group 8"])

# Create content frames for our custom grid tables
group1_4_content = ttk.Frame(top_frame)
group1_4_content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

group5_8_content = ttk.Frame(bottom_frame)
group5_8_content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

# Configure grid columns to be exactly 1/4 the width
for i in range(4):
    group1_4_content.grid_columnconfigure(i, weight=1, uniform="group1_4")
    group5_8_content.grid_columnconfigure(i, weight=1, uniform="group5_8")

# These will store our cell widgets for later updates
table1_cells = []  # Will be a 2D array of labels for groups 1-4
table2_cells = []  # Will be a 2D array of labels for groups 5-8

# Bind click event
tree.bind("<ButtonRelease-1>", handle_click)

# Create a button frame at the bottom
button_frame = tk.Frame(window)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# One melee mode checkbox
one_melee_var = tk.BooleanVar(value=False)
one_melee_checkbox = tk.Checkbutton(button_frame, text="1 Melee Mode", variable=one_melee_var)
one_melee_checkbox.pack(side=tk.LEFT, padx=10)

# Generate button
generate_button = tk.Button(button_frame, text="Generate", command=generate_button_clicked)
generate_button.pack(side=tk.RIGHT, padx=10)

# Add Manual Import button to open paste window
manual_import_button = tk.Button(button_frame, text="Manual Import", command=create_paste_window)
manual_import_button.pack(side=tk.RIGHT, padx=10)

# Add File Import button
file_import_button = tk.Button(button_frame, text="Import File", command=import_file)
file_import_button.pack(side=tk.RIGHT, padx=10)

window.mainloop()