import tkinter as tk


def test_button_click():
    print("The button was clicked!")


def entry_button_click():
    print("The entered value is " + entry.get())


def text_box_button_click():
    print(text_box.get("1.0", tk.END))


window = tk.Tk()

winframe = tk.Frame(master=window, width=680, height=640)
winframe.pack()

greeting = tk.Label(text="Hello, Tkinter")
greeting.place(x=0,y=0)

biglabel = tk.Label(
    text="Test",
    fg="white",
    bg="black",
    width=10,
    height=10
)

biglabel.place(x=100, y=0)

button = tk.Button(
    text="Test Button",
    fg="white",
    bg="black",
    width=10,
    height=10,
    command=test_button_click
)

button.place(x=200, y=0)

# entries get one line

entry = tk.Entry(
    fg="Yellow",
    bg="blue",
    width=45
)

entry.place(x=10, y=170)

entrybutton = tk.Button(
    text="Enter",
    width=10,
    height=1,
    command=entry_button_click
)

entrybutton.place(x=300, y=170)

# text gets multiple lines of text

text_box = tk.Text()

text_box.place(x=10, y=200)

textbotbutton = tk.Button(
    text="Finish",
    width=10,
    height=1,
    command=text_box_button_click
)

textbotbutton.place(x=300, y=600)

window.mainloop()