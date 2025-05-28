import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import ImageTk, Image
import cv2
import numpy as np

# Create the main window
window = tk.Tk()
window.geometry("1000x700")
window.title("Image Encryption Decryption")
window.configure(bg="#caf0f8")

# Define global variables
global count, emig, key, image_encrypted, encryption_state
frp = []
tname = []
con = 1
bright = 0
panelB = None
panelA = None
key = None
image_encrypted = None
encryption_state = None  # Track the encryption state

# Function to get the path of the selected image
def getpath(path):
    a = path.split('/')
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

# Function to get the folder name from the selected image path
def getfoldername(path):
    a = path.split('/')
    name = a[-1]
    return name

# Function to get the file name of the selected image
def getfilename(path):
    a = path.split('/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

# Function to open the image file
def openfilename():
    filename = filedialog.askopenfilename(title='"pen')
    return filename

# Function to open the selected image
def open_img():
    global x, panelA, panelB, chooseb, saveb, key
    global count, eimg, location, filename
    count = 0
    x = openfilename()
    img = Image.open(x)
    eimg = img
    img = ImageTk.PhotoImage(img)
    temp = x
    location = getpath(temp)
    filename = getfilename(temp)
    
    if panelA is None or panelB is None:
        panelA = tk.Label(image=img, bg="#caf0f8")
        panelA.image = img
        panelA.place(relx=0.25, rely=0.5, anchor="center")
        
        panelB = tk.Label(image=img, bg="#caf0f8")
        panelB.image = img
        panelB.place(relx=0.75, rely=0.5, anchor="center")
    else:
        panelA.configure(image=img)
        panelB.configure(image=img)
        panelA.image = img
        panelB.image = img

    chooseb.lift()
    saveb.lift()

# Function to encrypt the image
def en_fun():
    global x, image_encrypted, key, encryption_state
    image_input = cv2.imread(x, 0)
    (x1, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0

    mu, sigma = 0, 0.1  # mean and standard deviation
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    image_encrypted = image_input / key
    cv2.imwrite(r'image_encrypted.jpg', image_encrypted * 255)  # Save the encrypted image
    encryption_state = 'encrypted'  # Update the encryption state
    imge = Image.open(r'image_encrypted.jpg')
    imge = ImageTk.PhotoImage(imge)
    panelB.configure(image=imge)
    panelB.image = imge
    messagebox.showinfo("Encrypt Status", "Image Encrypted successfully.\nKey: {}".format(key))

    # Load the decryption key when the image is uploaded
    key = load_key()

# Function to decrypt the image
def de_fun():
    global image_encrypted, key, encryption_state
    if key is None:
        messagebox.showerror("Error", "No decryption key loaded.")
        return
    
    if image_encrypted is None:
        messagebox.showerror("Error", "No encrypted image found.")
        return
    
    # Decrypt the image with the loaded key
    image_output = image_encrypted * key
    image_output *= 255.0
    cv2.imwrite('image_output.jpg', image_output)
    encryption_state = 'decrypted'  # Update the encryption state

    # Display the decrypted image
    imgd = Image.open('image_output.jpg')
    imgd = ImageTk.PhotoImage(imgd)
    panelB.configure(image=imgd)
    panelB.image = imgd
    messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")


# Function to reset the edited image to the original one
def reset():
    image = cv2.imread(x)[:, :, ::-1]
    global count, eimg
    count = 6
    global o6
    o6 = image
    image = Image.fromarray(o6)
    eimg = image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image
    messagebox.showinfo("Success", "Image reset to original format!")

# Function to save the encrypted image or decrypted image based on the current state
def save_img():
    global image_encrypted, key, x, encryption_state
    if image_encrypted is None:
        messagebox.showerror("Error", "No image found.")
        return

    if encryption_state == 'encrypted':
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        cv2.imwrite(filename.name, image_encrypted * 255)
        messagebox.showinfo("Success", "Encrypted Image Saved Successfully!")

    elif encryption_state == 'decrypted':
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        # Load the decrypted image
        image_decrypted = cv2.imread('image_output.jpg', cv2.IMREAD_COLOR)
        # Convert the image to RGB format (OpenCV reads images in BGR format)
        image_decrypted = cv2.cvtColor(image_decrypted, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename.name, image_decrypted)
        messagebox.showinfo("Success", "Decrypted Image Saved Successfully!")

# Function to save the encryption key to a file
def save_key():
    global key
    if key is None:
        messagebox.showerror("Error", "No encryption key available.")
        return
    
    filename = filedialog.asksaveasfilename(defaultextension=".npy")
    if filename:
        np.save(filename, key)
        messagebox.showinfo("Success", "Encryption key saved to file.")

# Function to load the encryption key from a file
def load_key():
    key_file = filedialog.askopenfilename(title="Select Key File", filetypes=[("NumPy array files", "*.npy")])
    if key_file:
        return np.load(key_file)
    else:
        messagebox.showerror("Error", "No decryption key selected.")
        return None

# Top label
start1 = tk.Label(text="Mask on Mask off\nImage Encryption Decryption", font=("Arial", 40), fg="#03045e", bg="#caf0f8")
start1.place(relx=0.5, rely=0.1,anchor="center")

# Original image label
start1 = tk.Label(text="Original\nImage", font=("Arial", 30), fg="#03045e", bg="#caf0f8")
start1.place(relx=0.25, rely=0.5, anchor="center")

# Encrypted/Decrypted image label
start1 = tk.Label(text="Encrypted\nDecrypted\nImage", font=("Arial", 30), fg="#03045e", bg="#caf0f8")
start1.place(relx=0.75, rely=0.5, anchor="center")

# Choose button
chooseb = tk.Button(window, text="Choose", command=open_img, font=("Arial", 20), bg="#00b4d8", fg="white", borderwidth=3,relief="raised")
chooseb.place(relx=0.25, rely=0.3, anchor="center")

# Save button
saveb = tk.Button(window, text="Save", command=save_img, font=("Arial", 20), bg="#98fb98", fg="black", borderwidth=3,relief="raised")
saveb.place(relx=0.75, rely=0.3, anchor="center")

# Encrypt button
enb = tk.Button(window, text="Encrypt", command=en_fun, font=("Arial", 20), bg="#00b4d8", fg="white", borderwidth=3,relief="raised")
enb.place(relx=0.20, rely=0.90, anchor="center")

# Decrypt button
deb = tk.Button(window, text="Decrypt", command=de_fun, font=("Arial", 20), bg="#00b4d8", fg="white", borderwidth=3,relief="raised")
deb.place(relx=0.40, rely=0.90, anchor="center")

# Reset button
resetb = tk.Button(window, text="Reset", command=reset, font=("Arial", 20), bg="#00b4d8", fg="white", borderwidth=3, relief="raised")
resetb.place(relx=0.60, rely=0.90, anchor="center")

# Save Key button
save_key_button = tk.Button(window, text="Save Key", command=save_key, font=("Arial", 20), bg="#00b4d8", fg="white", borderwidth=3, relief="raised")
save_key_button.place(relx=0.80, rely=0.90, anchor="center")

# Load Key button
load_key_button = tk.Button(window, text="Load Key", command=load_key, font=("Arial", 20), bg="#00b4d8", fg="white", borderwidth=3, relief="raised")
load_key_button.place(relx=0.90, rely=0.90, anchor="center")

# Function to exit the application
def exit_win():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Exit button
exitb = tk.Button(window, text="EXIT", command=exit_win, font=("Arial", 20), bg="red", fg="black", borderwidth=3,
               relief="raised")
exitb.place(relx=0.93, rely=0.07, anchor="center")

# Load and display the logo
logo_img = Image.open(r"C:\Users\user\Desktop\Image\word logo.png")
logo_img = logo_img.resize((100, 100), Image.BICUBIC)  # Resize the logo as needed
logo_img = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(window, image=logo_img, bg="#caf0f8")
logo_label.image = logo_img
logo_label.place(relx=0.07, rely=0.09, anchor="center")

# Define the protocol for window closure
window.protocol("WM_DELETE_WINDOW", exit_win)

# Start the main event loop
window.mainloop()
