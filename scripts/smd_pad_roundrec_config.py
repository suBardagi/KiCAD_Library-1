import re
import tkinter as tk
from tkinter import filedialog

# Open a file picker dialog
root = tk.Tk()
root.withdraw()  # hide the main tkinter window
infile = filedialog.askopenfilename(
    title="Select a KiCad footprint file",
    filetypes=[("KiCad footprint", "*.kicad_mod"), ("All files", "*.*")]
)

if not infile:
    print("No file selected. Exiting.")
    exit()

# Output file (adds -fixed before extension)
outfile = infile.replace(".kicad_mod", ".kicad_mod")

# Desired rratio for rounded rectangle
rratio = 0.25

output_lines = []

# Regex to match pad line with smd rect
pad_regex = re.compile(r'\(pad\s+"(\d+)"\s+smd\s+rect')

with open(infile, "r") as f:
    for line in f:
        pad_match = pad_regex.search(line)
        if pad_match:
            # Convert rect → roundrect
            line = line.replace("smd rect", "smd roundrect")
            output_lines.append(line)
            # Insert roundrect_rratio line after pad declaration
            output_lines.append(f'\t\t(roundrect_rratio {rratio})\n')
        else:
            output_lines.append(line)

with open(outfile, "w") as f:
    f.writelines(output_lines)

print(f"Updated footprint written to {outfile}")
