import zipfile
import os

# Define paths
base_dir = "/mnt/data/rajput-portfolio"
os.makedirs(base_dir, exist_ok=True)

# Create the necessary folder structure
os.makedirs(os.path.join(base_dir, "static", "images"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "templates"), exist_ok=True)

# Create app.py
app_py_content = """
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
"""
with open(os.path.join(base_dir, "app.py"), "w") as f:
    f.write(app_py_content.strip())

# Create requirements.txt
requirements_content = "Flask==2.3.2\ngunicorn"
with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
    f.write(requirements_content)

# Create Procfile
with open(os.path.join(base_dir, "Procfile"), "w") as f:
    f.write("web: gunicorn app:app")

# Create templates/index.html
index_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rajput Mayur - Portfolio</title>
</head>
<body>
    <h1>Welcome to Rajput Mayur's Portfolio</h1>
    <img src="{{ url_for('static', filename='images/image.png') }}" alt="Profile Image">
</body>
</html>
"""
with open(os.path.join(base_dir, "templates", "index.html"), "w") as f:
    f.write(index_html_content.strip())

# Add a placeholder image file in static/images
image_path = os.path.join(base_dir, "static", "images", "image.png")
with open(image_path, "wb") as f:
    f.write(b'\x89PNG\r\n\x1a\n')  # Simple PNG header as a placeholder

# Create a zip file
zip_path = "/mnt/data/rajput-portfolio-ready.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, base_dir)
            zipf.write(file_path, arcname)

zip_path
