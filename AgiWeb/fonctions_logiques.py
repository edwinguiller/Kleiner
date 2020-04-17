# coding: utf-8
import sqlite3 as lite
import time

def transformation(a):#on transforme la chaine pour qu'elle soit traitable
	c=a
	supprimable = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â',' ', '-', '_','.', ',',"'",'!' ,':', '/']
	correct = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a', '', '', '', '', '','', '', '', '']
	for i in range(len(supprimable)):
		c=c.replace(supprimable[i],correct[i])
	c=c.lower()
	return(c)
	
def compare_nom(a,b):#On regarde si a est dans b, b est une liste
	A=transformation(a)
	B=[]
	for i in range(len(b)):
		B.append(transformation(b[i])) 
	if A in B:
		return(True)
	return(False)

def liste(b):#transforme un dictionnaire en liste
	c=[]
	for chaque in b:
		c.append(chaque[0])
	return(c)

def creer_id(b):#créé un id
	c=liste(b)
	taille=len(c)
	if taille==0:
		ide=1
	else:
		ide=max(c)+1
	return(ide)
