def alreadyconnected(node,manage_connected_nodes): #fonction qui verifie l'existance ou non d'un client dans la liste de ceux existants, en donnant sa classe et son filtre. S'il n'existe pas, elle lui attribue un identifiant pour la classe et le filtre
 
	import os	


	exist=False
	if (os.path.isfile("connected_nodes.txt")) and (os.stat("connected_nodes.txt").st_size!=0):
		f1=open("connected_nodes.txt",'r')
	
		for line in f1.readlines():
			analyse=line.strip().split()  
			if (analyse[0]==node): 
				exist=True
				break
	
		f1.close()	
		if analyse[0]==node:
			return (exist, int(analyse[1]), int(analyse[2]))
		else:
			(id_classe,id_filter)= new_connected(node, int(analyse[1]), int(analyse[2]),manage_connected_nodes)	
			return  (exist,id_classe,id_filter)
	else:
		(id_classe,id_filter)= new_connected(node, 1, 799,manage_connected_nodes)	
		return  (exist,id_classe,id_filter)	



def new_connected(node,last_value_classe,last_value_filter,manage_connected_nodes): # fonction a utiliser dans la fonction "alreadyconnected" pour attribuer le nouveau identifiant de classe et de filtre


	import os	

	if (os.path.isfile("disconect_class_filter.txt")) and (os.stat("disconect_class_filter.txt").st_size!=0):	
		f2=open("disconect_class_filter.txt",'r')		
		f3=open("new_disconect_class_filter.txt",'w')
		line=f2.readline()
		analyse=line.strip().split()		
		id_classe=int(analyse[0])
		id_filter=int(analyse[1])
		for line in f2.readlines():
			f3.write(line)

		f2.close()
		f3.close()
		os.remove("disconect_class_filter.txt")	
		os.rename("new_disconect_class_filter.txt","disconect_class_filter.txt")	
	else:
		if (len(manage_connected_nodes)==0):	
			id_classe=last_value_classe+1
			id_filter=last_value_filter+1
		else:
			if (manage_connected_nodes[len(manage_connected_nodes)-1][1]> last_value_classe):
				id_classe=manage_connected_nodes[len(manage_connected_nodes)-1][1]+1		
				id_filter=manage_connected_nodes[len(manage_connected_nodes)-1][2]+1
			else:
				id_classe=last_value_classe+1
				id_filter=last_value_filter+1
	return (id_classe,id_filter)	



def connection_process(nodes): # fonction qui gere le tri du fichier de fonctionement des noeuds connectes 
	import os	

	if (os.path.isfile("connected_nodes.txt")) and (os.stat("connected_nodes.txt").st_size!=0):
		f1=open("connected_nodes.txt",'r')
		f2=open("new_connected_nodes.txt",'w')


		line=f1.readline()
		i=0	
		while line!="":
			analyse	=line.strip().split()		
			while (i<len(nodes)) and (nodes[i][1]<int(analyse[1])):
				element=nodes[i]			
				c_code=element[0]+" " +str(element[1])+ " "+ str(element[2])+"\n"
				f2.write(c_code)	 	
				i=i+1
			f2.write(line)
			line=f1.readline()
	
		while i< len(nodes):
			element=nodes[i]
			i=i+1		
			c_code=element[0]+" " +str(element[1])+ " "+ str(element[2])+"\n"
			f2.write(c_code)
		

	
		f1.close()
		f2.close()
		os.remove("connected_nodes.txt")	
		os.rename("new_connected_nodes.txt","connected_nodes.txt")	
	
	else:
		f1=open("connected_nodes.txt",'w')
		for node in nodes:
			c_code=node[0]+" " +str(node[1])+ " "+ str(node[2])+"\n"		
			f1.write(c_code)
		f1.close()	
		
	return



def disconnection_coordinates(node): #fonction qui retourne les identifiants de classes et de filtre du client deconnectes
	
	f1=open("connected_nodes.txt",'r')

	for line in f1.readlines():
		analyse=line.strip().split()
		if (analyse[0]==node[0]): 
			id_classe=int(analyse[1])
			id_filter=int(analyse[2])
			break
	
	f1.close()
	return (id_classe,id_filter)


def ordonate_classes(nodes): # fonction qui tri les clients, nodes, par leur ordres croissants des identifiants des classes pour faciliter la gestion

	ordonne=[]
	for element in nodes:
		index_tri=0		
		size=len(ordonne)
		if len(ordonne)==0: 
			ordonne.append(element)
		
		else:     
			for element1 in ordonne:		
				if element[0]<element1[0]: break
			 	else: index_tri=index_tri+1
					
			ordonne.append(ordonne[size-1])
			index2_tri=1	
			while (index2_tri < size-index_tri):	
				ordonne[size-index2_tri]=ordonne[size-index2_tri-1]
				index2_tri=index2_tri+1
			
			ordonne[index_tri]=element
	return ordonne



def disconnection_process(nodes): #fonction qui gere les client decoonectes en les enlevant du fichier de fonctionement des clients connetctes, et les mettre dans le fichier des identifiant des classes et filtres a reutiliser, en gardant les fichier de fonctionamant tries pour utilisation anterieures simples. je n'ai pas verifier si les elements a deconnecter existe reelement ou pas

	import os	
	
 	if os.path.isfile("connected_nodes.txt"):
		f1=open("connected_nodes.txt",'r')
		f2=open("new_connected_nodes.txt",'w')
		ordonated_disconnected=ordonate_classes(nodes)
		
 		line=f1.readline()
		if line !="": 
			analyse=line.strip().split()
						
		for element in ordonated_disconnected:
			while (line !="") and (element[0] != int(analyse[1])):
				f2.write(line)
				line=f1.readline()
				analyse	=line.strip().split()
			if (line !="") and (element[0] == int(analyse[1])):
				line=f1.readline()
				analyse	=line.strip().split()
			
		while line!="":
			f2.write(line)
			line=f1.readline()
		f1.close()
		f2.close()
		os.remove("connected_nodes.txt")	
		os.rename("new_connected_nodes.txt","connected_nodes.txt")	
		disconnected_management(ordonated_disconnected)		
		
	return		
	
def last_elem(file): # une simple fonction qui retourne le dernier element d'un fichier
	f1=open(file,'r')
	line=element=f1.readline()
	while line!="":
		element=line		
		line=f1.readline()
	f1.close()		

	return element
	
	
def disconnected_management(classe_filter):  # fonction qui gere les identifiants des classes et filtre des noeuds deconnectes pour pouvoir les reutiliser

	import os	
	
	compare_with=last_elem("connected_nodes.txt")
	if (compare_with==""):
		if (os.path.isfile("disconect_class_filter.txt")): os.remove("disconect_class_filter.txt")
	
	else:
		analyse_connected=compare_with.strip().split()

		if (os.path.isfile("disconect_class_filter.txt")) and (os.stat("disconect_class_filter.txt").st_size!=0):	
			f1= open("disconect_class_filter.txt", 'r')
			f2=open("new_disconect_class_filter.txt", 'w')
			i=0	
			for line in f1.readlines():
				analyse=line.strip().split()	
				while (i< len(classe_filter)) and (int(analyse[0])>classe_filter[i][0]) and (int(analyse_connected[1])>classe_filter[i][0]):
					c_code=str(classe_filter[i][0])+" "+str(classe_filter[i][1])+ "\n"		
					i=i+1
					f2.write(c_code)	
		
				if (int(analyse_connected[1])> int(analyse[0])): 
					f2.write(line)
			while (i< len(classe_filter)) and (int(analyse_connected[1])>classe_filter[i][0]):
				c_code=str(classe_filter[i][0])+" "+str(classe_filter[i][1])+ "\n"		
				i=i+1
				f2.write(c_code)
			f2.close()			
			f1.close()
			os.remove("disconect_class_filter.txt")
			os.rename("new_disconect_class_filter.txt","disconect_class_filter.txt")	
		else:
		
			f1= open("disconect_class_filter.txt", 'w')
			for element in classe_filter:				
				if (int(analyse_connected[1])> element[0]):	
					c_code=str(element[0])+" "+str(element[1])+ "\n"
					f1.write(c_code)
			f1.close()		
		
	return 



def upload_table(file): #charge le contenu du fichier file, des clients connectes/deconnectes dans une table pour pouvoir l'utiliser
	import os
	table=[]
	if (os.path.isfile(file)) and (os.stat(file).st_size!=0):
		f1= open(file, 'r')
		for line in f1.readlines():
			analyse=line.strip().split()  
			table.append(analyse)			
		f1.close()	
			
	return table




