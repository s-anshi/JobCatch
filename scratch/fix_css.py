import re

with open('static/css/style.css', 'r') as f:
    css = f.read()

# Replace hardcoded white backgrounds
css = re.sub(r'background:\s*white;', 'background: var(--surface);', css)
css = re.sub(r'background-color:\s*white;', 'background-color: var(--surface);', css)

# Fix --secondary text usage (stats, values, headers) to --text-heading
css = re.sub(r'color:\s*var\(--secondary\);', 'color: var(--text-heading);', css)

# Fix #f8fafc (slate 50) used as a slightly off-white background to --bg-color or --surface-hover
css = re.sub(r'background-color:\s*#f8fafc;', 'background-color: var(--surface-hover);', css)
css = re.sub(r'background-color:\s*#f1f5f9;', 'background-color: var(--surface-hover);', css)

# Make sure buttons that really need white text still have it, e.g. btn-primary
# (btn-primary color is `white;` which we didn't touch because we only replaced `background: white;`)
# btn-google hover has background-color: #f1f5f9; which is now var(--surface-hover).

with open('static/css/style.css', 'w') as f:
    f.write(css)

print("CSS variables updated successfully!")
