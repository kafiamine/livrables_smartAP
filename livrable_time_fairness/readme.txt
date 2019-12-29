-le code principal qui doit ètre exécuter est: "implement_time_fairness.py". ce code génère les commandes de traffic control, correspondants aux clients connectés/déconnéctés à l'AP et les mis dans un fichier, appelé "tc_htb.sh" pour ètre exécutées. 

-Le code ne traite pas les erreurs, tels que la vérification si un client dans la liste de deconnexion existe déja dans ceux connectés, ou le cas de double...    

- ce code génere deux fichier supplementaires. Le premier pour sauvegarder les noeuds connéctés avec leurs informations de classes, et filtres. Le deuxième fichier contient les identifiants des filtres des clients déconnéctés, qui constituent des trous de séquances dans les identifiants incrémentales. Ces deux fichiers ne doivent pas étre effacés pour le bon déroulement de script.

-Le fichier en sortie "tc_htb.sh", doit ètre donné les priorités pour s'executer. Cela est fait en exécutant la commande :
    Chmod +x tc_htb.sh  
-Le fichier est éxécuté: sudo ./tc_htb.sh 

-Au niveau de l'AP, un autre script doit ètre ècrit pour la gestion en continue de nouvelles connections/déconnection. Le script "implement_time_fairness.py", ainsi que fichier "tc_htb.sh" sont éxécutés à chaque modification


-=====important======
Les commandes: tc qdisc add dev wlp2s0 root handle 1: htb 
               tc class add dev wlp2s0 parent 1: classid 1:1 htb rate 150mbit ceil 150mbit 
doivent ètre exécutées, une seule fois, (en terminal) avant de commencer l'utilisation de script "implement_time_fairness.py". Les valeurs 150mbit sont indicatives, et doivent etre changées par celles de la capacité globale de l'AP.
