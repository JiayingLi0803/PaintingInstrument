from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox as MessageBox
from random import *
from tkinter.ttk import Separator
from PIL import Image, ImageDraw
from musicpy import *
import numpy as np

def choose_color():
    global color
    color = askcolor()
    color_button.config(bg = color[1])
def outline_color():
    global color_outline
    color_outline = askcolor()
    color_outline_button.config(bg = color_outline[1])

global pointlist0, pointlist1, pointlist2, pointlist3, pointlist4
pointlist0, pointlist1, pointlist2, pointlist3, pointlist4 = [], [], [], [], []
def paint( event ):
    global cl
    if opVar.get() == 0: # circle
        cl=[]
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )
        
        if fillVar.get() == 0:
            w.create_oval( x1, y1, x2, y2, fill = color[1], outline = color_outline[1])
            draw.ellipse([x1, y1, x2, y2], fill = color[0], outline = color_outline[0])
        else:

            w.create_oval( x1, y1, x2, y2, fill = None, outline = color_outline[1])
            draw.ellipse([x1, y1, x2, y2], fill = None, outline = color_outline[0])   
        pointlist0.append([x1, y1])
    elif opVar.get() == 1: # Line
        cl=[]
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )

        w.create_line(x1, y1, x2, y2, fill = color[1])
        draw.line([x1, y1, x2, y2], fill=color[0],  width=scaleVar.get())
        pointlist1.append([x1, y1])
    elif opVar.get() == 2: # Square
        cl=[]
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )
        if fillVar.get() == 0:
            w.create_rectangle( x1, y1, x2, y2, fill = color[1],outline = color_outline[1])
            draw.rectangle([x1, y1, x2, y2], fill = color[0], outline = color_outline[0])
        else:
            w.create_rectangle( x1, y1, x2, y2, fill = None,outline = color_outline[1])
            draw.rectangle([x1, y1, x2, y2], fill = None, outline = color_outline[0])
        pointlist2.append([x1, y1])
    elif opVar.get() == 3: # Polygon
        if len(cl)<4:
                cl.append(event.x)
                cl.append(event.y)
                try:
                        w.create_line(cl[0],cl[1],cl[2],cl[3], fill = color[1])
                        draw.line([cl[0],cl[1],cl[2],cl[3]], fill = color[0])
                except:
                        pass
        elif len(cl) == 4:
                w.create_line(cl[0],cl[1],cl[2],cl[3], fill = color[1])
                draw.line([cl[0],cl[1],cl[2],cl[3]], fill = color[0])
                cl = [cl[2],cl[3]]
                cl.append(event.x)
                cl.append(event.y)
                try:
                        w.create_line(cl[0],cl[1],cl[2],cl[3], fill = color[1])
                        draw.line([cl[0],cl[1],cl[2],cl[3]], fill = color[0])
                except:
                        pass
    elif opVar.get() == 4: # Star
        x1, y1 = (event.x - scaleVar.get()), (event.y)
        x2, y2 = (event.x - scaleVar.get()//4), (event.y - scaleVar.get()//4)
        x3, y3 = (event.x), (event.y - scaleVar.get())
        x4, y4 = (event.x + scaleVar.get()//4), (event.y - scaleVar.get()//4)
        x5, y5 = (event.x + scaleVar.get()), (event.y)
        x6, y6 = (event.x + scaleVar.get()//4), (event.y + scaleVar.get()//4)
        x7, y7 = (event.x), (event.y + scaleVar.get())
        x8, y8 = (event.x - scaleVar.get()//4), (event.y + scaleVar.get()//4)
        points = [x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8]
        if fillVar.get() == 0:
            w.create_polygon(points, fill = color[1], outline = color_outline[1])
            draw.polygon([x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8],fill=color[0], outline = color_outline[0])
        else:
            w.create_polygon(points, fill = '', outline = color_outline[1])
            draw.polygon([x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8], fill = None, outline = color_outline[0])
        pointlist4.append([x1, y1])
    elif opVar.get() == 5: # Random
        rand_num = randint(0,1)
        x1, y1 = ( event.x - scaleVar.get() ), ( event.y - scaleVar.get() )
        x2, y2 = ( event.x + scaleVar.get() ), ( event.y + scaleVar.get() )
        if fillVar.get() == 0:
            if rand_num == 0:
                rand_shape = w.create_oval( x1, y1, x2, y2, fill = color[1], outline = color_outline[1])
                draw.ellipse([x1, y1, x2, y2], fill = color[0], outline = color_outline[0])
            else:
                rand_shape = w.create_rectangle( x1, y1, x2, y2, fill = color[1], outline = color_outline[1])
        else:
            if rand_num == 0:
                rand_shape = w.create_oval( x1, y1, x2, y2, fill = None, outline = color_outline[1])
            else:
                rand_shape = w.create_rectangle( x1, y1, x2, y2, fill = None, outline = color_outline[1])
        def movement(dx, dy):
            x1_1, y1_1, x2_1, y2_1 = list(map(int, w.coords(rand_shape))) 
            # Crea una lista con las corrdenadas pero en vez de float con int

            if (x1_1 <= 0 and dx < 0) or (x2_1 >= canvas_width and dx > 0): 
                # Invierte desplazamiento en x cuando choca con muros verticales. Evita bug
                
                dx = -dx
            elif (y1_1 <= 0 and dy < 0) or (y2_1 >= canvas_height and dy > 0): 
                # Invierte desplazamiento en y cuando choca con muros horizontales. Evita bug
                dy = -dy
            w.move(rand_shape, dx, dy)
            w.after(25, movement, dx, dy) # Se mueve cada 25 ms
            draw.ellipse([x1_1, y1_1, x2_1, y2_1], fill = color[0], outline = color_outline[0])
        movement(randint(-15, 15), randint(-15, 15)) # Se mueve x pixeles en horizontal e y en vertical


def findparas(points, listtype, total_piece_time):
    sort_point = points[np.argsort(points[:,0])]
    unique_points = points[np.unique(points[:,0]//20,axis=0,return_index=True)[1]]
    x = unique_points[:,0]//20
    y = unique_points[:,1]
    timelist = np.zeros(50)
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
            intervallist[i] = 50-onesrange[i]
    for yval in y:
        chordlist.append(decideNote(yval, listtype))
    return starttime, (intervallist/(100/total_piece_time)).tolist(), chordlist
def decideNote(y, listtype):
    classy = 0
    interval = 100/7
    octave = 6- y//100
    y = y%100
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
        starttime0, intervallist0, chordlist0 = findparas(np.array(pointlist0), givenkey, total_piece_time)
        tracklist.append(chord(chordlist0, interval = intervallist0))
        instrumentlist.append(20)
        startTimelist.append(starttime0)
    if pointlist1:
        starttime1, intervallist1, chordlist1 = findparas(np.array(pointlist1), givenkey, total_piece_time)
        tracklist.append(chord(chordlist1, interval = intervallist1))
        instrumentlist.append(25)
        startTimelist.append(starttime1)
    if pointlist2:
        starttime2, intervallist2, chordlist2 = findparas(np.array(pointlist2), givenkey, total_piece_time)
        tracklist.append(chord(chordlist2, interval = intervallist2))
        instrumentlist.append(46)
        startTimelist.append(starttime2)
    if pointlist3:
        starttime3, intervallist3, chordlist3 = findparas(np.array(pointlist3), givenkey, total_piece_time)
        tracklist.append(chord(chordlist3, interval = intervallist3))
        instrumentlist.append(108)
        startTimelist.append(starttime3)
    if pointlist4:
        starttime4, intervallist4, chordlist4 = findparas(np.array(pointlist4), givenkey, total_piece_time)
        tracklist.append(chord(chordlist4, interval = intervallist4))
        instrumentlist.append(109)
        startTimelist.append(starttime4)
    my_piece = piece(tracks = tracklist, instruments = instrumentlist, bpm = 120, start_times = startTimelist)
    play(my_piece)


def clear():
    global pointlist0, pointlist1, pointlist2, pointlist3, pointlist4
    pointlist0, pointlist1, pointlist2, pointlist3, pointlist4 = [], [], [], [], []
    w.delete(ALL)
    wid = image1.width
    h = image1.height
    draw.rectangle([0, 0, wid, h], fill = "white", width = 0)
    # You would normally put that on the App class
    def show_error(self, *args):
        pass
    # but this works too
    Tk.report_callback_exception = show_error
def grid_on():
    for i in range(50):
        w.create_line(0,int(1000/50*i),1000,int(1000/50*i),fill='black',width=1)
        w.create_line(int(1000/50*i),0,int(1000/50*i),400,fill='black',width=1)
    w.create_line(0,200,1000,200,fill='red',width=1)


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
root.iconbitmap('logo.ico')
root.resizable(False,False)

# Variables
opVar = IntVar()
scaleVar = IntVar()
fillVar = IntVar()
keyVar = StringVar()
timeVar = StringVar()

canvas_width = 1000
canvas_height = 400

color = ((0,0,0),['#000'])
color_outline = ((0,0,0),['#000'])
cl = []

pointlist0, pointlist1, pointlist2, pointlist3, pointlist4 = [], [], [], [], []

font_1 = ("Times", "14", "bold italic")
font_2 = ("Times", "12", "bold")
font_3 = ("Helvetica", "12", "bold")

# CANVAS
w = Canvas(root, width = canvas_width, height = canvas_height)

w.config(bg = '#fff')

w.pack(expand = 1, fill = 'both')

w.bind("<B1-Motion>", paint )
w.bind("<Button-1>", paint )


# Img in PIL. It is not displayed, it is used to save the image.
image1 = Image.new("RGB", (canvas_width, canvas_height), 'white')
draw = ImageDraw.Draw(image1)


## Labels and Tools
# LabelFrame 1
bg_image = PhotoImage(file = 'bg_2.png')

mylabelframe = LabelFrame(root, text = 'Tools', font=font_1)
mylabelframe.pack(fill = 'both',expand = 1, ipadx = 10, ipady = 10, padx = 8, pady = 5)

bg_label = Label(mylabelframe, image = bg_image)
bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)


scale = Scale(mylabelframe, variable = scaleVar, orient = 'horizontal', from_ = 0, to = 60, label = 'Brush Size', length = 400, repeatdelay = 500, relief = 'sunken', sliderlength = 25)
scale.grid(row = 0, column = 0, columnspan = 3)

oval_brush = Radiobutton(mylabelframe, text = 'Circle Brush', variable = opVar, value = 0, font = font_2).grid(row = 1, column = 0, sticky = 'w')
line_brush = Radiobutton(mylabelframe, text = 'Line Brush', variable = opVar, value = 1, font = font_2).grid(row = 2, column = 0, sticky ='w')
rectangle = Radiobutton(mylabelframe, text = 'Square Brush', variable = opVar, value = 2, font = font_2).grid(row = 1, column = 1, sticky = 'w')
polygon_brush = Radiobutton(mylabelframe, text = 'Polygon Brush', variable = opVar, value = 3, font = font_2).grid(row = 2, column = 1, sticky = 'w')
star = Radiobutton(mylabelframe, text = 'Star Brush', variable = opVar, value = 4, font = font_2).grid(row = 3, column = 0, sticky = 'w')
random_move = Radiobutton(mylabelframe, text = 'Random Brush', variable = opVar, value = 5, font = font_2).grid(row = 3, column = 1, sticky = 'w')


# LabelFrame 2
mylabelframe2 = LabelFrame(mylabelframe, text = 'Fill  and  Outline color', font = font_1)
mylabelframe2.grid(row = 1, column = 2, rowspan = 2, ipadx = 20, pady = 10, padx = 25)

color_button = Button(mylabelframe2, width = 5)
color_button.grid(row = 0, column = 0)
color_button.config(command = choose_color, bg = color[1])

sep = Separator(mylabelframe2, orient = 'vertical').grid(row = 0, column = 1, sticky = 'ns', padx = 5)

color_outline_button = Button(mylabelframe2, width = 5)
color_outline_button.grid(row = 0, column = 2, padx = 9)
color_outline_button.config(command = outline_color, bg = color_outline[1])

fill_button = Radiobutton(mylabelframe2, text = 'Fill', variable = fillVar, value = 0, font = font_2).grid(row = 2, column = 0, sticky = 'w')
hollow_button = Radiobutton(mylabelframe2, text = 'Hollow', variable = fillVar, value = 1, font = font_2).grid(row = 3, column = 0, sticky = 'w')



sep_2 = Separator(mylabelframe, orient = 'vertical').grid(row = 0, column = 4, rowspan = 4,sticky = 'ns', padx = 25)

# Grid on
grid_on_button = Button(mylabelframe, text="       Grid On        ", compound = 'left', padx = 8, pady = 5, font = font_3)
grid_on_button.grid(row = 1, column = 5, sticky = 'w')
grid_on_button.config(command = grid_on)

# Clear
clear_button = Button(mylabelframe, text="          Clear          ", compound = 'left', padx = 8, pady = 5, font = font_3)
clear_button.grid(row = 2, column = 5)
clear_button.config(command = clear)

# Music Generator
play_button = Button(mylabelframe, text="Play your music", compound = 'left', padx = 8, pady = 5, font = font_3)
play_button.grid(row = 3, column = 5)
play_button.config(command = play_button_event)


# dropown select
sep_3 = Separator(mylabelframe, orient = 'vertical').grid(row = 0, column = 6, rowspan = 4,sticky = 'ns', padx = 25)

# Select time
timechoices = {"5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"}
timeVar.set('30') # set the default option
timeMenu = OptionMenu(mylabelframe, timeVar, *timechoices)
timeMenu.grid(row = 0, column =7)

# Select key
keychoices = {'C','C#','D','D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'}
keyVar.set('C') # set the default option
keyMenu = OptionMenu(mylabelframe, keyVar, *keychoices)
keyMenu.grid(row = 1, column =7)


'''If the different images don't work, try putting the full URL or just skip the images'''

root.mainloop()
