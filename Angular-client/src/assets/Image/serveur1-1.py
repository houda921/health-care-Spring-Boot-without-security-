import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread , Event ,Lock
from datetime import datetime
import tkinter as tk
import time

import queue
import tkinter as tk

q=queue.Queue(10) #
lockFileBien = Lock()
lockFileHisto = Lock()
lockFileInvoice = Lock()
lockVente = Lock()
lockInvoice= Lock()
counter =200

#Accept the connection receive by client
def accept_client_connexions():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s is connected." % client_address)
        client.send(bytes("Welcome to Our Application!\n", "utf8"))
        time.sleep(0.05)
        client.send(bytes(" Type your id please !\n", "utf8"))
        addresses[client] = client_address
        Thread(target=manage_client, args=(client,)).start()

#Synchronise clients
def manage_client(client):
    nom = client.recv(BUFSIZ).decode("utf8")
    client.send(bytes('welcome among us %s! \n' % nom, "utf8"))
    time.sleep(0.05)
    client.send(bytes('If you ever want to quit, type QUIT \n', "utf8"))
    msg = "%s joined Application\n" % nom
    broadcast(bytes(msg, "utf8"))
    clients[client] = nom
    file = open("files/Bien.txt", "r")
    lockFileBien.acquire()
    buf = ""
    liste=[]
    client.send(bytes("The list of accounts in the banc\n:","utf8"))
    time.sleep(0.05)
    client.send(bytes("id init last state buyers\n","utf8"))
    for line in file.readlines():
        x, y, z, w, t = line.split()
        if w == "Disponible":
           liste.append(line)
           client.send(bytes(line,"utf8"))
           time.sleep(0.05)
    lockFileBien.release()
    file.close()
    length = len(liste)
    for i in range(length):
        x, y, z, w, t = liste[i].split()
        debut=(time.time())
        while  w=="Disponible" :
            client.send(bytes("We will sell the property : \n"+str(x)+"with the price : "+str(z), "utf8"))
            time.sleep(0.05)
            client.send(bytes("1) Buy a property\n", "utf8"))
            time.sleep(0.05)
            client.send(bytes("2) Receive an invoice  \n", "utf8"))
            time.sleep(0.05)
            client.send(bytes('\n if you ever want to quit, type QUIT \n', "utf8"))
            msg = client.recv(BUFSIZ)
            client.send(bytes("\n The remaining time is :%.2f \n " % (30-(time.time()-debut)),"utf8"))
            if msg != bytes("QUIT", "utf8"):
                if msg == bytes(str(1),"utf8") :
                    print(datetime.now().strftime("%S"))
                    w= sale(client,z,nom,x,debut)
                    break
                elif msg == bytes(str(2), "utf8") :
                    lockInvoice.acquire()
                    consult_invoice(client,nom)
                    lockInvoice.release()

            else:
                client.send(bytes("\n !!!You have left Auction!!! \n", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("\n !!!%s left Auction!!!\n" % nom, "utf8"))
                break

#brodcast message between server and clients
def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

#Sale objects
def sale (client,z,nom,idbien,debut):

    verif=0
    test=True

    while (test and verif==0 and 30-(time.time()-debut)>0 ):

        client.send(bytes('give your proposal : \n', "utf8"))
        client.settimeout(30)
        try:
            msg_prix = client.recv(BUFSIZ).decode("utf8")

            print(msg_prix)
        except:
            break

        else :
            broadcast(bytes("The price that the buyer offered %s == "%nom + str(msg_prix),"utf8"))
            broadcast(bytes("The remaining time is : %.2f" % (30 - (time.time() - debut)), "utf8"))
            if int(msg_prix) < int(z):
                client.send(bytes("The unacceptable amount sorry", "utf8"))

            else:
                if 30-(time.time()-debut)>0 :
                    print("1 %s : "%msg_prix)
                    debut=time.time()
                    file=open("histo.txt","a")
                    lockFileHisto.acquire()
                    ligne=str(nom)+" "+str(msg_prix)+" echec\n"
                    file.write(ligne)
                    lockFileHisto.release()
                    file.close()
                    i = -1
                    biens = open("bien.txt", "r")
                    lockFileBien.acquire()

                    for lines in biens.readlines():
                        x, y, z, w, t = lines.split()
                        i = i + 1
                        if x == idbien:
                            indice = i
                            break

                    aux = str(x) + " " + str(y) + " " + msg_prix+ " Disponible " + nom + "\n"
                    lockFileBien.release()
                    biens.close()
                    replace_line("bien.txt", indice, aux)
                    print(30-(time.time()-debut))

    histoR = open('histo.txt', 'r')
    lockFileHisto.acquire()
    liste = []
    for line in histoR.readlines():
        liste.append(line)
    lockFileHisto.release()
    histoR.close()
    id, ai, ao =liste[len(liste)-1].split()
    ao="succes"
    nv_ligne=str(id)+" "+str(ai)+" "+str(ao)+"\n"
    liste[len(liste) - 1]=nv_ligne
    print("\nThe buyer who won is:  %s \n" % nv_ligne)
    broadcast(bytes("\n***************** Congratulation, The buyer who won is : %s ****************\n " %nv_ligne, "utf8"))
    f = open('histo.txt', 'w')
    lockFileHisto.acquire()
    for l in liste:
        f.write(l)
    lockFileHisto.release()
    f.close()
    i=-1
    biens=open("bien.txt","r")
    lockFileBien.acquire()

    for lines in biens.readlines():
        x, y, z, w, t = lines.split()
        i=i+1
        if x==idbien :
            indice=i
            break
    aux=str(x) +" "+ str(y) +" "+ str(ai) +" Vendu "+str(id)+"\n"
    lockFileBien.release()
    biens.close()
    replace_line("bien.txt",indice,aux)
    consult_invoice(client,nom)
    return 'Vendu'

#Manipulate invoice data
def invoice(client,nom):

    biens=open("bien.txt","r")
    lockFileBien.acquire()
    somme=0
    for lines in biens.readlines():
        x, y, z, w, t = lines.split()
        if t==nom :
            somme=somme+int(z)

    somme=somme*1.2
    lockFileBien.release()
    biens.close()

    fact = open("facture.txt","r")
    lockFileInvoice.acquire()
    lines = fact.readlines()
    line_count =0
    for line in fact:
        if line != "\n":
            line_count += 1
    lockFileInvoice.release()

    fact.close()
    print(line_count)
    fact = open("facture.txt","r")
    lockFileInvoice.acquire()
    lines = fact.readlines()
    i=-1
    for line in lines :
        x, y = line.split()
        i=i+1
        if x==nom :
            indice=i
            break
        else :
            indice=-2


    if(indice==-2):
        lockFileInvoice.release()
        fact.close()
        replace_line("facture.txt",line_count,nom+" "+str(somme)+"\n")

    else :
        lockFileInvoice.release()
        fact.close()
        replace_line("facture.txt",indice,nom+" "+str(somme)+"\n")


#Show invoice result to each client
def consult_invoice(client,nom):
    invoice(client,nom)
    fact = open("files/facture.txt","r")
    lockFileInvoice.acquire()
    lines = fact.readlines()
    for line in lines :
        x, y = line.split()
        if x==nom :
            break
    lockFileInvoice.release()
    fact.close()
    client.send(bytes("your Invoice is :   "+str(y)+"\n", "utf8"))


#replace line in the files
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


clients = {}

addresses = {}

HOST = '127.0.0.1'
PORT = 8007
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)  # le type du socket : SOCK_STREAM pour le protocole TCP # inet ipv4 ip
SERVER.bind(ADDR)  # liaison entre socket et @ip

if __name__ == "__main__":
    SERVER.listen(5)
    print("waiting for connection ...")
    ACCEPT_THREAD = Thread(target= accept_client_connexions)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
