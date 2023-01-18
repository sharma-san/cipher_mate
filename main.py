import random
import tkinter as tk
import customtkinter as ctk

#initialization for key
master=[]
seed=['A','a','0','@']
for i in range(0,24):
  temp1=seed.copy()
  temp2=[]
  temp2.append(temp1[i//6])
  temp1.pop(i//6)
  temp2.append(temp1[(i%6)//2])
  temp1.pop((i%6)//2)
  temp2.append(temp1[(i%6)%2])
  temp1.pop((i%6)%2)
  temp2+=temp1
  master.append(temp2)

def to95(x):
  if x>=1 and x<=95:
    return x
  elif x>95:
    if x<1000:
      return to95(x-95)
    else:
      return (x%96+1)
  else:
    if x>-1000:
      return to95(x+95)
    else:
      return (-x)%96+1

def facList(x):
  listFac=[]
  for i in range(1,x+1):
    if x%i==0:
      listFac.append(i)
  return listFac

def ranFact(x):
  factRan=[]
  for i in range(0,3):
    r=(random.choice(facList(x)))
    factRan.append(r)
    x//=r
  factRan.append(x)
  return factRan
  
class Key:
  def __init__(self, key_list):
    self.dict={}
    count = 1
    for i in key_list:
      if i=="A":
        for j in range(0,26):
          self.dict[count]=chr(65+j)
          count+=1

      elif i=="a":
        for j in range(0,26):
          self.dict[count]=chr(97+j)
          count+=1

      elif i=="0":
        for j in range(0,10):
          self.dict[count]=chr(48+j)
          count+=1

      else:
        for j in range(0,16):
          self.dict[count]=chr(32+j)
          count+=1
        for j in range(0,7):
          self.dict[count]=chr(58+j)
          count+=1
        for j in range(0,6):
          self.dict[count]=chr(91+j)
          count+=1
        for j in range(0,4):
          self.dict[count]=chr(123+j)
          count+=1

  def printKey(self):
    pListT=list(self.dict.items())
    pListF=sorted(pListT, key=lambda a: a[0])
    for i in pListF:
      print(i[0],"\t:\t", i[1])

  def shift(self, pin):
    for i in list(self.dict.items()):
      if i[1]=="A":
        n1=i[0]
      elif i[1]=="a":
        n2=i[0]
      if i[1]=="0":
        n3=i[0]
      if i[1]==" ":
        n4=i[0]

    sKey1={}
    for i in range(0,26-pin[0]):
      sKey1[n1+pin[0]+i]=self.dict[n1+i]
    for i in range(0,pin[0]):
      sKey1[n1+i]=self.dict[n1+26-pin[0]+i]

    sKey2={}
    for i in range(0,26-pin[1]):
      sKey2[n2+pin[1]+i]=self.dict[n2+i]
    for i in range(0,pin[1]):
      sKey2[n2+i]=self.dict[n2+26-pin[1]+i]

    sKey3={}
    for i in range(0,10-pin[2]):
      sKey3[n3+pin[2]+i]=self.dict[n3+i]
    for i in range(0,pin[2]):
      sKey3[n3+i]=self.dict[n3+10-pin[2]+i]

    sKey4={}
    for i in range(0,33-pin[3]):
      sKey4[n4+pin[3]+i]=self.dict[n4+i]
    for i in range(0,pin[3]):
      sKey4[n4+i]=self.dict[n4+33-pin[3]+i]

    self.dict.update(sKey1)
    self.dict.update(sKey2)
    self.dict.update(sKey3)
    self.dict.update(sKey4)
  
  def encode(self, m_str):
    c_list=[]
    for i in m_str:
      for j in list(self.dict.items()):
        if i==j[1]:
          c_list.append(j[0])
          break
    return c_list
  
  def decode(self, c_list):
    m_str=""
    for i in c_list:
      m_str+=self.dict[i]
    return m_str

def cipher(message, k1=1, k2=1, k3=1, k4=1, pinn="0000", passw="password"):
  global master
  pin=[]
  for i in pinn:
    pin.append(int(i))
  keyOne=Key(master[k1-1])
  keyOne.shift(pin)
  keyTwo=Key(master[k2-1])
  keyTwo.shift(pin)
  keyThree=Key(master[k3-1])
  keyThree.shift(pin)
  keyFour=Key(master[k4-1])
  keyFour.shift(pin)
  c_list=keyOne.encode(message)
  pList=keyOne.encode(passw)
  c2List=[]
  if len(pList)!=0:
    for i in range(0, len(c_list)):
      c2List.append(to95(c_list[i]+pList[i%len(pList)]))
  else:
    c2List=c_list.copy()
  c3List=[]
  count=0
  for i in c2List:
    r=ranFact(i)
    for j in r:
      c3List.append(to95(j+count))
      count+=1
  code1=keyTwo.decode(c3List)
  code2=keyThree.encode(code1)
  code3=keyFour.decode(code2)
  return code3[::-1]

def decipher(code, k1=1, k2=1, k3=1, k4=1, pinn="0000", passw="password"):
  global master
  pin=[]
  for i in pinn:
    pin.append(int(i))
  keyOne=Key(master[k1-1])
  keyOne.shift(pin)
  keyTwo=Key(master[k2-1])
  keyTwo.shift(pin)
  keyThree=Key(master[k3-1])
  keyThree.shift(pin)
  keyFour=Key(master[k4-1])
  keyFour.shift(pin)
  pList=keyOne.encode(passw)
  code2=keyFour.encode(code[::-1])
  code3=keyThree.decode(code2)
  cList=keyTwo.encode(code3)
  count=0
  c2List=[]
  for i in cList:
    c2List.append(to95(i-count))
    count+=1
  c3List=[]
  for i in range(0,len(c2List)//4):
    c3List.append(c2List[4*i]*c2List[4*i+1]*c2List[4*i+2]*c2List[4*i+3])
  mList=[]
  if len(pList)!=0:
    for i in range(0, len(c3List)):
      mList.append(to95(c3List[i]-pList[i%len(pList)]))
  else:
    mList=c3List.copy()
  return keyOne.decode(mList)

def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list
  
root = ctk.CTk()
root.title("C A S K")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()-90))
root.configure(fg_color="black")
ctk.set_appearance_mode("dark")

def welc():
  global root
  widget_list = all_children(root)
  for item in widget_list:
      item.pack_forget()
  widget_list = all_children(root)
  for item in widget_list:
      item.grid_forget()
  titleLabel = ctk.CTkLabel(master=root,width=root.winfo_screenwidth()-20,height=root.winfo_screenheight()//3-60,corner_radius=10, fg_color="gray25", font=("Times",70), text="\u20A1\t\u20B3\t\u0586\t\u20AD", text_color="orangered")
  titleLabel.pack(pady=10)
  mainLabel = ctk.CTkLabel(master=root,width=root.winfo_screenwidth()-20,height=root.winfo_screenheight()//3-150,corner_radius=10, fg_color="gray25", font=("Times",30), text="\u20A1ipher\t\t\u20B3lgorithm\t\u1D42\u1D35\u1D40\u1D34\t\u0586hifted\t\t\u20ADey",text_color="darkorange")
  mainLabel.pack()
  buttonCipher = ctk.CTkButton(master=root,width=root.winfo_screenwidth()//4-20,height=root.winfo_screenheight()//8, fg_color="gray25", text="CIPHER",font=("Times",30), border_width=10, border_color="lawngreen", text_color="lawngreen", command=winCipher)
  buttonCipher.pack(pady=10)
  buttonDecipher = ctk.CTkButton(master=root,width=root.winfo_screenwidth()//4-20,height=root.winfo_screenheight()//8, fg_color="gray25", text="DECIPHER",font=("Times",30), border_width=10, border_color="cyan",text_color="cyan", command=winDecipher)
  buttonDecipher.pack(pady=10)
  buttonExit = ctk.CTkButton(master=root,width=root.winfo_screenwidth()//4-20,height=root.winfo_screenheight()//8, fg_color="gray25", text="Exit",font=("Times",30), border_width=10, border_color="red",text_color="red", command=root.destroy)
  buttonExit.pack(pady=10)

  root.mainloop()

def winCipher():
  global root
  global keyMenu1
  global keyMenu2
  global keyMenu3
  global keyMenu4
  global pinMenu1
  global pinMenu2
  global pinMenu3
  global pinMenu4
  global passEntry
  global mText
  global outText  
  
  keyOpt=[]
  for i in range(1,25):
    keyOpt.append("Key {}".format(i))
  pinOpt=[]
  for i in range(0,10):
    pinOpt.append(str(i))
  
  widget_list = all_children(root)
  for item in widget_list:
      item.pack_forget()
  root.columnconfigure(8)
  root.rowconfigure(20)
  backButton = ctk.CTkButton(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, fg_color="gray25", text="\u2770"+"  Back", font=("Times", 20), border_width=5, border_color="cyan", text_color="cyan", command=welc)
  backButton.grid(row=0,column=0, rowspan=1, columnspan=2)
  
  keyLabel = ctk.CTkLabel(master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()//20, fg_color="gray25", text="Select four keys in order:", font=("Times", 20), text_color="yellow")
  keyLabel.grid(row=1, column=0, rowspan=1, columnspan=8)
  keyMenu1 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu1.grid(row=2, column=0, rowspan=1, columnspan=2)
  keyMenu2 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu2.grid(row=2, column=2, rowspan=1, columnspan=2)
  keyMenu3 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu3.grid(row=2, column=4, rowspan=1, columnspan=2)
  keyMenu4 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu4.grid(row=2, column=6, rowspan=1, columnspan=2)
  
  pinLabel = ctk.CTkLabel(master=root, width=root.winfo_screenwidth()//2, height=root.winfo_screenheight()//20, fg_color="gray25", text="Enter four digit PIN:", font=("Times", 20), text_color="lawngreen")
  pinLabel.grid(row=3, column=0, rowspan=1, columnspan=4)
  pinMenu1 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu1.grid(row=3, column=4, rowspan=1, columnspan=1)
  pinMenu2 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu2.grid(row=3, column=5, rowspan=1, columnspan=1)
  pinLabel.grid(row=3, column=0, rowspan=1, columnspan=4)
  pinMenu3 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu3.grid(row=3, column=6, rowspan=1, columnspan=1)
  pinLabel.grid(row=3, column=0, rowspan=1, columnspan=4)
  pinMenu4 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu4.grid(row=3, column=7, rowspan=1, columnspan=1)

  
  passEntry = ctk.CTkEntry(master=root, width=root.winfo_screenwidth()//2, height=root.winfo_screenheight()//20, fg_color="grey25", font=("Times", 20), text_color="deeppink", placeholder_text="Enter Password(0-25 Characters, excess will be truncated)....", placeholder_text_color="grey70")
  passEntry.grid(row=4, column=0, rowspan=1, columnspan=4)

  mLabel = ctk.CTkLabel(master=root, width=root.winfo_screenwidth()//2, height=root.winfo_screenheight()//20, fg_color="grey25", font=("Times", 20), text_color="darkorange", text="Enter text to be encoded below:")
  mLabel.grid(row=4, column=4, rowspan=1, columnspan=4)
  mText = ctk.CTkTextbox(master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()//3-90, fg_color="grey25", font=("Times", 20), text_color="darkorange", border_width=5, border_color="darkorange")
  mText.grid(row=5, column=0, rowspan=7, columnspan=8)

  def guiEncode():
    global keyMenu1
    global keyMenu2
    global keyMenu3
    global keyMenu4
    global pinMenu1
    global pinMenu2
    global pinMenu3
    global pinMenu4
    global passEntry
    global mText
    global outText
    k1 = keyMenu1.get()
    k2 = keyMenu2.get()
    k3 = keyMenu3.get()
    k4 = keyMenu4.get()
    K1 = int(k1[4::])
    K2 = int(k2[4::])
    K3 = int(k3[4::])
    K4 = int(k4[4::])
    pinng=""
    for i in [pinMenu1, pinMenu2, pinMenu3, pinMenu4]:
      pinng+=i.get()

    pwStr=passEntry.get()[0:26]

    mStr=mText.get('1.0', tk.END)
    try:
      cde=cipher(mStr, K1, K2, K3, K4, pinng, pwStr)
    except:
      cde="~~~Incorrect Key~~~"
    outText.configure(state="normal")
    outText.delete('1.0 linestart', tk.END)
    outText.insert('1.0', text=cde)
    outText.configure(text_color="darkgoldenrod1")
    outText.configure(state="disabled")
  
  cButton = ctk.CTkButton(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, fg_color="gray25", text="\u21A3 Encode \u21A2", font=("Times", 20), border_width=5, border_color="snow", text_color="snow", command=guiEncode)
  cButton.grid(row=12, column=0, rowspan=1, columnspan=8)

  outText = ctk.CTkTextbox(master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()//3, fg_color="grey25", font=("Times", 20), text_color="grey70", border_width=5, border_color="darkgoldenrod1")
  outText.grid(row=13, column=0, columnspan=8, rowspan=7)
  outText.insert('1.0', text="Your code will appear here...")
  outText.configure(state="disabled")
  
  root.mainloop()
  

def winDecipher():
  global root
  global keyMenu1
  global keyMenu2
  global keyMenu3
  global keyMenu4
  global pinMenu1
  global pinMenu2
  global pinMenu3
  global pinMenu4
  global passEntry
  global mText
  global outText  
  
  keyOpt=[]
  for i in range(1,25):
    keyOpt.append("Key {}".format(i))
  pinOpt=[]
  for i in range(0,10):
    pinOpt.append(str(i))
  widget_list = all_children(root)
  for item in widget_list:
      item.pack_forget()
  root.columnconfigure(8)
  root.rowconfigure(20)
  backButton = ctk.CTkButton(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, fg_color="gray25", text="\u2770"+"  Back", font=("Times", 20), border_width=5, border_color="cyan", text_color="cyan", command=welc)
  backButton.grid(row=0,column=0, rowspan=1, columnspan=2)
  
  keyLabel = ctk.CTkLabel(master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()//20, fg_color="gray25", text="Select four keys in order:", font=("Times", 20), text_color="yellow")
  keyLabel.grid(row=1, column=0, rowspan=1, columnspan=8)
  keyMenu1 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu1.grid(row=2, column=0, rowspan=1, columnspan=2)
  keyMenu2 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu2.grid(row=2, column=2, rowspan=1, columnspan=2)
  keyMenu3 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu3.grid(row=2, column=4, rowspan=1, columnspan=2)
  keyMenu4 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, values=keyOpt, fg_color="grey25", text_color="yellow", font=("Times", 20), dropdown_text_color="yellow")
  keyMenu4.grid(row=2, column=6, rowspan=1, columnspan=2)
  
  pinLabel = ctk.CTkLabel(master=root, width=root.winfo_screenwidth()//2, height=root.winfo_screenheight()//20, fg_color="gray25", text="Enter four digit PIN:", font=("Times", 20), text_color="lawngreen")
  pinLabel.grid(row=3, column=0, rowspan=1, columnspan=4)
  pinMenu1 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu1.grid(row=3, column=4, rowspan=1, columnspan=1)
  pinLabel.grid(row=3, column=0, rowspan=1, columnspan=4)
  pinMenu2 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu2.grid(row=3, column=5, rowspan=1, columnspan=1)
  pinLabel.grid(row=3, column=0, rowspan=1, columnspan=4)
  pinMenu3 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu3.grid(row=3, column=6, rowspan=1, columnspan=1)
  pinLabel.grid(row=3, column=0, rowspan=1, columnspan=4)
  pinMenu4 = ctk.CTkOptionMenu(master=root, width=root.winfo_screenwidth()//8, height=root.winfo_screenheight()//20, values=pinOpt, fg_color="grey25", text_color="lawngreen", font=("Times", 20), dropdown_text_color="lawngreen")
  pinMenu4.grid(row=3, column=7, rowspan=1, columnspan=1)

  
  passEntry = ctk.CTkEntry(master=root, width=root.winfo_screenwidth()//2, height=root.winfo_screenheight()//20, fg_color="grey25", font=("Times", 20), text_color="deeppink", placeholder_text="Enter Password(0-25 Characters, excess will be truncated)....", placeholder_text_color="grey70")
  passEntry.grid(row=4, column=0, rowspan=1, columnspan=4)

  mLabel = ctk.CTkLabel(master=root, width=root.winfo_screenwidth()//2, height=root.winfo_screenheight()//20, fg_color="grey25", font=("Times", 20), text_color="darkorange", text="Enter code to be decoded below:")
  mLabel.grid(row=4, column=4, rowspan=1, columnspan=4)
  mText = ctk.CTkTextbox(master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()//3, fg_color="grey25", font=("Times", 20), text_color="darkorange", border_width=5, border_color="darkorange")
  mText.grid(row=5, column=0, rowspan=7, columnspan=8)

  def guiDecode():
    global keyMenu1
    global keyMenu2
    global keyMenu3
    global keyMenu4
    global pinMenu1
    global pinMenu2
    global pinMenu3
    global pinMenu4
    global passEntry
    global mText
    global outText
    k1 = keyMenu1.get()
    k2 = keyMenu2.get()
    k3 = keyMenu3.get()
    k4 = keyMenu4.get()
    K1 = int(k1[4::])
    K2 = int(k2[4::])
    K3 = int(k3[4::])
    K4 = int(k4[4::])
    pinng=""
    for i in [pinMenu1, pinMenu2, pinMenu3, pinMenu4]:
      pinng+=i.get()

    pwStr=passEntry.get()[0:26]

    mStr=mText.get('1.0', tk.END)

    try:
      cde=decipher(mStr, K1, K2, K3, K4, pinng, pwStr)
    except:
      cde="~~~Incorrect Key~~~"
    outText.configure(state="normal")
    outText.delete('1.0 linestart', tk.END)
    outText.insert('1.0', text=cde)
    outText.configure(text_color="darkgoldenrod1")
    outText.configure(state="disabled")
  
  cButton = ctk.CTkButton(master=root, width=root.winfo_screenwidth()//4, height=root.winfo_screenheight()//20, fg_color="gray25", text="\u21A2 Decode \u21A3", font=("Times", 20), border_width=5, border_color="snow", text_color="snow", command=guiDecode)
  cButton.grid(row=12, column=0, rowspan=1, columnspan=8)

  outText = ctk.CTkTextbox(master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()//3-90, fg_color="grey25", font=("Times", 20), text_color="grey70", border_width=5, border_color="darkgoldenrod1")
  outText.grid(row=13, column=0, columnspan=8, rowspan=7)
  outText.insert('1.0', text="Your message will appear here...")
  outText.configure(state="disabled")
  
  root.mainloop()
  

welc()