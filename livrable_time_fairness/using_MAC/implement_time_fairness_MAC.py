#on suppose qu'on dispose de deux fichiers en entree a ce code. Le premier fichier s'appelle "liste_connected.txt", contient la liste des clients connectes a cet instant avec l'AP. Le deuxieme fichier s'appelle "liste_disconected.txt" qui contient la liste des clients deconnectes a cet instant 

# ce code genere les commandes de traffic control, correspondant aux clients connectes/deconnectes a l'AP et les mis dans un fichier, appele "tc_htb.sh" pour etre execute. Le code ne traite pas les erreurs, tels que la verification si un client dans la liste de deconnexion existe deja dans ceux connectes, ou le cas de double... 

# ce code genere deux fichier supplementaires le premier pour sauvegarder les noeuds connectes avec leur informations de classes, et filtres. Le deuxieme fichier contient les identifiants des filtres des clients deconnectes, qui constituent des trous de sequances dans les identifiants incrementales.

import os
import sys
from management_functions_MAC import *

   
wireless_dev_id="wlp2s0"  # l'identifiant de l'interface sans fil de l'AP a laquelle le controle de traffic sera applique


Connected_nodes=upload_table("liste_connected.txt")  # recupere la liste des clients connectes d'un fichier sous forme: @MAC demande debit 
#chaque ligne contient un client. la demande et le debit sont en Megabits per second (mbit), exemple: 

#6c:88:14:f0:dc:14 100 144
#6c:88:14:f0:dc:15 50 50



 
Disconnected_nodes=upload_table("liste_disconected.txt") # recupere la liste des clients deconnectes. On a besoin que de l'adresse MAC

f1= open("tc_htb.sh", 'w') # le fichier qui va contenir les commandes de traffic control

c_code="#!/bin/bash \n"
f1.write(c_code)

c_code="tc qdisc add dev %s root handle 1: htb \n"% wireless_dev_id
c_code=c_code+"tc class add dev %s parent 1: classid 1:1 htb rate 150mbit ceil 150mbit \n\n"%wireless_dev_id      #**********ces deux commandes doivent etre executees qu'une seule fois au debut, puisque concerne le root seulement

f1.write(c_code)

i=0

manage_Disconnected_nodes=[]
for node in Disconnected_nodes: #commence par gerer les clients deconnectes, en suprimant: classe, queue et filtre correspandants 
 	
	(id_classe,id_filter)=disconnection_coordinates(node)
	element=[id_classe,id_filter]
	manage_Disconnected_nodes.append(element)
	
	c_code="tc qdisc delete dev %s parent 1:%d handle %d: pfifo \n"%(wireless_dev_id,id_classe,id_classe+100)
	f1.write(c_code)

	c_code="tc filter del dev %s parent 1: proto ip prio 1 handle 800::%d u32 \n"%(wireless_dev_id,id_filter)
	f1.write(c_code)

	c_code="tc class del dev %s parent 1: classid 1:%d \n\n"% (wireless_dev_id,id_classe)
	f1.write(c_code)
	
disconnection_process(manage_Disconnected_nodes)


fifo_limit= 1000   #fixer la taille des files des donnees destinees aux clients




nb_nodes=len(Connected_nodes)

manage_connected_nodes=[]

#for node in set(Connected_nodes):
for node in Connected_nodes:   #gerer les nouveaux clients connectes en leur creants: classe, queue, filtre. Modifier aussi les capacites de ceux existants, si besoin   
	
	(existing_node,id_classe, id_filter)=alreadyconnected(node[0],manage_connected_nodes)

	if (existing_node==True):
	
		c_code="tc class change dev %s parent 1:1 classid 1:%d htb rate %.2fmbit ceil %.2fmbit \n\n"%(wireless_dev_id,id_classe,min(float(int(node[2])/float(nb_nodes)),int(node[1])),min(float(int(node[2])/float(nb_nodes)),int(node[1]))) # on mis la valeur de ceil a la meme valeur de rate
		#c_code="tc class change dev %s parent 1:1 classid 1:%d htb rate %.2fmbit ceil %dmbit \n\n"%(wireless_dev_id,id_classe,min(float(int(node[2])/float(nb_nodes)),int(node[1])),int(node[2]))  # valeur de rate et ceil different 
		f1.write(c_code)

	else:
		c_code="tc class add dev %s parent 1:1 classid 1:%d htb rate %.2fmbit ceil %.2fmbit \n"%(wireless_dev_id,id_classe,min(float(int(node[2])/float(nb_nodes)),int(node[1])),min(float(int(node[2])/float(nb_nodes)),int(node[1]))) # on mis la valeur de ceil a la meme valeur de rate

		#c_code="tc class add dev %s parent 1:1 classid 1:%d htb rate %.2fmbit ceil %dmbit \n"%(wireless_dev_id,id_classe,min(float(int(node[2])/float(nb_nodes)),int(node[1])),int(node[2])) # valeur de rate et ceil different 
 
		f1.write(c_code)
		
		analyse=node[0].strip().split(':')
				
		c_code="tc filter add dev %s parent 1:0 prio 1 protocol ip u32 match u16 0x0800 0xffff at -2 match u32 0x%s%s%s%s 0xffffffff at -12 match u16 0x%s%s 0xffff at -14 classid 1:%d \n"%(wireless_dev_id,analyse[2],analyse[3],analyse[4],analyse[5],analyse[0],analyse[1],id_classe)




		#c_code="tc filter add dev %s parent 1:0 prio 1 protocol ip u32 match ip dst %s classid 1:%d \n"%(wireless_dev_id,node[0],id_classe)   # si on veut faire le filtrage par @IP
		f1.write(c_code)
				
		c_code="tc qdisc add dev %s parent 1:%d handle %d: pfifo limit %d \n\n"%(wireless_dev_id,id_classe,id_classe+100,fifo_limit)	
		f1.write(c_code)
		
		element=[node[0],id_classe,id_filter]
		manage_connected_nodes.append(element)		

connection_process(manage_connected_nodes)
		
		

f1.close()




