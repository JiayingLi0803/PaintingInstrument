from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox as MessageBox
from random import *
from tkinter.ttk import Separator
from PIL import Image, ImageDraw
from musicpy import *
import numpy as np
import time


def to_rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

global pointlist0, pointlist1, pointlist2, pointlist3, pointlist4
pointlist0, pointlist1, pointlist2, pointlist3, pointlist4 = [], [], [], [], []
def paint( event ):
    global cl
    if opVar.get() == 0: # circle
        cl=[]
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )

        colorxxx = to_rgb((x1+y1)//9, x1//10, y1//3)
        w.create_oval( x1, y1, x2, y2, fill = colorxxx)
        draw.ellipse([x1, y1, x2, y2], fill = colorxxx)
        pointlist0.append([x1, y1])
    elif opVar.get() == 1: # Line
        cl=[]
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )
        colorxxx = to_rgb((x1+y1)//9, y1//3, x1//10)
        w.create_line(x1, y1, x2, y2, fill = colorxxx)
        draw.line([x1, y1, x2, y2], fill=colorxxx,  width=scaleVar.get())
        pointlist1.append([x1, y1])
    elif opVar.get() == 2: # Square
        cl=[]
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )
        colorxxx = to_rgb((x1+y1)//9, x1//6, y1//5)
        w.create_rectangle( x1, y1, x2, y2, fill = colorxxx)
        draw.rectangle([x1, y1, x2, y2], fill = colorxxx)
        pointlist2.append([x1, y1])
    elif opVar.get() == 3: # Star
        x1, y1 = (event.x - scaleVar.get()), (event.y)
        x2, y2 = (event.x - scaleVar.get()//4), (event.y - scaleVar.get()//4)
        x3, y3 = (event.x), (event.y - scaleVar.get())
        x4, y4 = (event.x + scaleVar.get()//4), (event.y - scaleVar.get()//4)
        x5, y5 = (event.x + scaleVar.get()), (event.y)
        x6, y6 = (event.x + scaleVar.get()//4), (event.y + scaleVar.get()//4)
        x7, y7 = (event.x), (event.y + scaleVar.get())
        x8, y8 = (event.x - scaleVar.get()//4), (event.y + scaleVar.get()//4)
        points = [x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8]
        colorxxx = to_rgb((x1+y1)//9, x1//8, y1//4)
        w.create_polygon(points, fill = colorxxx)
        draw.polygon([x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8],fill=colorxxx)
        pointlist4.append([x1, y1])
    elif opVar.get() == 4: # Random
        rand_num = randint(0,1)
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )
        colorxxx = to_rgb((x1+y1)//9, x1//14, y1//6)
        if rand_num == 0:
            rand_shape = w.create_oval( x1, y1, x2, y2, fill = colorxxx)
            draw.ellipse([x1, y1, x2, y2], fill = colorxxx)
        else:
            rand_shape = w.create_rectangle( x1, y1, x2, y2, fill = colorxxx)
        def movement(dx, dy):
            x1_1, y1_1, x2_1, y2_1 = list(map(int, w.coords(rand_shape))) 

            if (x1_1 <= 0 and dx < 0) or (x2_1 >= canvas_width and dx > 0): 
                
                dx = -dx
            elif (y1_1 <= 0 and dy < 0) or (y2_1 >= canvas_height and dy > 0): 
                dy = -dy
            w.move(rand_shape, dx, dy)
            w.after(25, movement, dx, dy) 
            draw.ellipse([x1_1, y1_1, x2_1, y2_1], fill = color[0], outline = color_outline[0])
        movement(randint(-15, 15), randint(-15, 15)) 


def findparas(points, listtype, total_piece_time):
    sort_point = points[np.argsort(points[:,0])]
    unique_points = points[np.unique(points[:,0]//10,axis=0,return_index=True)[1]]
    x = unique_points[:,0]//10
    y = unique_points[:,1]
    timelist = np.zeros(150)
    chordlist = []
    for i in set(x):
        timelist[i] = 1
    onesrange = np.argwhere(timelist == 1).flatten()
    starttime = onesrange[0]
    intervallist = np.zeros(len(onesrange))
    for i in range(len(onesrange)):
        if i!=len(onesrange)-1:
            intervallist[i] = onesrange[i+1]-onesrange[i]
        else:
            intervallist[i] = 150-onesrange[i]
    for yval in y:
        chordlist.append(decideNote(yval, listtype))
    if scaleVar.get() >= 40:
        brushvolume = 100
    else:
        brushvolume = scaleVar.get()+60
    return starttime, (intervallist/(300/total_piece_time)).tolist(), chordlist, brushvolume
def decideNote(y, listtype):
    classy = 0
    interval = 150/7
    octave = 6- y//150
    y = y%150
    for i in range(1,7):
        if y>=interval*i and y<=interval*(i+1):
            classy = i
    return listtype[classy]+str(octave)


def play_button_event(): #play piece
    tracklist, instrumentlist, startTimelist = [], [], []
    getkeylist()
    getPieceTime()
# C1 = chord(['C5','E5', 'G5', 'B5'], interval=[0.5, 0.5, 0, 2], duration=[1, 2, 0.5, 1])
    if pointlist0:
        starttime0, intervallist0, chordlist0, brushvolume0 = findparas(np.array(pointlist0), givenkey, total_piece_time)
        C0 = chord(chordlist0, interval = intervallist0)
        C0.setvolume(brushvolume0)
        tracklist.append(C0)
        instrumentlist.append(20)
        startTimelist.append(starttime0)
    if pointlist1:
        starttime1, intervallist1, chordlist1, brushvolume1 = findparas(np.array(pointlist1), givenkey, total_piece_time)
        C1 = chord(chordlist1, interval = intervallist1)
        C1.setvolume(brushvolume1)
        tracklist.append(C1)
        instrumentlist.append(25)
        startTimelist.append(starttime1)
    if pointlist2:
        starttime2, intervallist2, chordlist2, brushvolume2 = findparas(np.array(pointlist2), givenkey, total_piece_time)
        C2 = chord(chordlist2, interval = intervallist2)
        C2.setvolume(brushvolume2)
        tracklist.append(C2)
        instrumentlist.append(46)
        startTimelist.append(starttime2)
    if pointlist3:
        starttime3, intervallist3, chordlist3, brushvolume3 = findparas(np.array(pointlist3), givenkey, total_piece_time)
        C3 = chord(chordlist3, interval = intervallist3)
        C3.setvolume(brushvolume3)
        tracklist.append(C3)
        instrumentlist.append(108)
        startTimelist.append(starttime3)
    if pointlist4:
        starttime4, intervallist4, chordlist4, brushvolume4 = findparas(np.array(pointlist4), givenkey, total_piece_time)
        C4 = chord(chordlist4, interval = intervallist4)
        C4.setvolume(brushvolume4)
        tracklist.append(C4)
        instrumentlist.append(109)
        startTimelist.append(starttime4)
    my_piece = piece(tracks = tracklist, instruments = instrumentlist, bpm = 120, start_times = startTimelist)
    play(my_piece)
    #time.sleep(total_piece_time)
    #print("end")
def pause_event():
    stopall()


def save():
    image1.save('paintingpy_image.png')
    MessageBox.showinfo(title = 'Saved', message = 'File Saved as: paintingpy_image.png')
def clear():
    global pointlist0, pointlist1, pointlist2, pointlist3, pointlist4
    pointlist0, pointlist1, pointlist2, pointlist3, pointlist4 = [], [], [], [], []
    w.delete(ALL)
    wid = image1.width
    h = image1.height
    draw.rectangle([0, 0, wid, h], fill = "black", width = 0)
    init_label = Label(mylabelframe, text = "   ")
    init_label.grid(row = 1, column = 12)
    # You would normally put that on the App class
    def show_error(self, *args):
        pass
    # but this works too
    Tk.report_callback_exception = show_error
def grid_on():
    for i in range(50):
        w.create_line(0,int(1500/50*i),1500,int(1500/50*i),fill='grey',width=1)
        w.create_line(int(1500/50*i),0,int(1500/50*i),600,fill='grey',width=1)
    w.create_line(0,300,1500,300,fill='red',width=1)


givenkey = ["C", "D", "E", "F", "G", "A", "B"]
def getkeylist():
    global givenkey
    if keyVar.get() == "C":
        givenkey = ["C", "D", "E", "F", "G", "A", "B"]
    elif keyVar.get() == "D":
        givenkey = ["D", "E", "F#", "G", "A", "B", "C#", "D"]
    elif keyVar.get() == "E":
        givenkey = ["E", "F#", "G#", "A", "B", "C#", "D#"]
    elif keyVar.get() == "F":
        givenkey = ["F", "G", "A", "Bb", "C", "D", "E"]
    elif keyVar.get() == "G":
        givenkey = ["G", "A", "B", "C", "D", "E", "F#"]
    elif keyVar.get() == "A":
        givenkey = ["A", "B", "C#", "D", "E", "F#", "G#"]
    elif keyVar.get() == "B":
        givenkey = ["B", "C#", "D#", "E", "F#", "G#", "A#"]
    elif keyVar.get() == "B":
        givenkey = ["B", "C#", "D#", "E", "F#", "G#", "A#"]
    elif keyVar.get() == "C#":
        givenkey = ["C#", "D#", "F", "F#", "G#", "A#", "C"]
    elif keyVar.get() == "D#":
        givenkey = ["D#", "F", "G", "G#", "A#", "C", "D"]
    elif keyVar.get() == "F#":
        givenkey = ["F#", "G#", "A#", "B", "C#", "D#", "F"]
    elif keyVar.get() == "G#":
        givenkey = ["G#", "A#", "C", "C#", "D#", "F", "G"]
    elif keyVar.get() == "A#":
        givenkey = ["A#", "C", "D", "Eb", "F", "G", "A"]

total_piece_time = 10
def getPieceTime():
    global total_piece_time
    total_piece_time = int(timeVar.get())


## --- MAIN --- ##
root = Tk()
root.title( "Painting Instrument" )
root.resizable(False,False)

# Variables
opVar = IntVar()
scaleVar = IntVar()
fillVar = IntVar()
keyVar = StringVar()
timeVar = StringVar()

canvas_width = 1500
canvas_height = 600

cl = []

pointlist0, pointlist1, pointlist2, pointlist3, pointlist4 = [], [], [], [], []

font_1 = ("Times", "14", "bold italic")
font_2 = ("Times", "12", "bold")
font_3 = ("Helvetica", "12", "bold")

# CANVAS
w = Canvas(root, width = canvas_width, height = canvas_height)

w.config(bg = '#000')

w.pack(expand = 1, fill = 'both')

w.bind("<B1-Motion>", paint )
w.bind("<Button-1>", paint )


# Img in PIL. It is not displayed, it is used to save the image.
image1 = Image.new("RGB", (canvas_width, canvas_height), 'black')
draw = ImageDraw.Draw(image1)


## Labels and Tools
# LabelFrame 1

mylabelframe = LabelFrame(root, text = 'Tools', font=font_1)
mylabelframe.pack(fill = 'both',expand = 1, ipadx = 10, ipady = 10, padx = 8, pady = 5)


scale = Scale(mylabelframe, variable = scaleVar, orient = 'horizontal', from_ = 0, to = 100, label = 'Brush Size', length = 300, repeatdelay = 500, relief = 'sunken', sliderlength = 25)
scale.grid(row = 0, column = 0, columnspan = 3)

oval_brush = Radiobutton(mylabelframe, text = 'Circle Brush', variable = opVar, value = 0, font = font_2).grid(row = 1, column = 0, sticky = 'w')
line_brush = Radiobutton(mylabelframe, text = 'Line Brush', variable = opVar, value = 1, font = font_2).grid(row = 2, column = 0, sticky ='w')
rectangle = Radiobutton(mylabelframe, text = 'Square Brush', variable = opVar, value = 2, font = font_2).grid(row = 3, column = 0, sticky = 'w')
star = Radiobutton(mylabelframe, text = 'Star Brush', variable = opVar, value = 3, font = font_2).grid(row = 1, column = 1, sticky = 'w')
random_move = Radiobutton(mylabelframe, text = 'Random Brush', variable = opVar, value = 4, font = font_2).grid(row = 2, column = 1, sticky = 'w')


# Save and Clear
sep_2 = Separator(mylabelframe, orient = 'vertical').grid(row = 0, column = 4, rowspan = 4,sticky = 'ns', padx = 25)

# Grid on
grid_on_button = Button(mylabelframe, text="Grid on", compound = 'left', padx = 8, pady = 5, font = font_3)
grid_on_button.grid(row = 3, column = 1, sticky = 'w')
grid_on_button.config(command = grid_on)


save_button = Button(mylabelframe, text='Save', compound = 'left', padx = 8,pady = 5, font = font_3)
save_button.grid(row = 1, column = 5)
save_button.config(command = save)

clear_button = Button(mylabelframe, text='Clear', compound = 'left', padx = 4, pady = 5, font = font_3)
clear_button.grid(row = 3, column = 5, sticky = 'w')
clear_button.config(command = clear)

# Music Generator
play_button = Button(mylabelframe, text="Play your music", compound = 'left', padx = 8, pady = 5, font = font_3)
play_button.grid(row = 0, column = 8)
play_button.config(command = play_button_event)

stop_button = Button(mylabelframe, text="Stop", compound = 'left', padx = 8, pady = 5, font = font_3)
stop_button.grid(row = 1, column = 8)
stop_button.config(command = pause_event)


# dropown select
sep_3 = Separator(mylabelframe, orient = 'vertical').grid(row = 0, column = 6, rowspan = 4,sticky = 'ns', padx = 25)

# Select time
timechoices = {"5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100", "105", "110", "115", "120"}
timeVar.set('30') # set the default option
timeMenu = OptionMenu(mylabelframe, timeVar, *sorted(timechoices))
timeMenu.grid(row = 0, column =7)

# Select key
keychoices = {'C','C#','D','D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'}
keyVar.set('C') # set the default option
keyMenu = OptionMenu(mylabelframe, keyVar, *sorted(keychoices))
keyMenu.grid(row = 1, column =7)

root.mainloop()
