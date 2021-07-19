import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText
import csv
import re
import subprocess
import time
import logging
import string
import random
import os.path as ostest
import playsound
import os
import winsound

#set up tkinter window
window = tk.Tk()
window.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=40)
window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], minsize=0)
window.resizable(False, False)

#logo
if ostest.isfile('LargeLogo.GIF'):
    print("File exists")
else:
    print("File not found")
img = tk.PhotoImage(file="MediumLogo.GIF")
canvas = tk.Canvas(window, width=300, height=150)
canvas.configure(bg='#F0F0F0')
canvas.grid(row=0, column=0)
canvas.create_image(90, 80, image=img)

#set up logging
logging.basicConfig(filename='test.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')
logging.Formatter(datefmt='%Y-%m-%d %H:%M:%S')


#logging object, referenced by Action Logging Window
class TextHandler(logging.Handler):
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(tk.END)

        self.text.after(0, append)


def create_window():
    newwindow = tk.Toplevel()
    newwindow.columnconfigure([0, 1, 2], minsize=40)
    newwindow.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], minsize=0)
    helplabel = tk.Label(newwindow,
        text="User Manual",
        width=12,
        height=7
    )
    helplabel.grid(row=1, column=1)
    initializetext = tk.Label(newwindow,
        text="First, click the Initialize button in the top center of the GUI. This will search for all online DREDs.  \n "
             "Next, select the DRED you wish to output audio to using the 'select DRED' dropdown menu. If the DRED you wish to use does not appear, it is offline. \n"
             "Next, select the frequency you wish the sound to play at from the 'select frequency' dropdown OR enter a custom frequnecy in the 'custom frequency' box. \n"
             "Next, select the sound you wish to play from the 'select sound' dropdown OR enter a custom sound in the 'custom sound' box. \n"
             "Lastly, select 'play sound' and the sound will play on the selected DRED",
        width=120,
        height=5
    )
    initializetext.grid(row=2, column=1)
    queuetext = tk.Label(newwindow,
        text="You also have the option to create a queue of multiple sounds to play. \n"
             "Simply initialize, select frequency and sound, then select the 'add to queue' option. \n"
             "Once your queue is complete, select 'play entire queue'. All selected sounds will play at their set frequecies in the order specified. \n"
             "NOTE: You can not add a queue to CRON as this is not supported by CRON jobs",
        width=120,
        height=5
    )
    queuetext.grid(row=3, column=1)
    crontext = tk.Label(newwindow,
        text="If you wish to set a cronjob to play at a set time you can schedule a 'cronjob' \n"
             "Select DRED, frequency, and sound, then fill out the desired minutes, hours, day of month, month, and day of week. \n"
             "You can use a wildcard (*) to select every available value. Or you can enter a number value. You can also use the */ option to play the sound every set interval. \n"
             "You can not use an numbers before '/', only wildcards. EX. '13/30' is not a valid command.\n"
             "All operators are '*' (any value) ',' (list values) '-' (value range) '/' (step values). Number values also start from 0. \n"
             "Ex: If you want to play a sound every 5 minutes at 1600 - 1800 5 days a week the syntax will be '*/5 16-18 * * 0,1,2,3,4' \n"
             "You also have the option to queue the same sound to play multiple times by using ';' to add multiple cron jobs at once. \n"
             " You can not add multiple sound files at once.\n \n"
             "You can view all cronjobs by selecting 'show CRON jobs'. You can reset all cron jobs by selecting 'reset CRON jobs', \n"
             "or you can remove a specific job by entering the job code in 'remove CRON job' (without the # sign) \n",
        width=120,
        height=12
    )
    crontext.grid(row=4, column=1)


addphoto = tk.PhotoImage(file=r"add_image.png")
remphoto = tk.PhotoImage(file=r"remove_image.png")
playphoto = tk.PhotoImage(file=r"play_image.png")
helpphoto = tk.PhotoImage(file=r"help_image.png")
initphoto = tk.PhotoImage(file=r"init_image.png")
timephoto = tk.PhotoImage(file=r"time_image.png")
clearphoto = tk.PhotoImage(file=r"clear_image.png")
vncphoto = tk.PhotoImage(file=r"vnc_image.png")
resetphoto = tk.PhotoImage(file=r"reset_image.png")
showphoto = tk.PhotoImage(file=r"show_image.png")
shutdownphoto = tk.PhotoImage(file=r"shutdown_image.png")
coordphoto = tk.PhotoImage(file=r"coord_image.png")

freqlist = ["blank"]
filelist = ["blank"]


#Button to play single sound (not actually standard button)
class StandardButton(tk.Button):
    def __init__(self, text, gfreq, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=playphoto, compound=tk.LEFT,
                    command=lambda: run_script(gfreq) or None)
        self.grid(row=rw, column=cl)


#Button to play single sound (not actually standard button)
class PlayLocalButton(tk.Button):
    def __init__(self, text, gfreq, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=playphoto, compound=tk.LEFT,
                    command=lambda: playlocal_script(gfreq) or None)
        self.grid(row=rw, column=cl)


#Button to add job to crontab
class JobButton(tk.Button):
    def __init__(self, text, gfreq, gmin, ghou, gdom, gmon, gdow, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=addphoto, compound=tk.LEFT,
                    command=lambda: sendjob_script(gmin, ghou, gdom, gmon, gdow, gfreq) or None)
        self.grid(row=rw, column=cl)


#Button to reset crontab
class ResetButton(tk.Button):
    def __init__(self, text, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=resetphoto, compound=tk.LEFT,
                    command=lambda: reset_script() or None)
        self.grid(row=rw, column=cl)


#Add sound file to queue
class AddQueueButton(tk.Button):
    def __init__(self, text, gfreq, queue, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=addphoto, compound=tk.LEFT,
                    command=lambda: addqueue_script(gfreq, queue) or None)
        self.grid(row=rw, column=cl)


class PlayQueueButton(tk.Button):
    def __init__(self, text, queue, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=playphoto, compound=tk.LEFT,
                    command=lambda: playqueue_script(queue) or None)
        self.grid(row=rw, column=cl)


class DeleteQueueButton(tk.Button):
    def __init__(self, text, queue, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=remphoto, compound=tk.LEFT,
                    command=lambda: deletequeue_script(queue) or None)
        self.grid(row=rw, column=cl, pady=12)


class ShowCronButton(tk.Button):
    def __init__(self, text, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=showphoto, compound=tk.LEFT,
                    command=lambda: showcron_script() or None)
        self.grid(row=rw, column=cl)


class RemoveCronButton(tk.Button):
    def __init__(self, text, code, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=remphoto, compound=tk.LEFT,
                    command=lambda: removecron_script(code) or None)
        self.grid(row=rw, column=cl)


class HelpButton(tk.Button):
    def __init__(self, text, code, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=helpphoto, compound=tk.LEFT,
                    command=create_window)
        self.grid(row=rw, column=cl)


class GetTimeButton(tk.Button):
    def __init__(self, text, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=timephoto, compound=tk.LEFT,
                    command=gettime_script)
        self.grid(row=rw, column=cl, pady=12)


class ClearLogButton(tk.Button):
    def __init__(self, text, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=clearphoto, compound=tk.LEFT,
                    command=clearlog_script)
        self.grid(row=rw, column=cl)


class VNCButton(tk.Button):
    def __init__(self, text, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=vncphoto, compound=tk.LEFT,
                    command=lambda: vncviewer_script())
        self.grid(row=rw, column=cl)


class ShutDownButton(tk.Button):
    def __init__(self, text, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="red", width=210, height=50, image=shutdownphoto, compound=tk.LEFT,
                    command=lambda: shutdown_script())
        self.grid(row=rw, column=cl)

class coordButton(tk.Button):
    def __init__(self, text, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=210, height=50, image=coordphoto, compound=tk.LEFT,
                    command=lambda: get_GPS_coords())
        self.grid(row=rw, column=cl)


#place logging object
log_window = ScrolledText.ScrolledText(window, state='disabled')
log_window.grid(row=2, column=1, rowspan=7, columnspan=5, sticky="nsew")
log_window.config(background="white")
# ALW is Action Logging Window
ALW = TextHandler(log_window)


logger = logging.getLogger()
logger.addHandler(ALW)


#log message function
def log(message):
    logging.info(time.asctime() + " - " + message)


badips = []
goodips = []
goodipnames = []


#reads ips from dredlist file and puts them in object
def scan_iplist():
    scanips = []
    with open('dredlist.csv') as iplist_csv:
        csv_reader = csv.reader(iplist_csv, delimiter=',')
        for row in csv_reader:
            scanips.append(row)
    print(scanips)

    return scanips


#determines if host is alive by ip
def find_good_ips(iplist_array):
    global badips
    badips = []
    global goodips
    goodips = []
    global goodipnames
    goodipnames = []
    for x in iplist_array:
        print(x[0])
        gip = str(x[0])
        print("Scanning " + gip)
        cmd = ['C:\\Windows\\System32\\PING.EXE', '-n', '1', gip]
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        # print(result.decode("utf-8"))
        if result.decode("utf-8").find("time") == -1:
            print("Address not found: " + gip)
            badips.append(x)
        else:
            goodips.append(x)
    list_bad_TB = []
    for x in badips:
        bad_TB = x[1]
        list_bad_TB.append(bad_TB)
    # print(badips)
    list_good_TB = []
    for x in goodips:
        good_TB = x[1]
        list_good_TB.append(good_TB)
    # print(goodips)
    log("Missing:  " + str(list_bad_TB))
    log("Found:    " + str(list_good_TB))
    if len(goodips) == 0:
        log("No DREDs loaded. Check Power and Wifi connections...")
    else:
        log("Select Device to operate with the drop down above...")
    for x in goodips:
        goodipnames.append(x[1])
    comboips.config(values=goodipnames)
    #comboips.current(1)  # check to see if it works


#logs scanned devices
def init_log(event):
    log("Scanning for devices. Please wait...")
    obj_list = []
    with open('dredlist.csv') as iplist_csv:
        csv_reader = csv.reader(iplist_csv, delimiter=',')
        for row in csv_reader:
            obj_list.append(row[1])
    log("Scanning: " + str(obj_list))
    return obj_list


# fuction for initialize button
def init_go(event):
    x = scan_iplist()
    find_good_ips(x)


# send command to DRED to play sound file
def run_script(freq):
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    ufreq = freq.get()
    log("Please wait...")
    window.update()
    #print("freq = " + freq.get())
    #print("cfreq = " + cfreq.get())
    #print("ufreq = " + ufreq)
    #pyscript = ufreq
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', 'pi@' + targetip, '/bin/bash',
           '/range/relay1on.sh; sudo python /range/' + ufreq + ' ; /range/relay1off.sh; exit ; exit']
    print(cmd)
    conout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # print(conout.decode("utf-8"))
    if "HackRF One" in str(conout):
        log("Sound played successfully.")
    else:
        log(str(comboips.get()) + '\n'*2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))


def playlocal_script(freq):
    if os.path.exists("got.wav"):
        os.remove("got.wav")
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    ufreq = freq.get()
    split_str = "_5w_"
    get_sound = ufreq.partition(split_str)[2]
    split_strb = ".py"
    get_soundb = get_sound.partition(split_strb)[0]
    window.update()
    #print("freq = " + freq.get())
    #print("cfreq = " + cfreq.get())
    #print("ufreq = " + ufreq)
    #pyscript = ufreq
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\sftp.exe ', 'pi@' + targetip + ':/home/pi/Music/' + get_soundb + '.wav', ' got.wav ; exit']
    print(cmd)
    conout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    #playsound.playsound('got.wav')
    if os.path.exists("got.wav"):
        log("Playing requested sound file. Please wait until the sound finishes playing.")
        window.update()
        winsound.PlaySound('got.wav', winsound.SND_FILENAME)
        log("Sound file has finished playing.")
    else:
        log("Could not retrieve sound file. Ensure that sound follows naming convention.")
    #os.remove("got.wav")


def sendjob_script(minute, hour, dom, month, dow, freq):
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    minr = minute.get()
    hourr = hour.get()
    domr = dom.get()
    monr = month.get()
    dowr = dow.get()
    minl = list(minr.split(";"))
    hourl = list(hourr.split(";"))
    doml = list(domr.split(";"))
    monl = list(monr.split(";"))
    dowl = list(dowr.split(";"))
    done = 0
    while done == 0:
        gminr = minl[0]
        ghourr = hourl[0]
        gdomr = doml[0]
        gmonr = monl[0]
        gdowr = dowl[0]
        if gminr == "" or ghourr == "" or gdomr == "" or gmonr == "" or gdowr == "":
            log("One or more fields are empty.")
            return
        if re.search("^([0-5][0-9](,[0-5][0-9])*(-[0-5][0-9])?([/][0-5][0-9])?|[*]([/][0-5][0-9])?)$", gminr) is None:
            log("Invalid content in Minutes field")
            return
        if re.search("^(([1-9]|1[0-9]|2[0-9]|3[0-1])(,([1-9]|1[0-9]|2[0-9]|3[0-1]))*([-]([1-9]|1[0-9]|2[0-9]|3[0-1]))?([/]([2-9]|1[0-9]|2[0-9]|3[0-1]))?|[*]([/]([2-9]|1[0-9]|2[0-9]|3[0-1]))?)$", gdomr) is None:
            log("Invalid content in Day of Month field")
            return
        if re.search("^(([0-9]|0[1-9]|1[0-9]|2[0-4])(,([1-2]|0[1-9]|1[0-9]|2[0-4]))*([-]([0-2]|0[1-9]|1[0-9]|2[0-4]))?([/]([2-9]|0[2-9]|1[0-9]|2[0-4]))?|[*]([/]([2-9]|0[2-9]|1[0-9]|2[0-4]))?)$", ghourr) is None:
            log("Invalid content in Hours field")
            return
        if re.search("^(([0-9]|0[0-9]|1[0-2])(,([0-9]|0[0-9]|1[0-2]))*([-]([0-9]|0[0-9]|1[0-2]))?([/]([2-9]|0[2-9]|1[0-2]))?|[*]([/]([2-9]|0[2-9]|1[0-2]))?)$", gmonr) is None:
            log("Invalid content in Month field")
            return
        if re.search("^(([0-6])(,([0-6]))*([-]([0-6]))?|[*])$", gdowr) is None:
            log("Invalid content in Day of Week field")
            return
        ufreq = freq.get()
        #pyscript = "/range/nbfm_" + ufreq + "_5w_" + uname + ".py"
        job = gminr + " " + ghourr + " " + gdomr + " " + gmonr + " " + gdowr + " /range/relay1on.sh ; sudo python /range/" + ufreq + " ; /range/relay1off.sh"
        print(job)
        cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v ', 'pi@' + targetip,
               ' crontab -l > mycron; exit ; exit']
        cmdb = ''.join(cmd)
        print(cmdb)
        conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("Phase 1")
        s = 10
        ran = "".join(random.choices(string.ascii_uppercase+string.digits, k=s))
        code = "#" + ran
        # print(conout.decode("utf-8"))
        #if len(str(conout)) > 10:
            #log(str(comboips.get()) + '\n' * 2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))

        cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
               ' \"echo \'' + code + '\' >> /home/pi/mycron; exit ; exit\"']
        cmdb = ''.join(cmd)
        print(cmdb)
        conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("Phase 2")
        #print(conout.decode("utf-8"))
        #if len(str(conout)) > 10:
            #log(str(comboips.get()) + '\n'*2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))

        cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
               ' \"echo \'' + job + '\' >> /home/pi/mycron; exit ; exit\"']
        cmdb = ''.join(cmd)
        conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("Phase 2.5")
        cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip, ' crontab mycron; exit ; exit']
        cmdb = ''.join(cmd)
        print(cmdb)
        conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("Phase 3")
        #print(conout.decode("utf-8"))
        if len(str(conout)) >= 10:
            log("Job Successfully added.")
        else:
            log(str(comboips.get()) + '\n'*2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))

        minl.pop(0)
        hourl.pop(0)
        doml.pop(0)
        monl.pop(0)
        dowl.pop(0)
        if len(minl) == 0 or len(hourl) == 0 or len(doml) == 0 or len(monl) == 0 or len(dowl) == 0:
            done = 1


def reset_script():
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
           ' \"crontab backupcron; exit ; exit\"']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # print(conout.decode("utf-8"))
    if len(str(conout)) >= 10:
        log("All jobs removed.")
    else:
        log(str(comboips.get()) + '\n'*2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))


def addqueue_script(freq, queue):
    ufreq = freq.get()
    sel = queue.curselection()
    sels = str(sel)
    if sels == '()':
        queue.insert(tk.END, ufreq)
    else:
        for index in sel[::-1]:
            queue.insert(sel, ufreq)


def playqueue_script(queue):
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    log("Playing first sound in queue.")
    window.update()
    while queue.size() > 0:
        element = queue.get(0)
        #tu = element.split(",")
        #freq = tu[0]
        #name = tu[1]
        #pyscript = freq
        cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe ', 'pi@' + targetip, '/bin/bash',
               '/range/relay1on.sh; sudo python /range/' + element + ' ; /range/relay1off.sh']
        conout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if "HackRF One" not in str(conout):
            log(str(comboips.get()) + '\n' * 2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))
        queue.delete(0)
        if queue.size == 0:
            log("All sounds in queue played.")
        else:
            log("Playing next sound in queue")
        window.update()


def deletequeue_script(queue):
    sel = queue.curselection()
    #print(sel)
    for index in sel[::-1]:
        queue.delete(index)


def showcron_script():
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
           ' crontab -l > mycron; exit ; exit']
    cmdb = ''.join(cmd)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    #print("1 Complete")
    #if len(str(conout)) > 10:
        #log(str(comboips.get()) + '\n' * 2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', ' pi@' + targetip,
           ' \"./getjobs.sh; exit ; exit\"']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(len(str(conout)))
    if len(str(conout)) == 10:
        log("No jobs found.")
    else:
        log(str(comboips.get()) + ' Jobs\n' + conout[0].decode("utf-8") + conout[1].decode("utf-8"))


def removecron_script(code):
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe ', 'pi@' + targetip,
               ' crontab -l > mycron']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    codeb = code.get()
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', ' pi@' + targetip,
               ' python removejob.py ' + codeb]
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # print("1 Complete")
    #log(str(comboips.get()) + '\n' * 2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', ' pi@' + targetip,
               ' \"crontab myreplacecron\"']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    #log(str(comboips.get()) + '\n' * 2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))
    log("Job " + str(codeb) + " removed.")


def gettime_script():
    print("Test")
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe ', 'pi@' + targetip,
               ' date ; exit ; exit']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    log(conout[0].decode("utf-8") + conout[1].decode("utf-8"))
    print("Done")


def clearlog_script():
    log_window.config(state='normal')
    log_window.delete('1.0', tk.END)
    log_window.config(state='disabled')


def vncviewer_script():
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\Program Files\RealVNC\VNC Viewer\\vncviewer.exe ', targetip]
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    log(str(comboips.get()) + '\n' * 2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))


def shutdown_script():
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
           ' \"sudo shutdown -h --no-wall now\"']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    log(str(comboips.get()) + ' Shutdown successfully')


def get_GPS_coords():
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
           ' \"gpspipe -r -n 8 | grep GPRMC | cut -d , -f 4-7\"']
    print("done")
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    log(str(comboips.get()) + ' coordinates: ' + conout[0].decode("utf-8"))
    gotstr = str(conout[0])
    gotstrb = gotstr.split("'")[1]
    print(gotstrb)
    long = float(gotstrb.split(",")[2])
    lat = float(gotstrb.split(",")[0])
    modlat = (lat - 100 * int(lat / 100)) / 60.0;
    modlat += int(lat / 100);
    if 'S' in gotstrb.split(",")[1]:
        modlat *= -1.0;
    modlon = (long - 100 * int(long / 100)) / 60.0;
    modlon += int(long / 100);
    if 'W' in gotstrb.split(",")[3]:
        modlon *= -1.0;
    write_to_kml(modlon, modlat)


def get_name_andfreq(eventObject):
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
           ' \" ls /range | grep py | grep -v "PTT" | grep -v "relay"\"']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    gotfreq = conout[0].decode("utf-8")
    #print(gotfreq)
    freqselect.config(values=gotfreq)
    freqselect.current(0)
    get_temp()


def get_temp():
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe -v', ' pi@' + targetip,
           ' \" /opt/vc/bin/vcgencmd measure_temp\"']
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    log(str(comboips.get()) + " " + conout[0].decode("utf-8"))


def write_to_kml(long, lat):
    kmlname = comboips.get() + "_coords.kml"
    kmlf = open(kmlname, "w")
    kmlf.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kmlf.close()
    kmlf = open(kmlname, "a")  # switch to append mode
    kmlf.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    kmlf.write("    <Placemark>\n")
    kmlf.write("        <name>" + comboips.get() + "</name>\n")
    kmlf.write("        <description>" + comboips.get() + " location</description>\n")
    kmlf.write("        <Point>\n")
    kmlf.write("            <coordinates>" + str(long) + "," + str(lat) + ",0</coordinates>\n")
    kmlf.write("        </Point>\n")
    kmlf.write("    </Placemark>\n")
    kmlf.write("</kml>\n")
    kmlf.close()


namelabel = tk.Label(
    text="Chimera DRED Controller",
    font=("Courier", 20),
    width=23,
    height=5
)

namelabel.grid(row=0, column=1, columnspan=5)

dselectlabel = tk.Label(
    text="Select DRED",
    width=11,
    height=3
)

dselectlabel.grid(row=1, column=0)

comboips = ttk.Combobox(window, values=goodipnames)
#comboips.current(0)

comboips.grid(row=2, column=0)

comboips.bind("<<ComboboxSelected>>", get_name_andfreq)

init_btn = tk.Button(window)
init_btn.grid(row=2, column=6, sticky="nsew")
init_btn.config(bg="black",
                fg="white",
                width=210,
                height=50,
                image=initphoto,
                compound=tk.LEFT,
                text="     INITIALIZE                  ")
init_btn.bind("<Button-1>", init_log)
init_btn.bind("<ButtonRelease-1>", init_go)

fselectlabel = tk.Label(
    text="Select File",
    width=13,
    height=3
)

fselectlabel.grid(row=4, column=0)

freqselect = ttk.Combobox(window, width=35, values=freqlist)
freqselect.current(0)

freqselect.grid(row=5, column=0)

#customfreqlabel = tk.Label(
#    text="OR enter custom file name",
#    width=20,
#    height=3
#)

#customfreqlabel.grid(row=6, column=0)

#freqentry = tk.Entry(
#    fg="black",
#    bg="white",
#    width=10
#)

#freqentry.grid(row=7, column=0)

#nselectlabel = tk.Label(
#    text="Select sound name",
#    width=14,
#    height=3
#)

#nselectlabel.grid(row=8, column=0)

#fileselect = ttk.Combobox(window, values=filelist)
#fileselect.current(0)

#fileselect.grid(row=9, column=0)

#customnamelabel = tk.Label(
#    text="OR enter custom name",
#    width=20,
#    height=3
#)

#customnamelabel.grid(row=10, column=0)

#nameentry = tk.Entry(
#    fg="black",
#    bg="white",
#    width=10
#)

#nameentry.grid(row=11, column=0)

minselectlabel = tk.Label(
    text="Minutes",
    width=14,
    height=3
)

minselectlabel.grid(row=10, column=1)

minentry = tk.Entry(
    fg="black",
    bg="white",
    width=10
)

minentry.grid(row=11, column=1)

houselectlabel = tk.Label(
    text="Hours",
    width=14,
    height=3
)

houselectlabel.grid(row=10, column=2)

houentry = tk.Entry(
    fg="black",
    bg="white",
    width=10
)

houentry.grid(row=11, column=2)

domselectlabel = tk.Label(
    text="Day of Month",
    width=14,
    height=3
)

domselectlabel.grid(row=10, column=3)

domentry = tk.Entry(
    fg="black",
    bg="white",
    width=10
)

domentry.grid(row=11, column=3)

monthselectlabel = tk.Label(
    text="Month",
    width=14,
    height=4
)

monthselectlabel.grid(row=10, column=4)

monthentry = tk.Entry(
    fg="black",
    bg="white",
    width=10
)

monthentry.grid(row=11, column=4)

dowselectlabel = tk.Label(
    text="Day of Week",
    width=14,
    height=5
)

dowselectlabel.grid(row=10, column=5)

dowentry = tk.Entry(
    fg="black",
    bg="white",
    width=10
)

dowentry.grid(row=11, column=5)

playsoundbutton = StandardButton("            Play Sound                  ", freqselect,  6, 0)

playsoundbutton = PlayLocalButton("            Play Sound Locally         ", freqselect,  7, 0)

addjobbutton = JobButton("       Add CRON Job                  ", freqselect, minentry, houentry, domentry, monthentry, dowentry, 10, 6)

resetjobbutton = ResetButton("    Reset CRON Jobs              ", 11, 6)

squeue = tk.Listbox(window, width=35, height=12)
#print(squeue.get(0))
#squeue.delete(0)
#print(squeue.get(0))
squeue.grid(row=12, column=0, columnspan=1, rowspan=3)

aqbutton = AddQueueButton("       Add to Queue                  ", freqselect, squeue, 12, 1)

pqbutton = PlayQueueButton("    Play Entire Queue              ", squeue, 13, 1)

dqbutton = DeleteQueueButton("   Delete Queue Item            ", squeue, 14, 1)

scbutton = ShowCronButton("    Show CRON jobs               ", 12, 6)

hbutton = HelpButton("       Help Button                  ", window, 0, 6)

timebutton = GetTimeButton("      Get DRED Time         ", 3, 6)

clearbutton = ClearLogButton("      Clear Log                ", 4, 6)

vncbutton = VNCButton("         Use VNC             ", 6, 6)

sdbutton = ShutDownButton("    Shutdown DRED              ", 14, 6)

coordbutton = coordButton("    Get DRED Coordinates             ", 5, 6)

codelabel = tk.Label(
    text="Job code",
    width=14,
    height=3
)

codelabel.grid(row=12, column=5, pady=12)

codeentry = tk.Entry(
    fg="black",
    bg="white",
    width=15
)

codeentry.grid(row=13, column=5)

rcbutton = RemoveCronButton("    Remove CRON Job            ", codeentry, 13, 6)


window.mainloop()
