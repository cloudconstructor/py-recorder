from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os.path

import calendar
import time



root = Tk()
original_background = root.cget("background")
root.title("audio recorder")
root.geometry("800x400")
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

fileinfo = ttk.Frame(root, borderwidth=4, padding=4, relief="solid")
fileinfo.grid(column=0, row=1, sticky=(N, W, E, S))

transportframe = ttk.Frame(root,  padding=10)
transportframe.grid(column=0, row=1, sticky=(N, W, E, S))

flashmesg = False
flash_delay = 500 
flash_bg_colours = (original_background, 'red')
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
        statusmsg.configure(text="Error: No filename selected!",  fg="Red", background=original_background)
        flashmesg = False
    else :
        ffname = path+"/"+filename+".wav"
        if os.path.isfile(ffname):
            statusmsg.config(text="Error: File already exists!", fg="Red", background=original_background)
            flashmesg = False
        else:
            recbtn.configure(relief=SUNKEN)
            statusmsg.config(text="Recording", fg="Red", background=original_background)
            fullFilePath.config(text=ffname)
            flashmesg = True
            flashColour(statusmsg, 0)
    
def stopRecording():
    global flashmesg
    recbtn.config(relief=RAISED)
    flashmesg = False
    statusmsg.configure(text="Recording stopped", fg="black", background=original_background)



ttk.Label(mainframe, text="Recording Options", font=("Arial Bold",15)).grid(column=2, row=0, sticky=W, columnspan=5)


filepath = StringVar()
ttk.Label(mainframe, text="Directory").grid(column=1, row=1, sticky=W)
directory_entry = ttk.Entry(mainframe, width=70, textvariable=filepath)
directory_entry.grid(column=2, row=1,  sticky=(W, E), columnspan=6)
ttk.Button(mainframe, text="Change", command=selectDirectory).grid(column=9, row=1, sticky=W)

filename = StringVar()
ttk.Label(mainframe, text="Filename").grid(column=1, row=2, sticky=W)
filename_entry = ttk.Entry(mainframe, width=70, textvariable=filename)
filename_entry.grid(column=2, row=2,  sticky=(W, E), columnspan=5)
ttk.Label(mainframe, text=".wav").grid(column=8, row=2, sticky=W)
ttk.Button(mainframe, text="Auto Generate", command=generateFilename).grid(column=9, row=2, sticky=W)


inputConfig = StringVar()
ttk.Label(mainframe, text="Input ch").grid(column=1, row=3, sticky=W)
inputconf = ttk.Combobox(mainframe, textvariable=inputConfig, width=6)
inputconf.grid(column=2, row=3,  sticky=(W, E))
inputconf['values'] = ('Stereo', 'Mono')
inputconf.current(0)

samplingRate = StringVar()
ttk.Label(mainframe, text="Sampling Rate").grid(column=3, row=3, sticky=E, padx=4)
sRate = ttk.Combobox(mainframe, textvariable=samplingRate, width=6)
sRate.grid(column=4, row=3,  sticky=(W, E))
sRate['values'] = ('44.1Khz', '48Khz')
sRate.current(0)

bitDepth = StringVar()
ttk.Label(mainframe, text="Bit Depth").grid(column=5, row=3, sticky=E, padx=4)
bd = ttk.Combobox(mainframe, textvariable=bitDepth, width=6)
bd.grid(column=6, row=3,  sticky=(W, E))
bd['values'] = ('16bit', '24bit')
bd.current(0)

fullFilePath = Label(fileinfo, text="No file generated yet",  font=("Arial Bold",10), fg="black")
fullFilePath.grid(row=0, column=0, sticky=W)


#Transport Area ---------------------------------------------------------------------------
statusmsg = Label(transportframe, text="Not Recording",  font=("Arial Bold",10), fg="black")
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