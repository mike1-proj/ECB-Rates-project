""" This standalone .py script is Using Pillow image editor to create a.png from a.jpeg for the currency converter app.
 This will open the .jpeg (if its in the local project folder) and save the new .png image into the project
 folder it runs in. In this case, it's the ECB_currency project folder"""
from PIL import Image

# Open the original JPEG
image = Image.open("euroimg.jpg")

# Resize it to 256 x 256 pixels
image = image.resize((256, 256), Image.Resampling.LANCZOS)

# Save it as a PNG
image.save("euro-icon.png")

print("Icon created successfully!")
