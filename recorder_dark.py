from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import Style
import os.path

import calendar
import time


DarkBg = "#333"
DarkBg2 = "#222"
DarkBg3 = "#111"
DarkFg = "#fff"
largerFontSize = 15
defaultFontSize = 12
buttonFontSize = 10
buttonBg = "#555"
buttonFg = "#fff"
fieldBg = "#555"
fieldFg = "#fff"


root = Tk()

root.title("audio recorder")
root.geometry("800x480")
root.configure(background=DarkBg)





style = Style(root)
style.configure('Dark.TFrame', background=DarkBg)
style.configure('Dark2.TFrame', background=DarkBg2)
style.configure('Dark3.TFrame', background=DarkBg3)



mainframe = ttk.Frame(root, style="Dark.TFrame")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)



# root.option_add('*TCombobox*Background', 'black')

root.option_add("*TCombobox*Listbox*Font", defaultFontSize)
root.option_add("*TCombobox*Listbox*Background", fieldBg)
root.option_add("*TCombobox*Listbox*Foreground", fieldFg)

fileinfo = ttk.Frame(root, borderwidth=4, padding=4, style="Dark3.TFrame")
fileinfo.grid(column=0, row=1, sticky=(N, W, E, S))

transportframe = ttk.Frame(root,  padding=10, style="Dark2.TFrame")
transportframe.grid(column=0, row=1, sticky=(N, W, E, S))

flashmesg = False
flash_delay = 500 
flash_bg_colours = (DarkBg2, 'red')
flash_fg_colours = ("red", 'white') 


def flashColour(object, colour_index):
    global flashmesg

    if flashmesg:
        object.config(bg = flash_bg_colours[colour_index], fg = flash_fg_colours[colour_index])
        root.after(flash_delay, flashColour, object, 1 - colour_index)


def generateFilename():
    ts = calendar.timegm(time.gmtime())
    fname = "audiofile_" + str(ts)
    filename_entry.delete(0,END)
    filename_entry.insert(0,fname)
    return

def selectDirectory():
    folder_selected = filedialog.askdirectory()
    directory_entry.delete(0,END)
    directory_entry.insert(0,folder_selected)
    return

def startRecording():
    global flashmesg

    filename = filename_entry.get()
    path = directory_entry.get()
    if filename=="":
        statusmsg.configure(text="Error: No filename selected!",  fg="Red", background=DarkBg2)
        flashmesg = False
    else :
        ffname = path+"/"+filename+".wav"
        if os.path.isfile(ffname):
            statusmsg.config(text="Error: File already exists!", fg="Red", background=DarkBg2)
            flashmesg = False
        else:
            recbtn.configure(relief=SUNKEN)
            statusmsg.config(text="Recording", fg="Red", background=DarkBg2)
            fullFilePath.config(text=ffname)
            flashmesg = True
            flashColour(statusmsg, 0)
    
def stopRecording():
    global flashmesg
    recbtn.config(relief=RAISED)
    flashmesg = False
    statusmsg.configure(text="Recording stopped", fg=DarkFg, background=DarkBg2)



ttk.Label(mainframe, text="Recording Options", font=("Arial Bold",largerFontSize), background=DarkBg, foreground=DarkFg).grid(column=2, row=0, sticky=W, columnspan=5)


filepath = StringVar()
ttk.Label(mainframe, text="Directory", background=DarkBg, foreground=DarkFg, font=defaultFontSize).grid(column=1, row=1, sticky=W)
directory_entry = Entry(mainframe, width=70, textvariable=filepath, font=defaultFontSize, bg=fieldBg, fg=fieldFg, relief=FLAT, borderwidth=5)
directory_entry.grid(column=2, row=1,  sticky=(W, E), columnspan=6)
sd = Button(mainframe, text="Change", fg=buttonFg, bg=buttonBg, relief=FLAT, font=("Arial Bold",buttonFontSize), command=selectDirectory)
sd.grid(column=9, row=1, sticky=W)

filename = StringVar()
ttk.Label(mainframe, text="Filename", background=DarkBg, foreground=DarkFg, font=defaultFontSize).grid(column=1, row=2, sticky=W)
filename_entry = Entry(mainframe,  textvariable=filename, font=defaultFontSize, bg=fieldBg, fg=fieldFg, relief=FLAT, borderwidth=5)
filename_entry.grid(column=2, row=2,  sticky=(W,E), columnspan=4)
ttk.Label(mainframe, text=".wav", background=DarkBg, foreground=DarkFg, font=defaultFontSize).grid(column=6, row=2, sticky=W)
sg = Button(mainframe, text="Generate", fg=buttonFg, bg=buttonBg, relief=FLAT, font=("Arial Bold",buttonFontSize), command=generateFilename)
sg.grid(column=9, row=2, sticky=W)


inputConfig = StringVar()
ttk.Label(mainframe, text="Input ch", background=DarkBg, foreground=DarkFg, font=defaultFontSize).grid(column=1, row=3, sticky=W)
inputconf = ttk.Combobox(mainframe, textvariable=inputConfig, width=6, font=defaultFontSize, background="#000" )
inputconf.grid(column=2, row=3,  sticky=(W, E))
inputconf['values'] = ('Stereo', 'Mono')
inputconf.current(0)

samplingRate = StringVar()
ttk.Label(mainframe, text="Sampling Rate", background=DarkBg, foreground=DarkFg, font=defaultFontSize).grid(column=3, row=3, sticky=E, padx=4)
sRate = ttk.Combobox(mainframe, textvariable=samplingRate, width=8, font=defaultFontSize)
sRate.grid(column=4, row=3,  sticky=(W, E))
sRate['values'] = ('48Khz', '44.1Khz')
sRate.current(0)

bitDepth = StringVar()
ttk.Label(mainframe, text="Bit Depth", background=DarkBg, foreground=DarkFg, font=defaultFontSize).grid(column=5, row=3, sticky=W, padx=4)
bd = ttk.Combobox(mainframe, textvariable=bitDepth, width=6, font=defaultFontSize)
bd.grid(column=5, row=3)
bd['values'] = ('16bit', '8bit')
bd.current(0)


mainframe.columnconfigure(5, weight=1)
mainframe.rowconfigure(4, weight=1)


#File info Area --------------------------------------------------------------------------

fullFilePath = Label(fileinfo, text="No file generated yet",  background=DarkBg3, foreground=DarkFg, font=defaultFontSize)
fullFilePath.grid(row=1, column=0, sticky=W)

fileinfo.columnconfigure(1, weight=1)
fileinfo.rowconfigure(2, weight=1)


#Transport Area ---------------------------------------------------------------------------
statusmsg = Label(transportframe, text="Not Recording",   fg="black", font=("Arial Bold",largerFontSize),  background=DarkBg2, foreground=DarkFg)
statusmsg.grid(row=4, column=3, columnspan=6, sticky=W)

recbtn = Button(transportframe, text="REC", bg="red", fg="white", padx=20, pady=20, font=("Arial Bold",15), command=startRecording, relief=RAISED )
recbtn.grid(column=0, row=4, sticky=S)

stopbtn = Button(transportframe, text="STOP", bg="#ffc847", fg="black", padx=20, pady=20, font=("Arial Bold",15), command=stopRecording)
stopbtn.grid(column=1, row=4, sticky=S )

#-------------------------------------------------------------------------------------------


#Pame mia xyma twra
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

for child in transportframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

mainframe.grid(row=0)
fileinfo.grid(row=1)
transportframe.grid(row=2)


root.mainloop()