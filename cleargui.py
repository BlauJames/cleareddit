import tkinter as tk
from tkinter.constants import NSEW
import cleareddit


class login:
    def __init__(self, master):
        self.settings = []
        
        
        self.users = cleareddit.getusers()
        if self.users == []:
            self.users = ['Add User']
        
        self.master = master
        
        
        self.clicked = tk.StringVar()
        self.clicked.set(self.users[0])
        self.userdrop = tk.OptionMenu(self.master,self.clicked,*self.users)
        self.userdrop.grid(row=0,column=0,columnspan = 2,padx=5,sticky="ew")
        
        
        self.addcred = tk.Button(self.master,text = "Add User",command= self.adduser)#,command = adduser()) ToDo add class for window to add user
        self.addcred.grid(row=0,column=2,sticky="ew")
        
        
        self.delcred = tk.Button(self.master, text = "Delete User")#, command = deleteuser()) Add method in cleareddit to delete user
        self.delcred.grid(row=0,column=3,padx=5,sticky="ew")

        self.mnvlab = tk.Label(self.master, text="Minimum Votes")
        self.mnvlab.grid(row=1,column=0,padx=5,sticky="w")
        self.minvotes = tk.StringVar()        # self.minvotes.set(-10000000)
        self.minvoteent = tk.Entry(self.master,textvariable=self.minvotes)
        self.minvoteent.grid(row=1,column=1,padx=5,sticky="ew")
        
        
        self.mxvlab = tk.Label(self.master, text="Maximum Votes")
        self.mxvlab.grid(row=1,column=2,padx=5,sticky="w")
        self.maxvotes = tk.StringVar()
        # self.maxvotes.set(10000000)
        self.maxvoteent = tk.Entry(self.master,textvariable=self.maxvotes)
        self.maxvoteent.grid(row=1,column=3,padx=5,sticky="ew")


        self.edlab = tk.Label(self.master, text="Newest days ago")
        self.edlab.grid(row=2,column=0,padx=5,sticky="w")
        self.enddays = tk.StringVar()
        # self.enddays.set(0)
        self.edent = tk.Entry(self.master,textvariable=self.enddays)
        self.edent.grid(row=2,column=1,padx=5,sticky="ew")


        self.sdlab = tk.Label(self.master, text="Oldest days ago")
        self.sdlab.grid(row=2,column=2,padx=5,sticky="w")
        self.startdays = tk.StringVar()
        # self.startdays.set(10000)
        self.sdent = tk.Entry(self.master,textvariable=self.startdays)
        self.sdent.grid(row=2,column=3,padx=5,sticky="ew")

        
        self.subdel = tk.IntVar()
        self.dsb = tk.Checkbutton(self.master, text="Delete Posts", onvalue = 1, offvalue = 0,variable = self.subdel)
        self.dsb.grid(row=3,column=0,padx=5)
        
        
        self.comdel =tk.IntVar()
        self.dcb = tk. Checkbutton(self.master,text="Delete Comments",variable = self.comdel)
        self.dcb.grid(row=3,column=1,padx=5)
        
        
        self.awarded = tk.IntVar
        self.awardcheck = tk. Checkbutton(self.master, text="Keep Awards", onvalue = 1, offvalue = 0, variable = self.awarded)
        self.awardcheck.grid(row=3,column=3,padx=5)
        
        
        self.listtype = tk.IntVar()
        self.bwlist = tk.Checkbutton(self.master, text="Blacklist/Whitelist", onvalue = 1, offvalue = 0, variable = self.listtype)
        self.bwlist.grid(row=3,column=2,padx=5)


        self.close = tk.Button(self.master, text='Quit')
        self.close.grid(row=4,column=1,padx=5,sticky="ew")
        
        
        self.clear = tk.Button(self.master, text='Cleareddit')
        self.clear.grid(row=4,column=2,sticky="ew")
        
        
        self.settingbut = tk.Button(self.master, text='Select Subreddits',command = self.subselect)
        self.settingbut.grid(row=4,column=3,padx=5,sticky="ew")
        self.sets = [self.clicked,self.minvotes,self.maxvotes,self.enddays,self.startdays,self.comdel,self.subdel,self.listtype]

    def adduser(self):
        self.usermenu = tk.Toplevel()


        self.entries = {}
        self.fields = ['Client ID', 'Client Secret', 'Password', 'User Agent', 'Username']


        for field in self.fields:
            print(field)
            self.row = tk.Frame(self.usermenu)
            self.lab = tk.Label(self.row, width=22, text=field+": ", anchor='w')
            self.ent = tk.Entry(self.row)
            self.row.pack(side=tk.TOP, 
                    fill=tk.X, 
                    padx=5, 
                    pady=5)
            self.lab.pack(side=tk.LEFT)
            self.ent.pack(side=tk.RIGHT, 
                    expand=tk.YES, 
                    fill=tk.X)
            self.entries[field,self.ent.get()]


        self.create = tk.Button(self.usermenu, text='Create User', command= self.checkcreds)

        self.close = tk.Button(self.usermenu, text='Quit')
        
        self.close.pack()
        
        self.create.pack(side = tk.BOTTOM)

    def deluser(self):
        self.var = []

    def checkcreds(self):
        self.credentials = []
        for entry in self.entries:
            print(entry.get())
            self.credentials.append(entry.get())
        self.success,self.unique,self.user = cleareddit.createredditor(self.credentials)
        if self.success == True and self.unique == True:
            self.clicked.set(self.user)
            print("User added")
            self.userdrop["menu"].add_command(label = self.user,command = tk._setit(self.clicked,self.user))
            self.usermenu.destroy()
        elif self.unique == True:
            print("User already added")
        else:
            print("User credentials incorrect")
    
    
    def subselect(self):
        self.settings = []
        self.master.destroy()
        self.master = tk.Tk()
        print(self.clicked)
        self.app = choosesubs(self.master,self.clicked,self.sets)
        self.master.mainloop()
    

class choosesubs():
    def __init__(self, master,user,sets):
        self.master = master
        self.wblist = ['Blacklist','Whitelist']
        self.subreddits = cleareddit.subfind(user.get(),sets[5].get(),sets[6].get())
        print(self.subreddits)
        self.listlab = tk.Label(self.master, text = self.wblist[sets[7].get()], font = ("Times", 14))
        self.listlab.grid(row=0,padx=5,pady=5)

        self.sublistb = tk.Listbox(self.master, selectmode = "multiple")
        self.sublistb.grid(row=1,padx=5)
        for subreddit in self.subreddits:
            print(subreddit)
            self.sublistb.insert(tk.END,subreddit)
        self.clearbut = tk.Button(self.master, text = "Clear")
        self.clearbut.grid(row = 2,padx=5,pady=5,sticky="nsew")

def main():
    root = tk.Tk()
    app = login(root)
    root.mainloop()

if __name__ == '__main__':
    main()