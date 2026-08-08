#StegBuster Steganalysis Application for Finall Year Project
#Harry Girdler

#Import Scripts
import os #For functions relating to the operating system
import time #For functions relating to time
import tkinter as tk #Tkinter for user interface
from tkinter import filedialog, Label, Button, scrolledtext, messagebox, PhotoImage #For file selection, labelling and button creation; modules from TKinter package
import numpy as np #Library for numerical computations
import matplotlib.pyplot as plt #For histogram and heatmap plotting
from PIL import Image, ImageTk #Pillow; Imaging library for image filetype support
from scipy.stats import chisquare #Scientific computation package that allows the usage of the chi-square module; contains formula
import magic #Libmagic library for detection of filetypes
import datetime #For determining date and time handling
import hashlib #For generating hash values of selected image files
from cryptography.fernet import Fernet #For encryption/decryption (for quarantining files)


os.chdir(os.path.dirname(os.path.abspath(__file__))) #Changes directory to that of this application
    
###################################################################################################

# GUI Setup
root = tk.Tk() #Defining the variable 'root' as TKinter user interface for main application (home)
root.title("StegBuster") #Application Title
root.geometry("1010x650") #Window Size
root.iconbitmap("logo.ico") #Uses the logo icon created as the application icon

#Top Framing for Buttons and Title
top_frame = tk.Frame(root) #Creates frame for application widgets
top_frame.pack(side = tk.TOP, fill = tk.X, padx = 10, pady = 10) #Positions, aligns at top, expands to fill space, adds padding

button_frame = tk.Frame(top_frame) #Creates frame dedicated for buttons within the application
button_frame.pack(side = tk.LEFT, padx = 10) #Positions, aligns at top left, expands to fill space, adds padding

preview_frame = tk.Frame(top_frame) #creates a frame dedicated for image previewing within the appliaction
preview_frame.pack(side = tk.RIGHT, padx = 10) #Positions, aligns at top right, expands to fill space, adds padding

Label(button_frame, text="StegBuster", font=("Arial", 16, "bold")).pack(pady = 5) #Labels the button frame "StegBuster", displaying title within the application

#Logo Icon Dispaly
big_logo = Image.open("logo.png") #Logo image too big, locates big logo
small_logo = big_logo.resize((150,150)) #Resizes logo to 150 x 150
app_logo = ImageTk.PhotoImage(small_logo) #Converts logo to Tkinter widget
logo_label = tk.Label(root, image = app_logo) #Locates the image as label with the given logo
logo_label.pack(side = tk.LEFT, padx = 5) #Positions logo on the left side with 5 pixel horizontal padding

# Image Display
image_label = Label(preview_frame) #Labels image space (which is the determined by preview frame)
image_label.pack() #Positions and allocates space for preview image to be displayed

#Bottom Frame for Metadata and Steganalysis Displays
bottom_frame = tk.Frame(root) #Creates a new frame
bottom_frame.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True, padx = 10, pady = 10) #New frame located at the bottom of the application, expand to fit, 10 pixel padding all round

# Metadata Information Display
metadata_column = tk.Frame(bottom_frame) #New column in bottom frame
metadata_column.pack(side = tk.LEFT, fill = tk.BOTH, expand = True, padx = (0, 5)) #Positions left of bottom frame, fills and expands to allocated space, with 5 pixel padding on the right hand side 

metadata_label = Label(metadata_column, text="Image Metadata Information", font = ("Arial", 14, "bold")) #Labels the metadata column with font, font size, and bold effect
metadata_label.pack(anchor="center") #Aligns label to center within allocated space (metadata column)

metadata_box = scrolledtext.ScrolledText(metadata_column, width = 50, height = 20, wrap = tk.WORD, font = ("Arial", 10)) #Creates text box with scrollbar
metadata_box.pack(fill=tk.BOTH, expand=True) #Fits and expands to the metadata column

# Steganalysis Display
steg_column = tk.Frame(bottom_frame) #New column in bottom frame
steg_column.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True, padx = (5, 0)) #Positions right of the bottom frame, fills and expands to allocated space, with 5 pixel padding on the left hand side

steg_label = Label(steg_column, text = "Steganography Detection", font = ("Arial", 14, "bold")) #Labels the stegbox column with font, font size, and bold effect
steg_label.pack(anchor="center") #Aligns label to center within allocated space (stegbox column)

detection_box = scrolledtext.ScrolledText(steg_column, width = 50, height = 20, wrap = tk.WORD, font=("Arial", 10)) #Creates text box with scrollbar
detection_box.pack(fill=tk.BOTH, expand=True) #Fits and expands to the stegbox column

###################################################################################################

#Image Comparison Feature
def comparison(path1, path2): #Defines comparison function with path1 and path2 as parameters
    comparison1 = Image.open(path1).convert("L") #Opens the first image through the first path, converting the image to greyscale
    comparison2 = Image.open(path2).convert("L") #Opens the second image through the second path, converting the image to greyscale

    comparison1_arr = np.array(comparison1) #Converts greyscale inmage into an image array
    comparison2_arr = np.array(comparison2) #Converts greyscale image into an image array

    if comparison1.size != comparison2.size: #If the 2 images do not share the same resolution
        messagebox.showerror("Error", f"Both selected images must have equal resolutions.") #Show the following error message
        return #Exit comparison function

    image_difference = np.abs(comparison1_arr - comparison2_arr) #Absolute difference between the two image arrays

    fig, axis = plt.subplots(1, 3, figsize = (15, 5)) #Creates 1 row of 3 columns, 15 inches wide and 5 high
    axis[0].imshow(comparison1, cmap = 'gray') #Displays first column as first image in greyscale
    axis[0].set_title("Image 1") #Gives the first image a title (Image 1)
    axis[0].axis('off') #Hides image axis and plot axis

    axis[1].imshow(comparison2, cmap = 'gray') #Displays second column as second image in greyscale
    axis[1].set_title("Image 2") #Gives the second image a title (Image 2)
    axis[1].axis('off') #Hides image axis and plot axis

    axis[2].imshow(image_difference, cmap = 'hot') #Displays third column as image difference in hot colourmap 
    axis[2].set_title("Difference Bettween Images") #Gives the image difference a title
    axis[2].axis('off') #Hides image axis and plot axis

    plt.show() #Diplays the planned plot
    
###################################################################################################
    
#File Path Navigation for Image Comparison Feature
def open_image_comparison(): #Defines the function for selecting two images 
    file_paths = filedialog.askopenfilenames(title="Select Two Images", filetypes = [("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if len(file_paths) == 2: #If two images are selected
        try: #Exception handling
            comparison(file_paths[0], file_paths[1]) #Use the comparison function on path1 and path2
        except Exception as e: #If there is an exception
            messagebox.showerror("Error", f"Comparison Failed: {e}") #Show the following error with the reason for failure (e)
    else:
        messagebox.showerror("Error", f"Select EXACTLY TWO images.") #Otherise show this error message instead
        
###################################################################################################

#Least Significant Bit (LSB) Extraction for Channels
def lsb_extraction(path): #Defines the least significant bit extraction function with 
    img = Image.open(path).convert("RGBA") #Open the image from the path and convert it to RGBA format
    img_data = np.array(img) #Turns the selected image into an array

    red_lsb = (img_data[:, :, 0] & 1).flatten() #All rows, all columns, and first channel (red), binary for lsb and flatten
    green_lsb = (img_data[:, :, 1] & 1).flatten() #As above but second channel instead (green)
    blue_lsb = (img_data[:, :, 2] & 1).flatten() #As above but third channel instead (blue)

    return red_lsb, green_lsb, blue_lsb #Exits function with lsb values for eah channel

###################################################################################################

#Least Significant Bit (LSB) Heatmap
def lsb_heatmap(): #Defines the lsb heatmap function
    path = filedialog.askopenfilename() #For file selection
    image = Image.open(path).convert("RGBA") #opens the selected image from the path and converts it to RGB format
    img_array = np.array(image) #Give the 'image' variable an array using the NumPy Library 
    print("Image Shape =", img_array.shape) #Debugging: Prints the image array to the terminal
   
    if img_array.shape[-1] == 4: #If format is RGBA, cancel RGBA, enable RGB channels ONLY
        img_array = img_array[:, :, :3] #All rows, all columns, all channels
        
    grayscale = np.dot(img_array[..., :3], [0.3, 0.6, 0.1]) #Green (middle figure) is more pronounced, we are more sensitive to G than R or B
    lsb_data = grayscale.astype(int) & 1 #Least Significant Bit data as numerical greyscaled image
    
    if len(lsb_data.shape) == 3:   #If the image is 3D, covert it to 2D
        heatmap = lsb_data.sum(axis = 2) #If the image is already
    else:
        heatmap = lsb_data #Keep it 2D  
          
   
    plt.figure(figsize = (10, 6)) #Set the figure size to 10 x 6 inches
    plt.imshow(heatmap, cmap = "hot", interpolation="nearest") #Displays collected lsb data as an image
    plt.colorbar(label="Least Significant Bit (LSB) Intensity") #Labels axis
    plt.title("Least Significant Bit (LSB) Heatmap") #Gives heatmap a title
    plt.show() #Displays the heatmap in a seperate window

###################################################################################################

def chisquare_test(lsb_array): #Defines the chi square test detection logic feature
    observed = [np.sum(lsb_array == 0), np.sum(lsb_array == 1)] #Binary value for observed lsbs
    expected = [len(lsb_array) / 2] * 2 #Value for expected is (length of lsb arrays / 2) x 2
    chi_stat, p_value = chisquare(f_obs = observed, f_exp = expected) #scipy library used for f_obs (observed frequencies), f_exp (expected frequencies), and chisquare
    return chi_stat, p_value, observed #Exit function with chi square statistics, p-value, and observed frequencies

###################################################################################################

def detection(path): #Defines the detection function
    detection_box.delete('1.0', tk.END) #Refreshes detection box for next analysis
    red, green, blue = lsb_extraction(path) #each channel selected for extraction function
    channels = {"Red": red, "Green": green, "Blue": blue} #Defining each colour channel
    p_values = [] #p-value is empty for appending
    

    detection_box.insert(tk.END, f"Analysing image: {path}\n") #Displays following message and selected file path
    for name, channel in channels.items(): #For every name and channel in the amount of channels
        chi, p, obs = chisquare_test(channel) #use chi square test in all channels
        p_values.append(p) #set results as p-value
        detection_box.insert(tk.END, f"\nChannel: {name}\n") #Dsiplay channel name
        detection_box.insert(tk.END, f"Observed LSBs: {obs}\n") #Display Observed count results
        detection_box.insert(tk.END, f"Chi-Square: {chi:.2f}, p-value: {p:.4f}\n") #Display chi square and p-value results
    
    #Detecttion Results
    detection_box.insert(tk.END, "\nDetection Result:\n") #Display one of the following detection results
    p_value_count = sum(1 for p in p_values if p < 0.05) #In each cannel, p-value threshold is 0.05
    if p_value_count == 3: #If all 3 channels have p-value of below 0.05
        detection_box.insert(tk.END, "WARNING! Potential steganography detected!\n") #Flag Steagnography
        result = messagebox.askyesno("WARNING!", "Potential steganography detected! Would you like to quarantine this file?") #Incident notification for quarantining file
        if result: #If yes is selected on this popup
            quarantine(path) #Quarantine the file
    else: #Otherwiser
        detection_box.insert(tk.END, "All clear! No signs of steganography detected.\n") #Flag as non suspicious
            
###################################################################################################

#Hash Value Calculation Feature
def calculate_hash(file_path, hash_type): #Defines the function that calculates hash values with file location info and hash type from hashlib
    hash_func = None #Hash function is nothing until hash type is defined 
    if hash_type == 'md5': #If the hash type is md5
        hash_func = hashlib.md5() #The hash function will be for md5 in hashlib
    elif hash_type == 'sha1': #Or if the hash type is sha1
        hash_func = hashlib.sha1() #The hash function will be for sha1 in hashlib
    elif hash_type == 'sha256': #Or if the hash type is sha256
        hash_func = hashlib.sha256() #The hash function will be be fir sha256 in hashlib
    else:
        return None #Otherwise exit the function with nothing

    with open(file_path, 'rb') as f: #Opens the file located in binary mode (rb(read binary)) and calls it 'f'
        while chunk := f.read(8192): #Reads file selected in chunks of 8KB at a time
            hash_func.update(chunk) #Each 8KB chunk is fed into hash function with its respective hash (md5, sha1, etc)
    return hash_func.hexdigest() #After chunks are processed, exit with hexidecimal hash value.

###################################################################################################

#Metadata Extraction Feature
def metadata_extraction(file_path): #Defines metadata extraction function
    try: #Error/exception handling
        metadata = {} #Metadata is an open variable awaiting value
        file_type = magic.from_file(file_path, mime=True) #Reads file selected and determines MIME type using python magic library

        metadata['MD5 Hash'] = calculate_hash(file_path, 'md5') #Calculates and displays MD5 hash value
        metadata['SHA-1 Hash'] = calculate_hash(file_path, 'sha1') #Calculates and displays SHA1 hash value
        metadata['SHA-256 Hash'] = calculate_hash(file_path, 'sha256') #Calculates and displays SHA256 hash value
        metadata['MIME Filetype'] = file_type #Determines MIME file type and displays results

        if file_type.startswith('image/'): #if the MIME file type starts with 'image/'
            img = Image.open(file_path) #Open the selected image
            metadata['Format'] = img.format #Determine and display image format
            metadata['Resolution'] = img.size #Determine and display image resolution
            metadata['Mode'] = img.mode #Determine mode of the image (RGB, RGBA, L, etc)
            metadata['Colour Depth'] = img.getbands() #Determines and displays colour depth with PIL
            metadata['Colour Palette'] = img.getpalette() #Determines and displays colour palette with PIL
        else:
            metadata['Error'] = "Unsupported file type." #Otherwise the file is not supported so display an error message

        os_metadata = os.stat(file_path) #Restrieves stat result object containing further metadata about selected file
        metadata['Creation Time'] = datetime.datetime.fromtimestamp(os_metadata.st_birthtime) #Determines and displays file creation time
        metadata['Modification Time'] = datetime.datetime.fromtimestamp(os_metadata.st_mtime) #Determines and displays file modification time
        metadata['File Size'] = os_metadata.st_size #Determines and displays size of file in bytes

        return metadata #Exits function with all metadata information
    except Exception as e: #Exception handling, giving e the contents of the excpetion class (part of python standard library)
        messagebox.showerror(f"Error extracting metadata: {e}") #If there is an exception, display the following error message along with the explanation (e)
        return None #And exit the function with nothing 

###################################################################################################

#File Path Navigation for Individual Images
def file_selection(): #Defines the file selection function
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]) #Uses windows file explorer to locate the selected file, only image files can be selected
    if path: #If an image is selected
        
        # Display Image for Interface
        img = Image.open(path) #Open the image
        img.thumbnail((200, 200)) #Make the selected image a thumbnail 
        img_tk = ImageTk.PhotoImage(img) #Make the selected image TKinter compatible
        image_label.configure(image = img_tk) #Configure the image label 
        image_label.image = img_tk #Image label is using the PhotoImage package from TKinter library

        #Refresh Text Displays
        metadata_box.delete('1.0', tk.END) #Refreshes the metadata textbox
        detection_box.delete('1.0', tk.END) #Refreshes the detection box

        #Run Steganalysis Detection Method
        detection(path) #Defines the detection function with file selection as a parameter
        metadata = metadata_extraction(path) #Metadata extraction function is called back as 'metadata'
        if metadata: #If the metadata extraction function is called
            for key, value in metadata.items(): #For all keys and values in the metadata dictionary
                metadata_box.insert(tk.END, f"{key}: {value}\n") #Insert the actual keys and actual values into the metadata textbox
                
###################################################################################################

#Quarantine Setup
QUARANTINE = "quarantine" #For quarantine folder location/creation
KEY = "key.key" #For encryption/decryption key location
os.makedirs(QUARANTINE, exist_ok = True) #Make the quarantine folder if it doesnt exist

###################################################################################################

#Key Generator for Encryption
def get_key(): #Defines the function that 
    if os.path.exists(KEY): #If that path to the key file exists
        with open(KEY, "rb") as f: #Open that key as binary (rb(read binary))
            return f.read() #Exit by reading the key file
    else:
        key = Fernet.generate_key() #Otherwise generate the encryption key file
        with open(KEY, "wb") as f: #Open the file as binary (wb(write binary))
            f.write(key) #Write the encryption key file
        return key #Exit the function with the encryption key file

key = get_key() #Outside of this function, the get key function will be referred to  as 'key'
fernet = Fernet(key) #Fernet class used on key function to securely encrypt files

###################################################################################################

#File Encryption for Quarantining
def quarantine(path): #Defines the quarantine function
    try: #Exception handling
        with open(path, "rb") as f: #Open the the selected file in binary mode (rb(read binary))
            encrypted_file = fernet.encrypt(f.read()) #Use the Fernet class to encrypt the selected file
        
        file = os.path.basename(path) #Extracts the file name from the selected file path
        quarantine_path = os.path.join(QUARANTINE, file + ".enc") #Location for encrypted quarantine files (.enc) after encryption
        with open(quarantine_path, "wb") as f: #Opens this path in binary (wb(write binary))
            f.write(encrypted_file) #Write the encrypted file
        
        os.remove(path) #Remove the original fle
        messagebox.showinfo("Quarantine", f"{file} has been successful quarantined.") #Display successful encryption message  
    except Exception as e: #Exception handling with exception as 'e'
        messagebox.showerror("Error", str(e)) #Show the folling error message with the correct exception explanation (e)
        
###################################################################################################

#File Decryption for Quarantine Restoration
def file_restore(path): #Defines the file recovery function
    try: #Exception handling
        file = os.path.basename(path).replace(".enc", "") #Replace encrypted files (.enc)
        destination = filedialog.asksaveasfilename(initialfile = file) #New file path saving for recovered file
        
        if not destination: #When the new file destination is chosen 
            return #Exit the function by
        with open(path, "rb") as f: #Opening the file in binary (rb(read binary))
            decrypted_file = fernet.decrypt(f.read()) #Decrypt the file
        with open(destination, "wb") as f: #Open the file again in binary (wb(write binary))
            f.write(decrypted_file) #Write as decrypted file
        os.remove(path) #Remove the original path (when it was encrypted)
        messagebox.showinfo("Quarantine", f"{file} has been successfully recovered") #Show success message
    except Exception as e: #Exception handling with exception as e
        messagebox.showerror("Error", str(e)) #Show error message with explanation of exception (e)
        
###################################################################################################

#View All StegBuster Quarantined Files
def open_quarantine(): #Defines the function that allows for viewing quarantined files
    quarantined_files = os.listdir(QUARANTINE) #List the files in the quarantine directory 
    if not quarantined_files: #If there are no quarantined files
        messagebox.showinfo("StegBuster File Quarantine", "There are no quarantined files.") #Display the message saying the folder is empty
        return #Exit the function

    win = tk.Toplevel(root) #Opens a new window for the quarantine vault
    win.title("StegBuster Quarantine Vault") #Names the new window

    for filename in quarantined_files: #For every filename among the quarantined files
        quarantine_path = os.path.join(QUARANTINE, filename) #Join the filenames and the quarantine directory
        btn = tk.Button(win, text = filename, command = lambda f = quarantine_path: recover_file(f)) #Creates a button for every filename in the new window
        btn.pack(fill = "x", padx = 10, pady = 5) #Fill the buttons to the window with 10 x 5 padding
        
###################################################################################################

#File Recovery Path Location
def recover_file(path): #Defines the recovery path location function
    file = os.path.basename(path).replace(".enc", "") #Replace the selected encrypted file (.enc) with nothing
    confirm = messagebox.askyesno("Recover File", f"Do you want to recover '{file}'?") #Displays confirmation box with answers yes or no
    if confirm: #If the answer is yes
        file_restore(path) #Restore the selected file
     
###################################################################################################

#TKinter Button Management: All buttons have 20 width and 5 vertical padding within root application (home)
Button(button_frame, text = "Scan Image", width = 20, command = file_selection).pack(pady = 5) #Button for scanning individual images
Button(button_frame, text = "Compare Two Images", width = 20, command=open_image_comparison).pack(pady = 5) #Button for comparing the differences between two images
Button(button_frame, text = "Generate LSB Heatmap", width = 20, command = lsb_heatmap).pack(pady = 5) #Button for generating a least significant bit heatmap for individual images (greyscale)
Button(button_frame, text = "View Quarantine", width = 20, command = open_quarantine).pack(pady = 5) #Button for accessing the quarantined files, can access file recovery in here too
Button(button_frame, text = "Quit", width = 20, command = root.quit).pack(pady = 5) #Button that exits application

###################################################################################################

# Start TKinter User Interface Mainloop and Console Debugging
root.protocol("WM_DELETE_WINDOW", lambda: (print("StegBuster closing..."), root.destroy())) #Closing error unfixed within .destroy, closing printed on console to show application attempt in closing
print("Starting Application...") #Printed on console to show application attempt in starting
root.mainloop() #Main application loop
print("Application Closed.") #Printed on console top show application has successfully closed
