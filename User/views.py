from django.shortcuts import render,redirect 
from django.contrib.auth.models import User,auth 
from django.contrib import messages 
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import cv2
from cryptography.fernet import Fernet
from tkinter import Button, Tk, Label, Entry, filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import numpy as np 
import subprocess

# Create the main window
window = Tk()
window.geometry("1255x710")
window.title("Image Encryption Decryption")
window.configure(bg="#F7E8C8")

# Top label
start1 = Label(text="Mask on Mask off\nImage Encryption Decryption", font=("Arial", 40), fg="#000000", bg="#F7E8C8")
start1.place(relx=0.5, rely=0.1, anchor="center")

# Load and display the logo0 
logo_img = Image.open(r"static\logo_type_2.png")
logo_img = logo_img.resize((175, 175), Image.BICUBIC)  # Resize the logo as needed
logo_img = ImageTk.PhotoImage(logo_img)
logo_label = Label(window, image=logo_img, bg="#F7E8C8")
logo_label.image = logo_img
logo_label.place(relx=0.09, rely=0.09, anchor="center")

    
# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def register(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        psw=request.POST['psw']
        psw1=request.POST['psw1']
        if psw==psw1:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"Username Exists")
                return render(request,"register.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Exists")
                return render(request,"register.html")
            else:
                user=User.objects.create_user(first_name=fname,
                last_name=lname,username=uname,email=email,
                password=psw)
                return redirect('login')
        else:
            messages.info(request,"Password not matching")
            return render(request,"register.html")
    return render(request,"register.html")

def login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        psw=request.POST['psw']
        user=auth.authenticate(username=uname,password=psw)
        if user is not None:
            auth.login(request,user)
            return redirect('data')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request,"login.html")

def data(request):
    # Function to generate a random key
    def generate_key():
        return Fernet.generate_key()
    
    #the blank Image
    blank_image = Image.open(r"static\blank space.png")
    # Resize the image as needed 
    blank_image = blank_image.resize((1150, 400))
    # Convert the image to PhotoImage object
    blank_photo = ImageTk.PhotoImage(blank_image)

    # Create a Label to display the image
    blank_label = Label(window, image=blank_photo, bg="#F7E8C8")
    blank_label.image = blank_photo  # Keep a reference to avoid garbage collection

    # Place the Label in the middle of the GUI
    blank_label.place(relx=0.5, rely=0.5, anchor="center")

    # Function to encrypt image with a given key
    def encrypt_image(image_path, key):
        fernet = Fernet(key)
        # Read image using OpenCV
        image = cv2.imread(image_path)
        # Convert image to bytes
        image_data = cv2.imencode('.png', image)[1].tobytes()
        # Encrypt image data
        encrypted_data = fernet.encrypt(image_data)
        return encrypted_data

    # Function to decrypt image with the given key
    def decrypt_image(encrypted_image_path, key):
        fernet = Fernet(key)
        # Read encrypted image data
        with open(encrypted_image_path, 'rb') as f:
            encrypted_data = f.read()
        # Decrypt image data
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data

    # Function to handle decryption process
    def decrypt_process():
        try:
            # Get decryption key from user
            decryption_key_path = filedialog.askopenfilename(title="Select Decryption Key")
            if not decryption_key_path:
                messagebox.showerror("File Selection Error", "No decryption key file selected.")
                return
            
            with open(decryption_key_path, 'rb') as key_file:
                decryption_key = key_file.read()

            # Get encrypted image file path from user
            encrypted_image_path = filedialog.askopenfilename(title="Select Encrypted Image")
            if not encrypted_image_path:
                messagebox.showerror("File Selection Error", "No encrypted image file selected.")
                return

            # Decrypt the image
            decrypted_data = decrypt_image(encrypted_image_path, decryption_key)

            # Choose a custom folder path to save the decrypted image
            custom_folder_path = filedialog.askdirectory(title="Select Custom Folder")
            if not custom_folder_path:
                messagebox.showerror("Folder Selection Error", "No custom folder selected.")
                return

            # Get the filename from the encrypted image path
            _, filename = os.path.split(encrypted_image_path)

            # Create a new filename for the decrypted image
            decrypted_image_path = os.path.join(custom_folder_path, "decrypted_" + filename)

            # Write decrypted data to the new image file
            with open(decrypted_image_path, 'wb') as f:
                f.write(decrypted_data)

            # Save the decryption key to a text file in the custom folder
            key_file_path = os.path.join(custom_folder_path, "decryption_key.txt")
            with open(key_file_path, "wb") as key_file:
                key_file.write(decryption_key)

            messagebox.showinfo("Decryption", f"Image decrypted and saved as '{decrypted_image_path}'\nDecryption key saved as '{key_file_path}'")
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Error decrypting image: {str(e)}")


    # Function to split image into YUV components
    def split_YUV():
        # Get image path from user
        image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if not image_path:
            messagebox.showerror("File Selection Error", "No image file selected.")
            return

        # Read the image
        image = cv2.imread(image_path)

        # Convert the image to YUV color space
        yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

        # Split the image into YUV components
        Y, U, V = cv2.split(yuv_image)

        # Choose the output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            messagebox.showerror("Directory Selection Error", "No output directory selected.")
            return

        output_dir = os.path.join(output_dir, 'YUV_Components')
        os.makedirs(output_dir, exist_ok=True)

        # Save the Y, U, and V components as separate image files
        cv2.imwrite(os.path.join(output_dir, 'Y_component.jpg'), Y)
        cv2.imwrite(os.path.join(output_dir, 'U_component.jpg'), U)
        cv2.imwrite(os.path.join(output_dir, 'V_component.jpg'), V)

        # Display the Y, U, V components, and merged YUV image using matplotlib
        plt.figure(figsize=(20, 6))

        plt.subplot(1, 5, 1)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title('Original image')
        plt.axis('off')

        plt.subplot(1, 5, 2)
        plt.imshow(Y, cmap='gray')
        plt.title('Y Component')
        plt.axis('off')

        plt.subplot(1, 5, 3)
        plt.imshow(U, cmap='gray') 
        plt.title('U Component')
        plt.axis('off')

        plt.subplot(1, 5, 4)
        plt.imshow(V, cmap='gray')
        plt.title('V Component')
        plt.axis('off')

    # Function to handle encryption process
    def encrypt_process():
        try:
            # Generate a random key
            key = generate_key()

            # Convert the key to a string
            key_str = key.decode()

            # Display the key
            # key_label.config(text="Generated Key: " + key_str)

            # Save the key to a text file
            key_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save Key")
            if key_file_path:
                with open(key_file_path, "w") as key_file:
                    key_file.write(key_str)
            
                # Get image path from user
                image_path = filedialog.askopenfilename()

                # Check if a file is selected
                if image_path:
                    # Prompt user to enter filename for encrypted image
                    encrypted_filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], title="Save Encrypted Image As")
                    if encrypted_filename:
                        # Encrypt the image
                        encrypted_data = encrypt_image(image_path, key)

                        # Save the encrypted data to the specified filename
                        with open(encrypted_filename, 'wb') as f:
                            f.write(encrypted_data)

                        messagebox.showinfo("Encryption", f"Image encrypted and saved as '{encrypted_filename}'\nKey saved as '{key_file_path}'")
            else:
                messagebox.showerror("File Selection Error", "No image selected.")
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Error encrypting image: {str(e)}")



    '''Entry field for user to enter the filename for the encrypted image
    filename_entry_label = Label(window, text="Enter filename for encrypted image:", bg='#ED6436', fg='#333333', font=('Helvetica', 16, 'bold'))
    filename_entry_label.place(relx=0.5, rely=0.65, anchor="center")
    filename_entry = Entry(window, width=40, font=('Helvetica', 16))
    filename_entry.place(relx=0.5, rely=0.7, anchor="center")'''



    # Label to display generated key
    key_label = Label(window, text="", bg="#F7E8C8")
    key_label.place(relx=0.5, rely=0.6, anchor="center")

    # Button to trigger Split Image process
    split_button = ttk.Button(window, text="Split Image", command=split_YUV, style='Custom.TButton', width="100%")
    split_button.place(relx=0.20, rely=0.90, anchor="center")

    # Button to trigger encryption process
    encrypt_button = ttk.Button(window, text="Encrypt Image", command=encrypt_process, style='Custom.TButton', width="100%")
    encrypt_button.place(relx=0.40, rely=0.90, anchor="center")

    # Button to trigger decryption process
    decrypt_button = ttk.Button(window, text="Decrypt Image", command=decrypt_process, style='Custom.TButton', width="100%")
    decrypt_button.place(relx=0.60, rely=0.90, anchor="center")

    #starts external python program
    def start_another_program():
        # Replace 'C:\\Users\\user\\Desktop\\test merge 2.py' with the path to your Python script
        subprocess.Popen(['python',r"static\external_merge_code.py"])

    # Button to trigger Merge Image process
    merge_button = ttk.Button(window, text="Merge Image", command=start_another_program, style='Custom.TButton', width="100%")
    merge_button.place(relx=0.80, rely=0.90, anchor="center")


    # Define a custom style for the buttons
    button_style = ttk.Style()
    button_style.configure('Custom.TButton', background='#00B4D8', foreground='black', font=('Arial', 24), borderwidth=3, relief='raised')

    # Function to exit the application
    def exit_win():
        if messagebox.askokcancel("Exit", "Do you want to exit?"): window.destroy()

    # Exit button
    exitb = Button(window, text="EXIT", command=exit_win, font=("Arial", 20), bg="red", fg="black", borderwidth=3, relief="raised")
    exitb.place(relx=0.93, rely=0.07, anchor="center")

    window.mainloop()

    return render(request,"data.html")

def logout(request):
    auth.logout(request)
    return redirect('/')
