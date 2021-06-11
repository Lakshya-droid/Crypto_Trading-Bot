from binance import BinanceClient
from bitmex import BitmexClient
from root_component import Root
from tkinter import *
from tkinter import messagebox
import pandas as pd
from encdec import encr
from encdec import decr

class Login():
    def __init__(self,root1):
        self.root1=root1
        self.root1.title("Crypto-Trade Bot")
        self.photo = PhotoImage(file="bitcoin.png")
        self.root1.iconphoto(False, self.photo)
        self.width = self.root1.winfo_screenwidth()

        self.height = self.root1.winfo_screenheight()

        self.root1.geometry("%dx%d" %(self.width, self.height))
        self.root1.resizable(False,False)
        self.bg=PhotoImage(file="cryptobg.png")

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
        global h
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
            if decr(pas[idd.index(a)])==str(b):
                c = idd.index(a)
                self.bpk = decr(self.df.bpk[c])
                self.bsk = decr(self.df.bsk[c])
                self.btpk = self.df.btpk[c]
                self.btsk = self.df.btsk[c]
                self.dark=self.df.dark[c]
                df1=pd.DataFrame([[self.bpk,self.bsk,self.btpk,self.btsk,self.dark]],columns=["bpk","bsk","btpk","btsk","dark"])
                df1.to_csv('inp.csv', index=False)
                messagebox.showinfo("Welcome", "Welcome user ", parent=self.root1)
                self.mainWindow()
            else:
                messagebox.showerror("Error", "Invalid Password", parent=self.root1)

    def mainWindow(self):

        self.binance = BinanceClient(self.bpk,
                                self.bsk,
                                testnet=True, futures=True)
        self.bitmex = BitmexClient(self.btpk,
                                self.btsk,
                              testnet=True)
        self.root1.destroy()

        self.root = Root(self.binance, self.bitmex)
        self.root.resizable(False, False)
        self.root.mainloop()



    def openNewWindow(self):
        self.newWindow = Toplevel(self.root1)
        self.newWindow.title("Crypto-Trade Bot Register")
        self.newWindow.iconphoto(False, self.photo)
        self.newWindow.geometry("%dx%d" % (self.width,self.height))
        self.bg1 = PhotoImage(file="cryptobg.png")

        self.bg1_image = Label(self.newWindow, image=self.bg1).place(x=0, y=0, relheight=1, relwidth=1)

        Frame_login = Frame(self.newWindow, bg="white")
        Frame_login.place(x=150, y=45, height=700, width=500)
        title = Label(Frame_login, text="Register Here", font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=90,y=25)
        desc = Label(Frame_login, text="WELCOME NEW USERS ", font=("Goudy old style", 14, "bold"), fg="#d77337",bg="white").place(x=90, y=95)
        lb1_user = Label(Frame_login, text="Username", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=125)
        self.txt_user1 = Entry(Frame_login, font=("times new roman", 14), bg="lightgray")
        self.txt_user1.place(x=90, y=155, width=350, height=30)
        lb2_pass = Label(Frame_login, text="Password", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=195)
        self.txt_ps1 = Entry(Frame_login, font=("times new roman", 14), bg="lightgray")
        self.txt_ps1.place(x=90, y=225, width=350, height=30)
        lb2_currency = Label(Frame_login, text="Currency", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=265)

        currency_name = ["US Dollar (USD)", "Euro(EUR)", "Indian rupee(INR)", "Japanese Yen(JPY)",
                         "Pound Sterling (GBP)", "Australian Dollar (AUD)", "Canadian Dollar(CAD)", "Swiss Franc(CHF) ",
                         "Chinese Renminbi (CNY) "]
        currency_sym = ["USD","EUR", "INR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY"]
        self.curr = StringVar()
        self.curr.set(currency_name[0])
        self.curr1 = OptionMenu(Frame_login,self.curr,*currency_name)
        self.curr1.place(x=200, y=265)
        self.curr_sym=currency_sym[currency_name.index(self.curr.get())]
        lb2_platform = Label(Frame_login, text="Platform", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=305)
        self.binsf = StringVar(value="test")
        off_button2 = Radiobutton(Frame_login, text="Test", variable=self.binsf, indicatoron=False, value="test", width=10)
        off_button2.place(x=250, y=305)
        on_button2 = Radiobutton(Frame_login, text="Trade", variable=self.binsf, indicatoron=False, value="trade", width=10)
        on_button2.place(x=330, y=305)
        lb1_Binance_pub_key = Label(Frame_login, text="Binance Public API Key", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=345)
        self.bpk = Entry(Frame_login, font=("times new roman", 14), bg="lightgray")
        self.bpk.place(x=90, y=375, width=350, height=30)
        lb1_Binance_sec_key = Label(Frame_login, text="Binance Secret API Key", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=415)
        self.bsk = Entry(Frame_login, font=("times new roman", 14), bg="lightgray")
        self.bsk.place(x=90, y=445, width=350, height=30)
        lb1_bitmex_pub_key = Label(Frame_login, text="Bitmex Public API Key", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=485)
        self.btpk = Entry(Frame_login, font=("times new roman", 14), bg="lightgray")
        self.btpk.place(x=90, y=515, width=350, height=30)
        lb1_bitmex_sec_key = Label(Frame_login, text="Bitmex Secret API Key", font=("Goudy old style", 14, "bold"), fg="gray",bg="white").place(x=90, y=555)
        self.btsk = Entry(Frame_login, font=("times new roman", 14), bg="lightgray")
        self.btsk.place(x=90, y=585, width=350, height=30)
        lb1_bitmex_sec_key = Label(Frame_login, text="Dark Mode", font=("Goudy old style", 14, "bold"),fg="gray", bg="white").place(x=90, y=625)
        self.dmv = StringVar(value="on")
        off_button2 = Radiobutton(Frame_login, text="OFF", variable=self.dmv,indicatoron=False, value="off", width=8)
        off_button2.place(x=280,y=625)
        on_button2 = Radiobutton(Frame_login, text="ON", variable=self.dmv,indicatoron=False, value="on", width=8)
        on_button2.place(x=220, y=625)
        nuser = Button(Frame_login, text="Existing User -> Log-In", bg="white", fg="#d77337", bd=0,font=("times new roman", 12),command=lambda: self.exit_btn()).place(x=90, y=655)
        Login_btm = Button(self.newWindow, text="Sign-Up", bg="#d77337", fg="white", font=("times new roman", 12),command=lambda: self.loginbut()).place(x=300, y=730, width=180, height=40)

    def exit_btn(self):
        self.newWindow.destroy()
        self.newWindow.update()

    def loginbut(self):
        self.df = pd.read_csv("out.csv")
        if self.txt_ps1.get()=="" or self.txt_user1.get()=="":
            messagebox.showerror("Error","All feilds are required",parent=self.newWindow)

        elif self.txt_user1.get() not in list(self.df['id']):

            messagebox.showinfo("Success", "Now you can login with your id and pass", parent=self.root1)
            self.df=self.df.append(pd.DataFrame(pd.DataFrame([[self.txt_user1.get(),encr(self.txt_ps1.get()),encr(self.bpk.get()),encr(self.bsk.get()),self.btpk.get(),self.btsk.get(),self.curr_sym,self.dmv.get(),self.binsf.get()]],columns=["id","pas","bpk","bsk","btpk","btsk","curr","dark","test"])))
            self.df.to_csv('out.csv', index=False)
            self.exit_btn()
        else:
            messagebox.showinfo("Error", "USERNAME not unique", parent=self.newWindow)
