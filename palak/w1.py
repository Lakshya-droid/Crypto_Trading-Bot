import tkinter

from binance import BinanceClient
from bitmex import BitmexClient
from root_component import Root
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import pandas as pd

class Login(Tk):
    def __init__(self):
        self.root1.title("Crypto-Trade Bot")
        self.root1.geometry("1199x600+100+50")
        self.root1.resizable(False,False)
        self.bg=PhotoImage(file="cryptob.png")

        self.bg_image=Label(self.root1,image=self.bg).place(x=0,y=0,relheight=1,relwidth=1)

        Frame_login=Frame(self.root1,bg="white")
        Frame_login.place(x=150,y=150,height=340,width=500)
        title=Label(Frame_login,text="Login Here", font=("Impact",35,"bold") ,fg="#d77337", bg="white").place(x=90,y=30)
        desc=Label(Frame_login,text="WELCOME USERS ", font= ("Goudy old style",15,"bold") ,fg="#d77337", bg="white").place(x=90,y=100)
        lb1_user=Label(Frame_login,text="Username", font= ("Goudy old style",15,"bold") ,fg="gray", bg="white").place(x=90,y=140)
        self.txt_user=Entry(Frame_login,font=("times new roman",15),bg="lightgray")
        self.txt_user.place(x=90,y=170,width=350,height=35)
        lb2_pass = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="gray",bg="white").place(x=90, y=210)
        self.txt_ps = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
        self.txt_ps.place(x=90, y=240, width=350, height=35)
        nuser=Button(Frame_login,text="New User -> Log-In",bg="white",fg="#d77337",bd=0,font=("times new roman" ,12),command=lambda: self.openNewWindow()).place(x=90,y=280)
        Login_btm = Button(self.root1 ,text="Login", bg="#d77337", fg="white",font=("times new roman", 12),command=lambda: self.signinbut()).place(x=300, y=470,width=180,height=40)
    def signinbut(self):
        self.df = pd.read_csv("out.csv")
        idd= list(self.df['id'])
        pas=list(self.df['pas'])
        a=self.txt_user.get()
        b=self.txt_ps.get()
        if self.txt_ps.get()=="" or self.txt_user.get()=="":
            messagebox.showerror("Error","All feilds are required",parent=self.root1)
        elif self.txt_user.get() not in list(self.df['id']):
            messagebox.showerror("Error", "Invalid Id - Password", parent=self.root1)
        else:
            if pas[idd.index(a)]==b:
                messagebox.showinfo("Welcome", "Welcome user ", parent=self.root1)
                self.mainWindow()
            else:
                messagebox.showerror("Error", "Invalid Password", parent=self.root1)

    def mainWindow(self):
        binance = BinanceClient("6c81732fb1de94e3ef9109ac964d92098e59589e3671ff3ba6fe66adfa4ca457",
                                "05b675afc40784573fd828d97f2d976429a1e1af123a20aa777272bc05b82a3a",
                                testnet=True, futures=True)
        bitmex = BitmexClient("KGJ3eKLhffOGukU_19zfmHYC", "1xyWxXnc9gUfiD7ExU-NC0sMLu-xl7wH6pcn6IiIeso3ugLH",
                              testnet=True)
        self.root1.destroy()

        self.root = Root(binance, bitmex)
        self.root.resizable(False, False)

        self.root.mainloop()



    def openNewWindow(self):
        self.newWindow = Toplevel(root1)
        self.newWindow.title("Crypto-Trade Bot Register")
        self.newWindow.geometry("1199x600+100+50")
        self.newWindow.resizable(False, False)
        self.bg1 = PhotoImage(file="cryptob.png")

        self.bg1_image = Label(self.newWindow, image=self.bg1).place(x=0, y=0, relheight=1, relwidth=1)

        Frame_login = Frame(self.newWindow, bg="white")
        Frame_login.place(x=150, y=150, height=340, width=500)
        title = Label(Frame_login, text="Register Here", font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=90,
                                                                                                                   y=30)
        desc = Label(Frame_login, text="WELCOME NEW USERS ", font=("Goudy old style", 15, "bold"), fg="#d77337",
                     bg="white").place(x=90, y=100)
        lb1_user = Label(Frame_login, text="Username", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=90, y=140)
        self.txt_user = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
        self.txt_user.place(x=90, y=170, width=350, height=35)
        lb2_pass = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=90, y=210)
        self.txt_ps = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
        self.txt_ps.place(x=90, y=240, width=350, height=35)
        nuser = Button(Frame_login, text="Existing User -> Log-Up", bg="white", fg="#d77337", bd=0,
                       font=("times new roman", 12),command=lambda: self.exit_btn()).place(x=90, y=280)
        Login_btm = Button(self.newWindow, text="Sign-Up", bg="#d77337", fg="white", font=("times new roman", 12),
                           command=lambda: self.loginbut()).place(x=300, y=470, width=180, height=40)

    def exit_btn(self):
        self.newWindow.destroy()
        self.newWindow.update()

    def loginbut(self):
        self.df = pd.read_csv("out.csv")
        if self.txt_ps.get()=="" or self.txt_user.get()=="":
            messagebox.showerror("Error","All feilds are required",parent=self.newWindow)

        elif self.txt_user.get() not in list(self.df['id']):

            messagebox.showinfo("Success", "Now you can login with your id and pass", parent=self.root1)
            self.df=self.df.append(pd.DataFrame(pd.DataFrame([[self.txt_user.get(),self.txt_ps.get()]],columns=["id","pas"])))
            self.df.to_csv('out.csv', index=False)


        else:
            messagebox.showinfo("Error", "USERNAME not unique", parent=self.newWindow)

