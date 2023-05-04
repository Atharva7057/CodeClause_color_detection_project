import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
import cv2
import pandas as pd

root=Tk()
root.title("color detector")
root.geometry("800x470+100+100")
root.configure(bg="#e4e8eb")
root.resizable(False,False)
csv_path = 'colors.csv'

# reading csv file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)


#declaring global variables
r = g = b = 0

#function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R,G,B):
	minimum = 1000
	for i in range(len(df)):
		d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name']

	return cname

# Function to Open the folder and select the image 
def open_file():
    global filepath,img,copyimg
    filepath = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                          filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    img = Image.open(filepath)
    resized_image = img.resize(( 315,275))
    copyimg = cv2.imread(filepath)
    copyimg = cv2.resize(copyimg, (315,275))
    img = ImageTk.PhotoImage(resized_image)
    lbl.configure(image=img,width=300,height=260)
    lbl.image = img  
    
def draw_function(event):
    x, y = event.x,event.y
    b,g,r =copyimg[y,x]
    b = int(b)
    g = int(g)
    r = int(r)
    

    #Creating text string to display( Color name and RGB values )
    text = get_color_name(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
   
    #This label contains color name
    label = tk.Label(frame, text=text,width=35,)
    label.place(x=10,y=10)


    
Label(root,width=220,height=10,bg="#4272f9").pack()

#Frame
Frame=Frame(root,width=700,height=370,bg="#fff")
Frame.place(x=50,y=50)

Label(Frame,text="Color Detector",font="arial 14 bold",bg="white").place(x=20,y=10)


innerframe = tk.Frame(root, width=300, height=300, bd=1, relief=tk.SOLID)
innerframe.place(x=250,y=100)

frame = tk.Frame(root, width=280, height=250, bd=1, relief=tk.SOLID, bg="black")
frame.place(x=260,y=110)
lbl=Label(frame,bg="black")
lbl.place(x=0,y=0)
lbl.bind("<Button-1>", draw_function)

#Button
button = tk.Button(root, text='Select image',font="arial 10 bold",bd=1,command=open_file)
button.place(x=350,y=365)


root.mainloop()
