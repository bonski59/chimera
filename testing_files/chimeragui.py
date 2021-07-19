import tkinter as tk
from tkinter import ttk
import subprocess
import ctypes
import csv
import threading


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


def opening_thread():
    ctypes.windll.user32.MessageBoxW(0, "Scanning for devices. Please wait...", "Output", 0)


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


trd = threading.Thread(target=opening_thread)
trd.start()

with open('iplist.csv') as iplist_csv:
    csv_reader = csv.reader(iplist_csv, delimiter=',')
    scanips = []
    for row in csv_reader:
        print(row[0])
        scanips.append(row)

print(scanips)
badips = []
goodips = []

for x in scanips:
    print(x[0])
    gip = str(x[0])
    print("Scanning " + gip)
    cmd = ['C:\\Windows\\System32\\PING.EXE', '-n', '2', gip]
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    # print(result.decode("utf-8"))
    if result.decode("utf-8").find("unreachable") > -1:
        print("Address not found: " + gip)
        badips.append(x)
    else:
        goodips.append(x)

trd.join()
if len(badips) > 0:
    ctypes.windll.user32.MessageBoxW(0, "The following ips cannot be found: " + str(badips), "Output", 0)
if len(goodips) == 0:
    ctypes.windll.user32.MessageBoxW(0, "No toughbuckets loaded. Program is exiting...", "Output", 0)
    exit()

goodipnames = []
for x in goodips:
    goodipnames.append(x[1])


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
                ctypes.windll.user32.MessageBoxW(0, "This protocol is not supported by the chosen toughbucket", "Output", 0)
                return
    cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', 'pi@' + targetip, '/bin/sh', '-c',
           script_path]

    conout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # print(conout.decode("utf-8"))
    ctypes.windll.user32.MessageBoxW(0, conout[0].decode("utf-8") + conout[1].decode("utf-8"), "Output", 0)


window = tk.Tk()
window.columnconfigure([0, 1, 2], minsize=50)
window.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50)

comboips = ttk.Combobox(window, values=goodipnames)
comboips.current(0)

comboips.grid(row=1, column=0)

comboips.bind("<<ComboboxSelected>>", get_GPS_coords)

tbiplabel = tk.Label(
    text="Select Device",
    width=11,
    height=3
)

tbiplabel.grid(row=0, column=0)

tbipentry = tk.Entry(
    fg="Yellow",
    bg="blue",
    width=30
)

tbipentry.grid(row=1, column=1)

testgsmbutton = tk.Button(
    text="Test GSM",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(gsm.name, gsm.testfile)
)

testgsmbutton.grid(row=2, column=0)

messagegsmbutton = tk.Button(
    text="Send GSM Message",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(gsm.name, gsm.message_file)
)

messagegsmbutton.grid(row=3, column=0)

callgsmbutton = tk.Button(
    text="Make GSM Call",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(gsm.name, gsm.call_file)
)

callgsmbutton.grid(row=4, column=0)

togglegsmbutton = tk.Button(
    text="Toggle GSM Power",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(gsm.name, gsm.toggle_file)
)

togglegsmbutton.grid(row=5, column=0)

testutmsbutton = tk.Button(
    text="Test UMTS",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(umts.name, umts.testfile)
)

testutmsbutton.grid(row=2, column=1)

messageutmsbutton = tk.Button(
    text="Send UMTS Message",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(umts.name, umts.message_file)
)

messageutmsbutton.grid(row=3, column=1)

callutmsbutton = tk.Button(
    text="Make UMTS Call",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(umts.name, umts.call_file)
)

callutmsbutton.grid(row=4, column=1)


toggleutmsbutton = tk.Button(
    text="Toggle UMTS Power",
    fg="white",
    bg="black",
    width=30,
    height=7,
    command=lambda : module_action(umts.name, umts.toggle_file)
)

toggleutmsbutton.grid(row=5, column=1)

window.mainloop()
