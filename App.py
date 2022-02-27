# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import sqlite3

class App:
	def __init__(self, projet):
		App.projet = projet
		App.window = Tk()
		App.window.title(projet)
		App.window.minsize(500, 400)
		App.window.geometry('500x400+710+200')
		h1 = Label(App.window, text=self.projet, style='H1.Label').pack()
		lg = Login(App.window)
		App.style()
		App.window.configure(background='#fff')
		App.window.mainloop()

	def open(container):
		container.pack()
	
	def getPage(page, i=0, idp=-1):
		if i == 1:
			Projet.h2.destroy()
			Projet.menu.destroy()
			Projet.container.destroy()
			if idp == -1:
				pg = page(App.window)
			else:
				pg = page(App.window, idp)	
		elif i == 0:
			App.window.destroy()
			app = App('Trillo')	
			
	def style():
		style = Style();
		style.configure('H1.Label', font =('Verdana', 65, 'bold'), foreground='#243454', background='#fff')
		style.configure('H2.Label', font =('Verdana', 20), foreground='#243454', background='#fff')	
		style.configure('H3.Label', font =('Verdana', 15, 'bold'), foreground='#243454', background='#fff')	
		style.configure('TFrame', font =('Verdana', 20), foreground='#243454', background='#fff')	
		style.configure('P.TButton', font =('calibri', 15), background='#fff')	
		style.configure('D.TButton', font=('calibri', 10, 'bold'),foreground='red')
		style.configure('Btn.Button', font = ('verdana', 18, 'bold'), foreground='#666666', background='#fff')	

class Login:

	def __init__(self, master):
		password = StringVar()
		Login.container = PanedWindow(master, orient=HORIZONTAL)
		panel = Frame(Login.container, style='TFrame')
		h2 = Label(panel, text='Authentification', style='H2.Label').pack(pady=15)
		field = Entry(panel, textvariable=password, show='*', width=50).pack(ipady=5, pady=10)
		btn = Button(panel, text='CONNEXION', command=lambda: self.verifier(password)).pack(ipady=8, pady=10, ipadx=15)
		Login.container.add(panel)
		App.open(Login.container)
	
	def verifier(self, password):
		password = password.get()
		if password == '123':
			Login.container.destroy()
			Login.container.quit()
			App.window.minsize(1300, 800)
			App.window.geometry('1200x760+300+100')
			pjs = Projets(App.window)
			App.window.mainloop()
		else:
			messagebox.showwarning('ERREUR', 'Mot de passe incorrect !')

class Projets:

	def __init__(self, master):
		Projets.h2 = Label(master, text='Liste de projets', style='H2.Label', anchor='w')
		Projets.h2.pack(pady=15)
		Projets.container = PanedWindow(master, orient=HORIZONTAL)
		self.panel = Frame(Projets.container, style='TFrame')
		btn = Button(self.panel, text='Nouveau projet', style='P.TButton', command=self.modal)
		btn.grid(column=0, row=0, ipadx=15, padx=5, ipady=6, pady=10)
		projets = self.getDataProjets()
		for projet in projets:
			self.getProjets(projet[0], projet[1])
		Projets.container.add(self.panel)
		App.open(Projets.container)	

	def modal(self):
		self.Ii = Toplevel()
		self.Ii.title(App.projet)
		self.Ii.minsize(350, 150)
		self.Ii.maxsize(350, 150)
		self.Ii.geometry("350x150+770+400")
		self.Ii.configure(background='#fff')
		self.field = StringVar()
		Label(self.Ii, text='Créer un nouveau projet', style='H3.Label').pack(pady=5)
		Entry(self.Ii, textvariable=self.field, width=40).pack(ipady=5, padx=5, pady=5)
		Button(self.Ii, text='AJOUTER', style='Btn.TButton', command=self.addProjet).pack(ipady=5, ipadx=3, pady=5)
		self.Ii.transient()
		self.Ii.grab_set() #empeche toute interaction avec la fenetre principale
		App.window.wait_window(self.Ii)

	def addProjet(self):
		field = self.field.get()
		field = (field, )
		connexion = sqlite3.connect('database.db')
		curseur = connexion.cursor()
		curseur.execute("INSERT INTO projets (nom) VALUES (?)", field)	
		connexion.commit()
		idp = curseur.lastrowid
		connexion.close()
		self.Ii.destroy()	
		self.getProjet(idp)

	def getProjets(self, idp, nom):
		btn = Button(self.panel, text=nom, style='P.TButton', command=lambda: self.getProjet(idp))
		btn.grid(column=idp, row=0, ipadx=15, padx=5, ipady=6, pady=10)	

	def getDataProjets(self):
		connexion = sqlite3.connect('database.db')
		curseur = connexion.cursor()
		curseur.execute("SELECT * FROM projets")
		resultats = curseur.fetchall()
		connexion.close()
		return resultats			

	def getProjet(self, idp):
		Projets.h2.destroy()
		Projets.container.destroy()
		pj = Projet(App.window, idp)

class Projet:

	def __init__(self, master, idp):
		projet = self.getDataProjet(idp)
		taches0 = self.getDataTaches(0, idp)
		taches1 = self.getDataTaches(1, idp)
		taches2 = self.getDataTaches(2, idp)
		Projet.h2 = Label(master, text='Projet | ' + projet[1], style='H2.Label', anchor='w')
		Projet.h2.pack(pady=15)
		Projet.menu = Frame(master)
		Projet.menu.pack(pady=10)
		Button(Projet.menu, text='Créer une tache', command=lambda: self.modal(idp)).grid(column=1, row=1, padx=5)
		Button(Projet.menu, text='Liste de projets', command=lambda: App.getPage(Projets, 1)).grid(column=2, row=1, padx=5)
		Button(Projet.menu, text='Deconnexion', command=lambda: App.getPage(Login, 0), style='D.TButton').grid(column=3, row=1, padx=5)
		Projet.container = PanedWindow(master, orient=HORIZONTAL)
		panel1 = Frame(Projet.container, style='TFrame')
		panel2 = Frame(Projet.container, style='TFrame')
		panel3 = Frame(Projet.container, style='TFrame')
		Label(panel1, text='A faire', style='H2.Label').grid(columnspan=2, row=0, padx=10, pady=10)
		for tache0 in taches0:
			self.getTaches(tache0[0], tache0[1], panel1, 0, 'Go>>', idp)
		Label(panel2, text='En-cours', style='H2.Label').grid(columnspan=2, row=0, padx=10, pady=10)
		for tache1 in taches1:
			self.getTaches(tache1[0], tache1[1], panel2, 1, 'Go>>', idp)
		Label(panel3, text='Terminé', style='H2.Label').grid(columnspan=2, row=0, padx=10, pady=10)
		for tache2 in taches2:
			self.getTaches(tache2[0], tache2[1], panel3, 2, '<<Go', idp)	
		Projet.container.add(panel1)
		Projet.container.add(panel2)
		Projet.container.add(panel3)
		App.open(Projet.container)

	def go(self, idp, idt, etat):
		connexion = sqlite3.connect('database.db')
		curseur = connexion.cursor()
		print(etat)
		if etat == 2:
			etat = 1
		else:
			etat = etat + 1	
		print(etat)
		e = (etat, idt, )
		curseur.execute("UPDATE taches SET etat=? WHERE id=?", e)
		connexion.commit()
		connexion.close()	
		App.getPage(Projet, 1, idp)

	def modal(self, idp):
		self.Ii = Toplevel()
		self.Ii.title('database')
		self.Ii.minsize(350, 150)
		self.Ii.maxsize(350, 150)
		self.Ii.geometry("350x150+770+400")
		self.field = StringVar()
		Label(self.Ii, text='Créer une nouvelle tache', style='Dim.TLabel').pack(pady=5)
		Entry(self.Ii, textvariable=self.field, width=40).pack(ipady=5, padx=5, pady=5)
		Button(self.Ii, text='AJOUTER', command=lambda: self.addTache(idp)).pack(ipady=5, ipadx=3, pady=5)
		self.Ii.transient()
		self.Ii.grab_set() #empeche toute interaction avec la fenetre principale
		App.window.wait_window(self.Ii)

	def addTache(self, idp):
		field = self.field.get()
		field = (field, 0, idp,)
		connexion = sqlite3.connect('database.db')
		curseur = connexion.cursor()
		curseur.execute("INSERT INTO taches (nom, etat, idp) VALUES (?,?,?)", field)	
		connexion.commit()
		connexion.close()
		self.Ii.destroy()
		App.getPage(Projet, 1, idp)

	def getTaches(self, idt, nom, panel, etat, btn, idp):
		Label(panel, text=nom, width=50).grid(column=0, row=idt, padx=5, pady=5, ipadx=5, ipady=5)
		Button(panel, text=btn, command=lambda: self.go(idp, idt, etat)).grid(column=1, row=idt, padx=5, ipady=2)

	def getDataTaches(self, etat, idp):
		connexion = sqlite3.connect('database.db')
		curseur = connexion.cursor()
		e = (etat,idp, )
		curseur.execute("SELECT * FROM taches WHERE etat=? AND idp=?",e)
		resultat = curseur.fetchall()
		connexion.close()
		return resultat		

	def getDataProjet(self, idp):
		connexion = sqlite3.connect('database.db')
		curseur = connexion.cursor()
		p = (idp, )
		curseur.execute("SELECT * FROM projets WHERE id=?", p)
		r = curseur.fetchone()
		connexion.close()	
		return r	

app = App('Trillo')