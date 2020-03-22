# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
from pathlib import Path
import pint
from pint import UnitRegistry
ureg = UnitRegistry()

vareni=Tk()
vareni.option_add('*Font', 'Arial 10')

PocetRadku = 1
Init_done= 0

#plonkova definice
Item = []
Value = []
Var = []
Unit = []
Item_new = []
Value_new = []
Var_new = []
Unit_new = []
Polozky = []
Unit_before = []
Real_Value = []
Pocet1_DATA = StringVar()

#naplneni pole
for i in range(PocetRadku):
    Item.append("0")
    Value.append("0")
    Var.append("0")
    Unit.append("0")
    Item_new.append("0")
    Value_new.append("0")
    Var_new.append("0")
    Unit_new.append("0")
    Polozky.append("0")
    Unit_before.append("0")
    Real_Value.append("0")

#cteni druhu suroviny
def Read():
    lineList = [line.rstrip('\n') for line in open(r'resources\units_mass.txt')]
    return lineList

#nastaveni grafiky
def Inicializace():
    #pocet osob
    Stitek=Label(text=u"Počet strávníků")
    Stitek.grid(row=0,column=0)
    Pocet1=Entry(width="4")
    Pocet1.insert(END,str(1))
    Pocet1.grid(row=0, column=1,sticky=W)

    #novy pocet osob
    Pocet1_new=Entry(width="4")
    Pocet1_new.grid(row=0,column=2,sticky=E)
    Pocet1_new.insert(END,str(2))

    #tlacitko tisk
    button1=Button(text=u"Tisk hodnot")
    button1.grid(row=10, column=3)

    #tlacitko prepocet osob
    button2=Button(text=u"Prepočet strávníci")
    button2.grid(row=11, column=3)
    button2.bind("<Button-1>", lambda udalost: PrepocetOsoby(udalost,Pocet1,Pocet1_new,Value))

    #Frame na oddeleni horizontalni
    Frame(height=2, bd=1, relief=SUNKEN,width=380).grid(row=1,columnspan=5, padx=5, pady=5,sticky=W)

    #hlavicka - název
    Stitek1=Label(text=u"surovina")
    Stitek1.grid(row=2,column=0)
    #hlavicka - hodnota
    Stitek1=Label(text=u"hodnota")
    Stitek1.grid(row=2,column=1)
    #hlavicka - jednotka
    Stitek1=Label(text=u"jednotka")
    Stitek1.grid(row=2,column=2)

    #cyklus na radky
    for i in range(PocetRadku):
        #surovina1
        Item[i]=Entry()
        Item[i].insert(END,'Mleko')
        Item[i].grid(row=3+i,column=0)
        #hodnota1
        Real_Value[i]=StringVar()
        Real_Value[i].trace("w",ZmenaHodnota)
        Value[i]=Entry(vareni,textvariable=Real_Value[i])
        Value[i].insert(END,0)
        Value[i].grid(row=3+i,column=1)

        #unit1
        MyItems=Read() #nacte hodnoty ze souboru
        Var[i] = StringVar(vareni)
        Var[i].set(MyItems[0]) # defaultni hodnota
        Var[i].trace("w", ZmenaJednotka)
        Unit[i]=OptionMenu(vareni, Var[i], *MyItems)
        Unit[i].grid(row=3+i,column=2)
        #Unit[i].bind("<Enter>", lambda udalost: Save(udalost,Var[i].get(),Value[i].get()))
        Save(Var[i].get(),Value[i].get())

    #inicializace dokoncena
    Init_done = 1
#prepocet stravnici
def PrepocetOsoby(udalost,Pocet1,Pocet1_new,Value):

    #hlavicka - název
    Stitek1=Label(text=u"surovina")
    Stitek1.grid(row=2,column=4)
    #hlavicka - hodnota
    Stitek1=Label(text=u"hodnota")
    Stitek1.grid(row=2,column=5)
    #hlavicka - jednotka
    Stitek1=Label(text=u"jednotka")
    Stitek1.grid(row=2,column=6)

    #Prepocet
    Z=int(Pocet1_new.get())/int(Pocet1.get())

    #cyklus na radky
    for i in range(PocetRadku):
        #surovina1{}
        Item_new[i]=Entry()
        Item_new[i].grid(row=3+i,column=4)
        Item_new[i].insert(END,Item[i].get())
        #hodnota1
        Value_new[i]=Entry()
        Value_new[i].grid(row=3+i,column=5)
        Value_new[i].insert(END,float(Real_Value[i].get())*Z)
        #unit1
        MyItems=Read() #nacte hodnoty ze souboru
        Var_new[i] = StringVar(vareni)
        Var_new[i].set(Var[i]) # defaultni hodnota
        Unit_new[i]=OptionMenu(vareni, Var[i], *MyItems)
        Unit_new[i].grid(row=3+i,column=6)

#prevod jednotky
def Prevod(NewUnit,Var):
    #cyklus na radky
    for i in range(PocetRadku):
        print('converting...')
        print(Var)
        c= Var.to(NewUnit)
        print('A conversion complete')
        print(c)
        d=round(c.magnitude,5)
        print(d)
        Value[i].delete(0,END)
        Value[i].insert(END,d)

#ulozeni jednotky
def Save(Unit,Value):
    #cyklus na radky
    for i in range(PocetRadku):
        print('Ukladam...')
        Unit_before[i] = float(Value) * ureg(Unit)
        print(Unit_before[i])

#zmenila se jednotka
def ZmenaJednotka(*args):
    print('probiha zmena jednotky')
    Prevod(Var[i].get(),Unit_before[i])

#zmenila se hodnota
def ZmenaHodnota(*args):
    Save(Var[i].get(),Real_Value[i].get())

# ------------------------------------------------------------
# -----------------Hlavni smycka -----------------------------
# ------------------------------------------------------------

Inicializace()

#obrazky (z nejakeho duvodu nelze v inicializaci)
obrazek=PhotoImage(file=r"obr\book2_crop.png")
image = Label(image=obrazek)
image.grid(row=1, column=3,rowspan=9)

obrazek1=PhotoImage(file=r"obr\arrow_crop.png")
image1 = Label(image=obrazek1,bg="grey")
image1.grid(row=0, column=1,columnspan=2)

# vypsani vsech jednotek z metrickeho systemu
#z=dir(ureg.sys.mks)
#print(z)

vareni.mainloop()
