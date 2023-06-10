import tkinter as tk
from tkinter import *
import datetime
from functools import partial

import requests
import pandas as pd
import numpy as np
import sys
import os
import tkinter.ttk
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
te=TransactionEncoder()

dff=pd.read_csv("./database.csv")
ind=110
det_ind=200
arrec=[]
mycolor = '#%02x%02x%02x' % (50, 50, 50)
added_count=0
newent_count=0   
twilio_account_id="API Key"    

tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutocompleteEntry(tk.Entry):
        """
        Subclass of tk.Entry that features autocompletion.

        To enable autocompletion use set_completion_list(list) to define
        a list of possible strings to hit.
        To cycle through hits use down and up arrow keys.
        """
        def set_completion_list(self, completion_list):
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)

        def autocomplete(self, delta=0):
                """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tk.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()):  # Match case-insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tk.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tk.END)
                entry1.delete(0,tk.END)
                entry1.insert(0,self.get())

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tk.INSERT), tk.END)
                        self.position = self.index(tk.END)
                if event.keysym == "Left":
                        if self.position < self.index(tk.END): # delete the selection
                                self.delete(self.position, tk.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tk.END)
                if event.keysym == "Right":
                        self.position = self.index(tk.END) # go to end (no selection)
                if event.keysym == "Down":
                        self.autocomplete(1) # cycle to next hit
                if event.keysym == "Up":
                        self.autocomplete(-1) # cycle to previous hit
                if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
                        self.autocomplete()


overall_user=dff.iloc[:,0]
overall_user=np.array(overall_user)
overall_user=list(overall_user)
overall_phone=dff.iloc[:,1]
overall_phone=np.array(overall_phone)
overall_phone=list(overall_phone)
overall_date=dff.iloc[:,2]
overall_date=np.array(overall_date)
overall_date=list(overall_date)
overall_time=dff.iloc[:,3]
overall_time=np.array(overall_time)
overall_time=list(overall_time)
overall_name=dff.iloc[:,4]
overall_name=np.array(overall_name)
overall_name=list(overall_name)
overall_price=dff.iloc[:,5]
overall_price=np.array(overall_price)
overall_price=list(overall_price)
overall_quantity=dff.iloc[:,6]
overall_quantity=np.array(overall_quantity)
overall_quantity=list(overall_quantity)
overall_amount=dff.iloc[:,7]
overall_amount=np.array(overall_amount)
overall_amount=list(overall_amount)
overall_cno=dff.iloc[:,8]
overall_cno=np.array(overall_cno)
overall_cno=list(overall_cno)

cno=dff["Customer No"][len(overall_cno)-1] + 1


curr_user=[]
curr_phone=[]
curr_date=[]
curr_time=[]
curr_name=[]
curr_price=[]
curr_quantity=[]
curr_amount=[]
curr_cno=[]

def print_bill():
    if os.path.isfile('print.txt'):
        os.remove('print.txt')
    with open('print.txt','a') as file:
        file.write('\t\tThank you for shopping\t\t\n')
        file.write('\t\t-----------------------\t\t\n')
        file.write(f'{curr_date[0]}\t\t\t{curr_time[0]}\n')
        file.write(f'Customer Name: {curr_user[0]}\n')
        file.write(f'Customer Phone: {curr_phone[0]}\n')
        file.write('Product\t\t\tQuantity\t\tPrice\t\t\tAmount\n')
    for i in range(len(curr_name)):
        with open('print.txt','a') as file:
            file.write(f'{curr_name[i]}\t\t\t{curr_quantity[i]}\t\t\t{curr_price[i]}\t\t\t{curr_amount[i]}\n')
    with open('print.txt','a') as file:
        file.write(f'Payable Amount:\tUSD.{sum(curr_amount)}\n')
    os.startfile("print.txt", "print")  #print bill using printer
    


window1=tk.Tk()
window1.configure(background="Light blue")
window1.title("Supermarket Recommendation System")
window1.geometry('600x600')
now = datetime.datetime.now()
date=now.strftime("%Y-%m-%d")
time=now.strftime("%H:%M:%S")

timee=tk.Label(window1,text=time, bg="Light blue", fg=mycolor)
timee.place(x=200,y=15)
datee=tk.Label(window1,text=date,bg="Light blue", fg=mycolor)
datee.place(x=300,y=15)

e11=tk.Label(window1,text="Name : ",bg="Light blue", fg=mycolor)
e11.place(x=50,y=45)
e22=tk.Label(window1,text="Phone Number : ",bg="Light blue", fg=mycolor)
e22.place(x=270,y=45)
e1=tk.Entry(window1)
e1.place(x=100,y=45)
e2=tk.Entry(window1)
e2.place(x=380,y=45)



l1=tk.Label(window1,text="Item name",bg="Light blue", fg=mycolor)
l1.place(x=10, y=80)
l2=tk.Label(window1,text="Price",bg="Light blue", fg=mycolor)
l2.place(x=110, y=80)
l3=tk.Label(window1,text="Quantity",bg="Light blue", fg=mycolor)
l3.place(x=210, y=80)
l3=tk.Label(window1,text="Amount",bg="Light blue", fg=mycolor)
l3.place(x=310, y=80)


def store() :
    global added_count
    added_count=added_count+1
    global e1,e2
    usern=e1.get()
    phno=e2.get()
    x=entry1.get()
    y=entry2.get()
    z=entry3.get()
    y=int(y)
    z=int(z)
    w=z*y
    l4=tk.Label(window1,text=(str(w)+"USD."),bg="Light blue", fg=mycolor)
    l4.place(x=310,y=ind)
    l5=tk.Label(window1,text="Added.",bg="Light blue", fg=mycolor)
    l5.place(x=410,y=ind)
    curr_user.append(usern)
    curr_phone.append(phno)
    curr_date.append(date)
    curr_time.append(time)
    curr_name.append(x)
    curr_price.append(y)
    curr_quantity.append(z)
    curr_amount.append(w)
    curr_cno.append(cno)
    

def newent() :
    global newent_count
    newent_count=newent_count+1
    if(newent_count!=added_count+1 and newent_count!=0):
        store()
    global ind
    ind=ind+20
    global entry1,entry2,entry3
    entry1=tk.Entry(window1)
    entry1.place(x=10,y=ind)
    entry = AutocompleteEntry(entry1)
    test_list=list(set(pd.read_csv("./database.csv")['Name']))
    if(np.nan in test_list):
            test_list.remove(np.nan)
    entry.set_completion_list(test_list)
    entry.pack()
    entry.focus_set()
    entry2=tk.Entry(window1)
    entry2.place(x=110,y=ind)
    entry3=tk.Entry(window1)
    entry3.place(x=210,y=ind)
    button1=tk.Button(window1,text="Add",command=store,fg="White", bg=mycolor)
    button1.place(x=400,y=430)

    
button1=tk.Button(window1,text="New item",command=newent, fg="White", bg=mycolor)
button1.place(x=400,y=400)

'''Below function requires changes for different users'''
def send_text() :
    text="Thank you for shopping with us! Here's your bill: "
    for i in range(len(curr_name)):
        text+=str(curr_name[i])+" - USD."+str(curr_amount[i])+"\n"
    
    total_amount=0
    for k in curr_amount :
        total_amount=total_amount+k
    text+="Total: "+str(total_amount)
    
    from twilio.rest import Client
    
    '''Create Twilio Account to get account_sid and auth_token'''
    
    account_sid = 'Account_sid' 
    auth_token = 'Acc_Token'
    client = Client(account_sid, auth_token)
    
    '''from_ = 'whatsapp:+the number assigned by twilio','''
    
    message = client.messages.create(
            from_='whatsapp:+000000000',
            body=text,
            to='whatsapp:+91'+curr_phone[0]
            )
    print(message.sid)

def subm() :
    global ind
    overall_user.extend(curr_user)
    overall_phone.extend(curr_phone)
    overall_date.extend(curr_date)
    overall_time.extend(curr_time)
    overall_name.extend(curr_name)
    overall_price.extend(curr_price)
    overall_quantity.extend(curr_quantity)
    overall_amount.extend(curr_amount)
    overall_cno.extend(curr_cno)
    df=pd.DataFrame({"UserName":overall_user,"Phone":overall_phone,"Date":overall_date,"Time":overall_time,"Name":overall_name,"Price":overall_price,"Quantity":overall_quantity,"Amount":overall_amount,"Customer No" : overall_cno })
    df.to_csv("./database.csv",index=False)
    ans=0
    for k in curr_amount :
        ans=ans+k
    op=tk.Label(window1,text="Submission successful. Thank you for shopping! Click below button to print bill",bg="Light blue", fg=mycolor)
    op.place(x=50,y=ind+50)
    op1=tk.Label(window1,text=("Total amount : "+ str(ans) + "USD."),bg="Light blue", fg=mycolor)
    op1.place(x=50,y=ind+80)
    button1=tk.Button(window1,text="Print Bill",command=print_bill, fg="White", bg=mycolor)
    button1.place(x=0,y=400)
    send_text()
    
button3=tk.Button(window1,text="Submit",command=subm, fg="White", bg=mycolor)
button3.place(x=400,y=460)
lg=[]


def recm() :
    df_new=pd.read_csv("./database.csv")
    for i in range(cno+1) :
        lg=[]
        for z in df_new.index :
            if df_new.iloc[z][8]==i :
                lg.append(df_new.iloc[z][4])
        arrec.append(lg)
    booldata=te.fit(arrec).transform(arrec)
    dff_new=pd.DataFrame(booldata,columns=te.columns_)
    freq_items=apriori(dff_new,min_support=0.05,use_colnames=True)
    freq_items['Length']=freq_items['itemsets'].apply(lambda x: len(x))
    
    recc=freq_items[(freq_items['Length']>=2) & (freq_items['support']>=0.02)]

    op=(recc.iloc[:,1].to_string(index=False)).split('\n')
    window_rec=tk.Tk()
    window_rec.title("Recommendations")
    window_rec.configure(background=mycolor)
    window_rec.geometry('300x300')
    for zz in op :
        l1=tk.Label(window_rec,text=zz,fg="White", bg=mycolor)
        l1.pack()
    

button4=tk.Button(window1,text="Recommend",command=recm,fg="White", bg=mycolor)
button4.place(x=400,y=490)
f=0


def det() :
    
    w11=tk.Tk()
    w11.title("Find Details")
    w11.configure(background=mycolor)
    w11.geometry('600x600')
    l12=tk.Label(w11,text="Username",fg="White", bg=mycolor)
    l12.place(x=100,y=50)
    e12=tk.Entry(w11)
    e12.place(x=160,y=50)
    l22=tk.Label(w11,text="Phone",fg="White", bg=mycolor)
    l22.place(x=100,y=80)
    e22=tk.Entry(w11)
    e22.place(x=160,y=80)
    
    
    def det2() :
        df_d=pd.read_csv("./database.csv")
        global det_ind
        zzz=e12.get()
        yyy=e22.get()
        laa1=tk.Label(w11,text="Date",fg="White", bg=mycolor)
        laa2=tk.Label(w11,text="Time",fg="White", bg=mycolor)
        laa3=tk.Label(w11,text="Product",fg="White", bg=mycolor)
        laa4=tk.Label(w11,text="Price",fg="White", bg=mycolor)
        laa5=tk.Label(w11,text="Quantity",fg="White", bg=mycolor)
        laa6=tk.Label(w11,text="Amount",fg="White", bg=mycolor)
        laa1.place(x=30,y=160)
        laa2.place(x=100,y=160)
        laa3.place(x=170,y=160)
        laa4.place(x=240,y=160)
        laa5.place(x=310,y=160)
        laa6.place(x=380,y=160)
        global f
        for j in df_d.index :
            if (df_d.iloc[j][0]==zzz) & (df_d.iloc[j][1]==int(yyy)) :
                f=1
                la1=tk.Label(w11,text=df_d.iloc[j][2],fg="White", bg=mycolor)
                la2=tk.Label(w11,text=df_d.iloc[j][3],fg="White", bg=mycolor)
                la3=tk.Label(w11,text=df_d.iloc[j][4],fg="White", bg=mycolor)
                la4=tk.Label(w11,text=df_d.iloc[j][5],fg="White", bg=mycolor)
                la5=tk.Label(w11,text=df_d.iloc[j][6],fg="White", bg=mycolor)
                la6=tk.Label(w11,text=df_d.iloc[j][7],fg="White", bg=mycolor)
                la1.place(x=30,y=det_ind)
                la2.place(x=100,y=det_ind)
                la3.place(x=170,y=det_ind)
                la4.place(x=240,y=det_ind)
                la5.place(x=310,y=det_ind)
                la6.place(x=380,y=det_ind)
                det_ind=det_ind+30

        if f==0 :
            la7=tk.Label(w11,text="Not Found!",bg="White", fg=mycolor)
            la7.place(x=170,y=400)
               
    button6=tk.Button(w11,text="Submit",command=det2,fg="White", bg=mycolor)
    button6.place(x=170,y=115)

    
button5=tk.Button(window1,text="Find Customer Details",command=det,fg="White", bg=mycolor)
button5.place(x=400,y=520)
    
window1.mainloop()