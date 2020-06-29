import threading
import time
import pickle
import socket
import csv

try_dict = {
} 
"""
import csv
with open("cn_2.csv") as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        train = row[0]
        l = []
        b = []
        l = list(row[1:])
        for i in l:
            if(i != ""):
                    b.append(i)

try_dict[train] = b
"""

'''
writer = csv.writer(open('/tmp/output.csv', 'w'))
writer.writerows(lines)
'''
user_name = {
    
}

station = {
    "city_1": ["train_a", "train_b"],
    "city_2": ["train_a", "train_b", "train_c", "train_d", "train_e"],
    "city_3": ["train_a", "train_c"],
    "city_4": ["train_a", "train_c", "train_e"],
    "city_5": ["train_a", "train_b", "train_d", "train_e"]
}
stops = {
    "train_a": ["c1", "c2", "c3", "c4", "c5"],
    "train_b": ["c1", "c2", "c5"],
    "train_c": ["c2", "c3", "c5"],
    "train_d": ["c2", "c5"],
    "train_e": ["c2", "c4", "c5"]
}
train = {
    "train_a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "train_b": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "train_c": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "train_d": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "train_e": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
}

def cancel_tickets1(l):
    for i in l:
        if(i != "pwd"):
            for j in l[i]:
                train[i][int(j)-1] = int(j)



def cancel_tickets2(l, train_name, cancel_list):
    for i in cancel_list:
        train[train_name][int(i)-1] = int(i)
        l[train_name].remove(i)
# user_name dictonary will have a dictonary with it. each dictonary key is user name, and it will have 2 keys. passwd and seat number
def thread_function(conn):
    while True:
        id_rcv = conn.recv(1000)
        id_rcv = pickle.loads(id_rcv)
        if(id_rcv[0] not in user_name): # id_rcv[0] will have user name , id_rcv[1] will have passwd
            user_name[id_rcv[0]] = {} # creating dictonary for each user name
            user_name[id_rcv[0]]["pwd"] = id_rcv[1] # creating a new key and associating a value to it
            for i in stops:
                user_name[id_rcv[0]][i] = []
            msg_send = "User Successfully added to database"
            enter = 1
            msg_send = msg_send.encode()
            conn.send(msg_send)
        elif(id_rcv[0] in user_name):
            if(id_rcv[1] != user_name[id_rcv[0]]["pwd"]):
                msg_send = "Wrong Password login failed"
                enter = 0
                msg_send = msg_send.encode()
                conn.send(msg_send)
            else: 
                msg_send = "Logged in Successfully"
                enter = 1
                msg_send = msg_send.encode()
                conn.send(msg_send)
        else:
            msg_send = "Login failed"
            msg_send = msg_send.encode()
            conn.send(msg_send)
        while(enter):
            data = conn.recv(10)
            if data.decode() == str(1):
                y1 = "Connected"
                y = y1.encode()
                conn.send(y)
                two_data = []
                ls = conn.recv(200)
                ls2 = pickle.loads(ls)
                ls2[0] = ls2[0].decode()
                ls2[1] = ls2[1].decode()
                for i in stops:
                    if ls2[0] in stops[i] and ls2[1] in stops[i]:
                        le = len(train[i])
                        li = train[i]
                        train_is = i
                two_data.append(li)
                two_data.append(train_is)
                print("Booking ticket in "+train_is)
                data_1 = pickle.dumps(two_data)
                conn.send(data_1)
                data_2 = conn.recv(100)
                data_3 = pickle.loads(data_2)
                print(data_3)
                for i in data_3:
                    print("here...")
                    if li[int(i) - 1] == "B":
                        err = "F" + str(i)
                       # check_now = 0
                        err_msg = err.encode("utf-8")
                        conn.send(err_msg)
                    else:
                        li[int(i) - 1] = "B"
                        upd_msg = "S" + str(i)
                        #train_list.append(i)
                        upd = upd_msg.encode("utf-8")
                        user_name[id_rcv[0]][train_is].append(i) 
                        conn.send(upd)
                    throw = conn.recv(100)
                print("-----")
                print(user_name[id_rcv[0]][train_is])
                print("-----")
                print("Done looping")
                v = "confirm"
                conn.send(v.encode())
            elif data.decode() == str(2):
               # k = "Cancel"
                #k = k.encode()
                #onn.send(k)
                #ls = conn.recv(100)
                copy_d = {}
                d = user_name[id_rcv[0]]
                for i in d:
                    if(i != "pwd"):
                        copy_d[i] = d[i]
                print(copy_d)
                #l = user_name[id_rcv[0]]
                cancel_choice = pickle.dumps(copy_d)
                conn.send(cancel_choice)
                test = conn.recv(10)
                test = test.decode()
                if(test == "P"):
                    a = "S"
                    a = a.encode()
                    conn.send(a)
                    cancel_recv = conn.recv(100)
                    cancel_recv = pickle.loads(cancel_recv)
                    if(cancel_recv[0] == '0'):
                        cancel_tickets1(user_name[id_rcv[0]])
                        for i in stops:
                            user_name[id_rcv[0]][i] = []

                    else:
                        k = len(cancel_recv)
                        k = k-2
                        cancel_tickets2(user_name[id_rcv[0]], cancel_recv[1], cancel_recv[2:])
                            #user_name[id_rcv[0]][cancel_recv[1]].remove(cancel_recv[i+2])

                    #cancel_recv = pickle.loads(cancel_recv)
                    a = "try"
                    print(a)
                    a = a.encode()
                    conn.send(a)
                else:
                    a = "F"
                    a = a.encode()
                    conn.send(a)


            elif data.decode() == str(3):
                y1 = "Connected"
                y = y1.encode()
                conn.send(y)
                ls = conn.recv(200)
                ls2 = pickle.loads(ls)
                ls2[0] = ls2[0].decode()
                ls2[1] = ls2[1].decode()
                #print(ls2)
                #le = 10
                for i in stops:
                    if ls2[0] in stops[i] and ls2[1] in stops[i]:
                        le = len(train[i])
                        li = train[i]
                        train_is = i
                print("Best Train Route available in "+train_is)
                data_1 = pickle.dumps(li)
                conn.send(data_1)


            else:
                k = "Exit"
                k = k.encode()
                conn.send(k)
                enter = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1025))  # must be greater than 1023 why?

s.listen(5)
while True:
    print("checking connections....")
    conn, addr = s.accept()
    x = threading.Thread(target=thread_function, args=(conn,))
    x.start()
    print("Yo")
