import tkinter as tk
from tkinter import NW
from Profil import open_profile_window
from python.activite import open_activite_window


def open_main_window(self=None):
    main_app_window = tk.Toplevel(self)
    main_app_window.title("Centre Sportif")
    main_app_window.config(bg="gray30")
    main_app_window.geometry("400x600")
    main_app_window.resizable(False, False)
    # Chargez les images
    navIcon = tk.PhotoImage(file='../images/menu.png')
    closeIcon = tk.PhotoImage(file='../images/close.png')
    fontImage = tk.PhotoImage(file='../images/font.png')
    # Note: Pour éviter le garbage collection sur les images, attachez-les à la fenêtre
    main_app_window.navIcon = navIcon
    main_app_window.closeIcon = closeIcon
    main_app_window.fontImage = fontImage

    btnEtat = False

    def switch():
        nonlocal btnEtat
        if btnEtat:
            for x in range(300):
                navLateral.place(x=-x, y=0)
                topFrame.update()
            btnEtat = False
        else:
            for x in range(-300, 0):
                navLateral.place(x=x, y=0)
                topFrame.update()
            btnEtat = True

    topFrame = tk.Frame(main_app_window, bg="#800080")
    topFrame.pack(side="top", fill=tk.X)

    accueilText = tk.Label(topFrame, font="ExtraCondensed 15", bg="#800080", height=2, padx=20)
    accueilText.pack(side="right")

    can = tk.Canvas(main_app_window, width=400, height=600)
    can.create_image(0, 0, anchor=NW, image=fontImage)
    can.pack()

    BannerText = tk.Label(main_app_window, text="Centre Sportif", font="ExtraCondensed 25", bg="#E6E8E9",
                          fg="#800080")
    BannerText.place(x=50, y=550)

    navBarBtn = tk.Button(topFrame, image=navIcon, bg="#800080", bd=0, activebackground="#800080",
                          command=switch)
    navBarBtn.place(x=10, y=10)

    navLateral = tk.Frame(main_app_window, bg="gray30", width=300, height=600)
    navLateral.place(x=-300, y=0)

    y = 80
    options = ["INSCRIPTION", "ACTIVITES", "HORAIRES", "PAIEMENT", "PROFIL"]
    for i, option in enumerate(options):
        if option == "PROFIL":
            tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                      activebackground="gray30", bd=0, command=open_profile_window).place(x=0, y=y)
        elif option == "ACTIVITES":
            tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                      activebackground="gray30", bd=0, command=open_activite_window).place(x=0, y=y)
        elif option == "HORAIRES":
            tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                      activebackground="gray30", bd=0, command=open_activite_window).place(x=0, y=y)

        elif option == "PAIEMENT":
            tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                      activebackground="gray30", bd=0, command=open_activite_window).place(x=0, y=y)

        else:
            tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                      activebackground="gray30", bd=0).place(x=0, y=y)
        y += 40

    fermeBtn = tk.Button(navLateral, image=closeIcon, bg="gray30", bd=0, activebackground="gray30",
                         command=switch)
    fermeBtn.place(x=250, y=10)
    main_app_window.mainloop()
