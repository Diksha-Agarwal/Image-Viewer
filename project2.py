import sqlite3
import PIL.ImageTk
import PIL.Image
from PIL import ImageEnhance
from PIL import ImageFilter
from tkinter import *
import tkinter.font as font
from tkinter import filedialog
import cv2
from tkinter.simpledialog import askinteger, askfloat

root = Tk()
root.iconbitmap('Icon.ico')
#root.geometry("340x433")
root.title('IMAGE VIEWER')  # TITLE OF THE APPLICATION
root.configure(bg="#d6eaf8") # BG COLOR OF THE APP
myFont = font.Font(family='Comic Sans MS') 

# CONNECTING TO THE DATABASE
conn = sqlite3.connect('images.db')
cursor = conn.cursor()

image_list = list()
imagefile_list = list()
# CREATING A STATUS BAR
status = Label(root, text="Image 1 of " + str(len(image_list)), bd=1, relief=SUNKEN, anchor=E, bg="#34495e", fg="white")

# CREATING TABLE IN THE DATABASE
try:
	cursor.execute("CREATE TABLE image(image_name text, image_file blob)")
except:
	print("Table exists")


# FUCTION FOR SUBMITTING ADDES IMAGE TO THE DB
def submitting_image_to_DB(image_file):
	conn = sqlite3.connect('images.db')
	cursor = conn.cursor()
	#add_image()
	cursor.execute("INSERT INTO image VALUES ('image', :image_file)",
			{
				'image_file' : image_file
			}

		)
	x = imagefile_list[len(imagefile_list)-1]
	display_added_image(x)


	conn.commit()
	conn.close()

# FUNCTION FOR DISPLAYING THE ADDED IMAGES
def display_added_image(image):
	global img
	img = PIL.Image.open(image)
	img = img.resize((300,350), PIL.Image.ANTIALIAS)
	img1 = PIL.ImageTk.PhotoImage(img)
	image_list.append(img1)

# FUNCTON FOR ADDING IMAGE TO THE IMAGE VIEWER
def add_image():
	global image
	root.filename = filedialog.askopenfilename(initialdir="File Explorer", title="Select image file", filetypes=(("jpeg files", "*.jpeg"), ("png files", "*.png"), ("jpg files", "*.jpg"), ("all files", "*.*")))
	image = root.filename
	imagefile_list.append(image)
	submitting_image_to_DB(image)

# FUNCTION TO START THE EXECUTION
def execute():
	conn = sqlite3.connect('images.db')
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT rowid, * from image")

		items = cursor.fetchall()
		for item in items:
			x = item[2]
			#print(x)
			imagefile_list.append(x)
			img = PIL.Image.open(x)
			img = img.resize((300,350), PIL.Image.ANTIALIAS)
			img1 = PIL.ImageTk.PhotoImage(img)
			image_list.append(img1)

	except:
		print('Image files not found')
		

#************************* BEGINNING OF THE CODE EXECUTION *****************************
execute()
if len(image_list) != 0:
	label = Label(root, image=image_list[0])
	label.grid(row=0, column=0, columnspan=4, rowspan=1)

# FUNCTION TO MAKE FORWARD BUTTON WORK
def forward_button(img_num):
	global label
	global forward
	global back

	label.grid_forget()
	label = Label(image=image_list[img_num-1])
	forward = Button(root, text=">>", command = lambda: forward_button(img_num+1), bg="#aed6f1", font=myFont)
	back = Button(root, text="<<", command=lambda: back_button(img_num - 1), bg="#aed6f1", font=myFont)

	if img_num == len(image_list):
		forward = Button(root, text=">>", state=DISABLED, bg="#aed6f1", font=myFont)

	label.grid(row=0, column=0, columnspan=4, rowspan=1)
	forward.grid(row=1, column=3)
	back.grid(row=1, column=0)

	# STATUS BAR
	status = Label(root, text="Image " + str(img_num) + " of " + str(len(image_list)), bd=1, relief=SUNKEN, anchor=E, bg="#34495e", fg="white")
	status.grid(row=3, column=0, columnspan=4, sticky=W + E)

# FUNCTION TO MAKE BACKWARD BUTTON WORK
def back_button(img_num):
	global label
	global forward
	global back

	label.grid_forget()
	try:
		label = Label(image=image_list[img_num-1])
	except:
		print('NO MORE IMAGES')

	back = Button(root, text="<<", command=lambda:back_button(img_num-1), bg="#aed6f1", font=myFont)
	forward = Button(root, text=">>", command=lambda: forward_button(img_num+1), bg="#aed6f1", font=myFont)

	if img_num == 1 or img_num == 0:
		back = Button(root, text="<<", state=DISABLED, bg="#aed6f1", font=myFont)

	label.grid(row=0, column=0, columnspan=4, rowspan=1)
	back.grid(row=1, column=0)
	forward.grid(row=1, column=3)

	# STATUS BAR
	status = Label(root, text="Image " + str(img_num) + " of " + str(len(image_list)), bd=1, relief=SUNKEN, anchor=E, bg="#34495e", fg="white")
	status.grid(row=3, column=0, columnspan=4, sticky=W + E)

# FUNCTION TO CONVERT IMAGE TO BLACK & WHITE
def convert_to_grayscale():
    global img
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    x = askinteger('input', 'Enter image number of the image')  # DISPLAYS A DIALOG BOX TO ENTER THE IMAGE NUMBER
    img = cv2.imread(imagefile_list[x-1])
    converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Image', converted_img)
    k = cv2.waitKey(0) #& 0xFF
    # saving b/w image
    if k==27:
        cv2.destroyAllWindows()

    elif k == ord('s'):
    	items = imagefile_list[x-1].split("/")
    	y = (items[len(items)-1]).split(".")
    	z = y[0] + "BW." + y[1]

    	cv2.imwrite(z, converted_img)
    	cv2.destroyAllWindows()

    conn.commit()
    conn.close()

# FUNCTION TO CONVERT IMAGE TO PNG
def convert_to_png():
    global image
    x = askinteger('input', 'Enter image number of the image')
    image = cv2.imread(imagefile_list[x-1])
    y = imagefile_list[x-1].split("/")
    z = y[len(y)-1].split('.')
    file_name = z[0] + '.png'
    cv2.imwrite(file_name, image)
    cv2.destroyAllWindows()

# FUNCTION TO CONVERT IMAGE TO JPEG
def convert_to_jpeg():
    global image
    x = askinteger('input', 'Enter image number of the image')
    image = cv2.imread(imagefile_list[x-1])
    y = imagefile_list[x-1].split("/")
    z = y[len(y)-1].split('.')
    file_name = z[0] + '.jpeg'
    cv2.imwrite(file_name, image)
    cv2.destroyAllWindows()

# FUNCTION TO CONVERT IMAGE TO JPG
def convert_to_jpg():
    global image
    x = askinteger('input', 'Enter image number of the image')
    image = cv2.imread(imagefile_list[x-1])
    y = imagefile_list[x-1].split("/")
    z = y[len(y)-1].split('.')
    file_name = z[0] + '.jpg'
    cv2.imwrite(file_name, image)
    cv2.destroyAllWindows()

# FUNCTION TO CONVERT IMAGE TO BITMAP
def convert_to_bmp():
    global image
    x = askinteger('input', 'Enter image number of the image')
    image = cv2.imread(imagefile_list[x-1])
    y = imagefile_list[x-1].split("/")
    z = y[len(y)-1].split('.')
    file_name = z[0] + '.bmp'
    cv2.imwrite(file_name, image)
    cv2.destroyAllWindows()

def convert_to_tiff():
    global image
    x = askinteger('input', 'Enter image number of the image')
    image = cv2.imread(imagefile_list[x-1])
    y = imagefile_list[x-1].split("/")
    z = y[len(y)-1].split('.')
    file_name = z[0] + '.tiff'
    cv2.imwrite(file_name, image)
    cv2.destroyAllWindows()

def convert_to_dib():
    global image
    x = askinteger('input', 'Enter image number of the image')
    image = cv2.imread(imagefile_list[x-1])
    y = imagefile_list[x-1].split("/")
    z = y[len(y)-1].split('.')
    file_name = z[0] + '.dib'
    cv2.imwrite(file_name, image)
    cv2.destroyAllWindows()

# FUNCTION TO MAKE AN IMAGE ROTATE
def rotating():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	theta = askfloat('input', 'Enter the angle to be rotated(anti-clockwise)')
	rotate_img = image.rotate(theta, expand=True, fillcolor="white").show()
	
# FUNCTION TO RESIZE AN IMAGE
def resize():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	height = askinteger('input', 'Mention height')
	width = askinteger('input', 'Mention width')
	image = image.resize((height,width), PIL.Image.ANTIALIAS)
	img1 = image.show()


#ENHANCING OPTIONS
def image_contrast():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	img_con = ImageEnhance.Contrast(image)
	y = askfloat('input', 'Enter the contrast you want between 0 & 1')
	img_con.enhance(y).show("contrast")

def image_brightness():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	img_con = ImageEnhance.Brightness(image)
	y = askfloat('input', 'Enter the brightness you want between 0 & 1')
	img_con.enhance(y).show("brightness")

def image_color():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	img_con = ImageEnhance.Color(image)
	y = askfloat('input', 'Enter the color balance you want between 0 & 1')
	img_con.enhance(y).show()

def image_sharpness():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	img_con = ImageEnhance.Sharpness(image)
	y = askfloat('input', 'Enter the sharpness you want between 0 & 2')
	img_con.enhance(y).show()


# FILTER OPTIONS
def blur_image():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	enc_img = image.filter(ImageFilter.BLUR)
	enc_img.show()

def edgeEnhance_image():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	enc_img = image.filter(ImageFilter.EDGE_ENHANCE)
	enc_img.show()

def edgeEnhanceMore_image():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	enc_img = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
	enc_img.show()

def contour_image():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	enc_img = image.filter(ImageFilter.CONTOUR)
	enc_img.show()

def emboss_image():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	enc_img = image.filter(ImageFilter.EMBOSS)
	enc_img.show()

def find_edges_image():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	enc_img = image.filter(ImageFilter.FIND_EDGES)
	enc_img.show()

def smooth_image():
	global image
	x = askinteger('input', 'Enter image number of the image')
	image = PIL.Image.open(imagefile_list[x-1])
	enc_img = image.filter(ImageFilter.SMOOTH_MORE)
	enc_img.show()

# FUNCTION TO DELETE AN IMAGE
def delete_image():
	conn = sqlite3.connect('images.db')
	cursor = conn.cursor()
	cursor.execute("SELECT rowid from image")
	rowid_list = cursor.fetchall()
	#print(rowid_list)
	x = askinteger('input', 'Enter image number to delete')
	y = str(rowid_list[x-1][0])
	cursor.execute("DELETE FROM image WHERE rowid=" + y)
	conn.commit()
	conn.close()

#CREATING MENUS
my_menu = Menu(root)
root.config(menu=my_menu)

# EDIT MENU
edit_menu = Menu(my_menu, tearoff = 0, activebackground='#d7bde2', bg="#f5eef8")
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="rotate", command=rotating)
edit_menu.add_command(label="resize", command=resize)

# OPTIONS MENU
option_menu = Menu(my_menu, tearoff = 0, activebackground='#d7bde2', bg="#f5eef8")
my_menu.add_cascade(label="Options", menu=option_menu)
option_menu.add_command(label="B/W", command=convert_to_grayscale)
option_menu.add_command(label="PNG", command=convert_to_png)
option_menu.add_command(label="JPEG", command=convert_to_jpeg)
option_menu.add_command(label="JPG", command=convert_to_jpg)
option_menu.add_command(label="Bitmap", command=convert_to_bmp)
option_menu.add_command(label="dib", command=convert_to_dib)
option_menu.add_command(label="TIFF", command=convert_to_tiff)

# ENHANCEMENTS MENU
Enhancements_menu = Menu(my_menu, tearoff = 0, activebackground='#d7bde2', bg="#f5eef8")
my_menu.add_cascade(label="Enhancements", menu=Enhancements_menu)
Enhancements_menu.add_command(label="contrast", command=image_contrast)
Enhancements_menu.add_command(label="brightness", command=image_brightness)
Enhancements_menu.add_command(label="color balance", command=image_color)
Enhancements_menu.add_command(label="sharpness", command=image_sharpness)

# FILTERS MENU
filter_menu = Menu(my_menu, tearoff = 0, activebackground='#d7bde2', bg="#f5eef8")
my_menu.add_cascade(label="Filters", menu=filter_menu)
filter_menu.add_command(label="blur", command=blur_image)
filter_menu.add_command(label="Edge Enhance", command=edgeEnhance_image)
filter_menu.add_command(label="more edge Enhance", command=edgeEnhanceMore_image)
filter_menu.add_command(label="Contour", command=contour_image)
filter_menu.add_command(label="Emboss", command=emboss_image)
filter_menu.add_command(label="edge Detection", command=find_edges_image)
filter_menu.add_command(label="smooth", command=smooth_image)

#VARIOUS BUTTONS
add_image_btn = Button(root, text="Add", command=add_image, bg="#aed6f1", font=myFont) # IMAGE ADDING BUTTON
forward = Button(root, text=">>", command=lambda: forward_button(1), bg="#aed6f1", font=myFont) # FORWARD BUTTON
back = Button(root, text="<<", command=lambda:back_button(1), bg="#aed6f1", font=myFont) # BACK BUTTON
delete_button = Button(root, text="delete", command=delete_image, bg="#aed6f1", font=myFont) # DELETE BUTTON

# DISPLAYING ALL THE BUTTONS ON THE SCREEN INCLUDING STATUS BAR
add_image_btn.grid(row=1, column=1)
forward.grid(row=1, column=3, pady=10)
back.grid(row=1, column=0)
status.grid(row=3, column=0, columnspan=4, sticky=W+E)
delete_button.grid(row=1, column=2)


#cursor.execute("SELECT rowid, * FROM image")
#print(cursor.fetchall())


# Commit our command
conn.commit()

# Closing our connection
conn.close()
root.mainloop()