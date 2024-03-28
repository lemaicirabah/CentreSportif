import tkinter as tk
from tkinter import NW
from Profil import open_profile_window


app = tk.Tk()
app.title("Centre Sportif")
app.config(bg="gray30")
app.geometry("400x600")
app.iconbitmap("log.ico")

navIcon = tk.PhotoImage(file='menu.png')
closeIcon = tk.PhotoImage(file='close.png')
fontImage = tk.PhotoImage(file='font.png')

btnEtat = False

def switch():
    global btnEtat
    if btnEtat is True:

        for x in range(300):
            navLateral.place(x=-x ,y=0)
            topFrame.update()
        BannerText.config(bg="#E6E8E9")
        accueilText.config(bg="#800080")
        topFrame.config(bg="#800080")
        app.config(bg="gray30")
        btnEtat=False
    else:
        for x in range(-300,0):
            navLateral.place(x=x,y=0)
            topFrame.update()
            btnEtat = True

topFrame = tk.Frame(app , bg = "#800080")
topFrame.pack(side="top",fill=tk.X)

accueilText = tk.Label(topFrame , font= "ExtraCondensed 15" , bg="#800080" ,height=2 ,padx=20)
accueilText.pack(side="right")

can = tk.Canvas(app, width="400", height="600")
can.create_image(0,0,anchor=NW,image=fontImage)
can.pack()

BannerText = tk.Label(app, text="Centre Sportif" , font="ExtraCondensed 25" ,bg="#E6E8E9", fg="#800080")
BannerText.place(x=50 , y=550)

navBarBtn = tk.Button(topFrame,image=navIcon,bg="#800080" , bd=0 , activebackground="#800080",command=switch)
navBarBtn.place(x=10,y=10)

navLateral = tk.Frame(app,bg="gray30" ,width="300",height="600")
navLateral.place(x=-300,y=0)
tk.Label(navLateral,font="ExtraCondensed 15",bg="#800080",fg="black")

y=80

option = ["ACCUEIL" , "PAGES" , "PROFIL" , "PARAMETRES" , "AIDE"]

for i in range(5):
    if option[i] == "PROFIL":
        # Si l'option est "PROFIL", le bouton ouvrira la fenêtre de profil
        tk.Button(navLateral, text=option[i], font="ExtraCondensed 16", bg="gray30", fg="white", activebackground="gray30", bd=0, command=open_profile_window).place(x=0, y=y)
    else:
        # Pour les autres options, créez le bouton sans lier à une commande spécifique
        tk.Button(navLateral, text=option[i], font="ExtraCondensed 16", bg="gray30", fg="white", activebackground="gray30", bd=0).place(x=0, y=y)
    y += 40
fermeBtn = tk.Button(navLateral,image=closeIcon,bg="gray30" , bd=0 , activebackground="gray30",command=switch)
fermeBtn.place(x=250,y=10)
app.mainloop()
