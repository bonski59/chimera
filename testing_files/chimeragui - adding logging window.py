import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText
import subprocess
import csv
import time
import logging
import os.path as ostest


logging.basicConfig(filename='test.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')
logging.Formatter(datefmt='%Y-%m-%d %H:%M:%S')


class gsm:
    name = "GSM"
    testfile = '/home/pi/phonescripts/testgsm.sh'
    message_file = '/home/pi/phonescripts/gsmmess.sh'
    call_file = '/home/pi/phonescripts/gsmcall.sh'
    toggle_file = '/home/pi/phonescripts/gsmtoggle.sh'


class CDMA:
    name = "CDMA"
    testfile = '/home/pi/phonescripts/testcdma.sh'
    message_file = '/home/pi/phonescripts/cdmamess.sh'
    call_file = '/home/pi/phonescripts/cdmacall.sh'
    toggle_file = '/home/pi/phonescripts/cdmatoggle.sh'


class umts:
    name = "UMTS"
    testfile = '/home/pi/phonescripts/testumts.sh'
    message_file = '/home/pi/phonescripts/umtsmess.sh'
    call_file = '/home/pi/phonescripts/umtscall.sh'
    toggle_file = '/home/pi/phonescripts/umtstoggle.sh'


class LTE:
    name = "LTE"
    testfile = '/home/pi/phonescripts/testlte.sh'
    message_file = '/home/pi/phonescripts/ltemess.sh'
    call_file = '/home/pi/phonescripts/ltecall.sh'
    toggle_file = '/home/pi/phonescripts/ltetoggle.sh'


window = tk.Tk()
window.columnconfigure([0, 1, 2, 3, 4, 5], minsize=50)
window.rowconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50)

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

namelabel = tk.Label(
    text="Chimera ToughBucket Controller",
    font=("Courier", 20),
    width=30,
    height=5
)

namelabel.grid(row=0, column=1, columnspan=4)

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


log_window = ScrolledText.ScrolledText(window, state='disabled')
log_window.grid(row=3, column=2, rowspan=4, columnspan=4, sticky="nsew")
log_window.config(background="white")
# ALW is Action Logging Window
ALW = TextHandler(log_window)


logger = logging.getLogger()
logger.addHandler(ALW)


def log(message):
    logging.info(time.asctime() + " - " + message)


badips = []
goodips = []
goodipnames = [""]


def scan_iplist():
    scanips = []
    with open('iplist.csv') as iplist_csv:
        csv_reader = csv.reader(iplist_csv, delimiter=',')
        for row in csv_reader:
            scanips.append(row)
    print(scanips)

    return scanips


def find_good_ips(iplist_array):
    global badips
    badips = []
    global goodips
    goodips = []
    global goodipnames
    goodipnames = [""]
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
    if len(badips) >= 0:
        log("Missing:  " + str(list_bad_TB))
        log("Found:    " + str(list_good_TB))
        log("Select Device to operate with the drop down above...")
    if len(goodips) == 0:
        log("No Tough Buckets loaded. Check Power and Wifi connections...")
    for x in goodips:
        goodipnames.append(x[1])
    comboips.config(values=goodipnames)
    comboips.current(0)


def module_action(name, script_path):
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
            if name == gsm.name:
                protocol = 2
            elif name == umts.name:
                protocol = 4
            print(x[protocol])
            if x[protocol] == "0":
                log("This protocol is not supported by the chosen toughbucket")
                return
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', 'pi@' + targetip, '/bin/sh', '-c',
           script_path]

    conout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # print(conout.decode("utf-8"))
    log(str(comboips.get()) + '\n'*2 + conout[0].decode("utf-8") + conout[1].decode("utf-8"))


def init_log(event):
    log("Scanning for devices. Please wait...")
    obj_list = []
    with open('iplist.csv') as iplist_csv:
        csv_reader = csv.reader(iplist_csv, delimiter=',')
        for row in csv_reader:
            obj_list.append(row[1])
    log("Scanning: " + str(obj_list))
    return obj_list


def init_go(event):
    x = scan_iplist()
    find_good_ips(x)

def get_GPS_coords(fillobj):
    targetip = "0.0.0.0"
    for x in goodips:
        if x[1] == comboips.get():
            print(comboips.get())
            targetip = x[0]
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', ' pi@' + targetip, ' /bin/sh', ' -c',
           ' /home/pi/phonescripts/getgps.sh']
    print("done")
    cmdb = ''.join(cmd)
    print(cmdb)
    conout = subprocess.Popen(cmdb, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(str(comboips.get()) + ' coordinates: ' + conout[0].decode("utf-8"))
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


init_btn = tk.Button(window)
init_btn.grid(row=1, column=3, rowspan=2, columnspan=2, sticky="nsew")
init_btn.config(bg="black",
                fg="white",
                text="INITIALIZE")
init_btn.bind("<Button-1>", init_log)
init_btn.bind("<ButtonRelease-1>", init_go)

comboips = ttk.Combobox(window, values=goodipnames)
comboips.current(0)

comboips.grid(row=2, column=0)

comboips.bind("<<ComboboxSelected>>", get_GPS_coords)

tbiplabel = tk.Label(
    text="Select Device",
    width=11,
    height=3
)

tbiplabel.grid(row=1, column=0)

tbipentry = tk.Entry(
    fg="Yellow",
    bg="blue",
    width=30
)

tbipentry.grid(row=2, column=1)


class StandardButton(tk.Button):
    def __init__(self, text, name, actfile, rw, cl, **kw):
        super().__init__(**kw)
        self.config(text=text, fg="white", bg="black", width=30, height=7,
                    command=lambda: module_action(name, actfile) or None)
        self.grid(row=rw, column=cl)


testgsmbutton = StandardButton("Test SIM/Modem", gsm.name, gsm.testfile, 3, 0)
messagegsmbutton = StandardButton("Send Text Message", gsm.name, gsm.message_file, 4, 0)
callgsmbutton = StandardButton("Make a Call", gsm.name, gsm.call_file, 5, 0)
togglegsmbutton = StandardButton("Switch to GSM", gsm.name, gsm.toggle_file, 3, 1)
#testutmsbutton = StandardButton("Test UMTS", umts.name, umts.testfile, 2, 1)
#messageutmsbutton = StandardButton("Send UMTS Message", umts.name, umts.message_file, 3, 1)
#callutmsbutton = StandardButton("Make UMTS Call", umts.name, umts.call_file, 4, 1)
toggleutmsbutton = StandardButton("Switch to UMTS", umts.name, umts.toggle_file, 4, 1)

window.mainloop()
