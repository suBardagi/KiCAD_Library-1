import re

infile = r"C:\Users\User\Desktop\efe\KiCAD_Libraries\symbols\Library-N1-Gate-Driver.kicad_sym"
outfile = r"C:\Users\User\Desktop\efe\KiCAD_Libraries\symbols\Library-N1-Gate-Driver.kicad_sym"

symbol_prefix = "UCC21550ADWR"
new_length = 2.54  # mm

inside_target_symbol = False
inside_pin = False
output_lines = []

# Regex patterns
at_regex = re.compile(r"\(at\s+([-\d\.]+)\s+([-\d\.]+)(?:\s+([-\d\.]+))?\)")
length_regex = re.compile(r"\(length\s+([0-9\.]+)\)")

# Temporary storage for pin lines
pin_lines = []

with open(infile, "r") as f:
    for line in f:
        stripped = line.strip()

        # Detect symbol blocks
        if stripped.startswith("(symbol") and symbol_prefix in stripped:
            inside_target_symbol = True
        elif stripped.startswith("(symbol") and symbol_prefix not in stripped:
            inside_target_symbol = False

        # Detect pin blocks
        if inside_target_symbol and stripped.startswith("(pin"):
            inside_pin = True
            pin_lines = [line]  # start collecting pin lines
            continue

        if inside_pin:
            pin_lines.append(line)
            # End of pin block
            if stripped.startswith(")"):
                inside_pin = False

                # Process the collected pin block
                pin_delta = 0
                # First, find the old length
                for pline in pin_lines:
                    length_match = length_regex.search(pline)
                    if length_match:
                        old_length = float(length_match.group(1))
                        pin_delta = new_length - old_length
                        break

                # Modify the pin block
                new_pin_lines = []
                for pline in pin_lines:
                    # Update length
                    pline = length_regex.sub(f"(length {new_length})", pline)
                    # Shift X coordinate if needed
                    if pin_delta != 0:
                        def shift_x_match(m):
                            x = float(m.group(1)) + pin_delta
                            y = m.group(2)
                            rot = m.group(3)

                            if x <= 0:
                                x -= 2*pin_delta  # positive X moves left
                            
                            if rot:
                                return f"(at {x} {y} {rot})"
                            else:
                                return f"(at {x} {y})"
                        pline = at_regex.sub(shift_x_match, pline)
                    new_pin_lines.append(pline)

                # Add modified pin block to output
                output_lines.extend(new_pin_lines)
            continue

        # Normal lines outside pin blocks
        output_lines.append(line)

# Write updated library
with open(outfile, "w") as f:
    f.writelines(output_lines)

print(f"Updated library written to {outfile}")
