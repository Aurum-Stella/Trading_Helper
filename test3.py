
from tkinter import *
import tkinter.messagebox
import tkinter
from tkinter import ttk
import json

column = 0
row = 0

with open('DB.json', 'r') as w:

    oll_dict = json.load(w)
    oll_keys = [i for i in oll_dict.keys()]
    print(oll_keys)

ain_notebook_controll = ttk.Notebook(width=1280, height=700)
a_tab = ttk.Frame(main_notebook_controll)
b_tab = ttk.Frame(main_notebook_controll)
#c_tab = ttk.Frame(main_notebook_controll)
main_notebook_controll.add(a_tab, text="Notebook A")
main_notebook_controll.add(b_tab, text="Notebook B")
#main_notebook_controll.add(c_tab, text="Notebook C")


draw = Canvas(a_tab, width=1280, height=700, scrollregion = (0,0, 230, 5000))
draw.sbar = Scrollbar(orient=VERTICAL)
frame = Frame(draw)


draw.create_window(0, 0, window=frame, width=230, height=5000, anchor=N+W)

Button(frame, text=f"asd",  width = 15, height = 2).grid(row=row, column=column, padx=5, pady=5)
Button(frame, text=f"asd",  width = 15, height = 2).grid(row=row, column=column, padx=5, pady=5)

#for i in oll_keys:
#    
#    tab = ttk.Frame(main_notebook_controll)
#    main_notebook_controll.add(tab, text=f"{i}")
#    
#    draw = Canvas(tab, width=1280, height=700, scrollregion = (0,0, 230, 5000))
#    draw.sbar = Scrollbar(orient=VERTICAL)
#    frame = Frame(draw)
#    draw.create_window(0, 0, window=frame, width=1280, height=700, anchor=N+W)
#    
#    for r in oll_dict[i]:
#        if column > 7:
#            column = 0
#            row += 1
#        Button(frame, text=f"{r}",  width = 15, height = 2).grid(row=row, column=column, padx=5, pady=5)
#        column += 1
#        
draw['yscrollcommand'] = draw.sbar.set
draw.sbar['command'] = draw.yview
draw.sbar.pack(side=RIGHT, fill=Y)
main_notebook_controll.pack()



draw.pack()


mainloop()



