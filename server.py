# Emily Haigh
# Server code on Paradise

import socket
import os
from _thread import *
import time
import threading
import random

ServerSocket = socket.socket()
ServerSocket.settimeout(10)
host = '' # only works with ''
port = 6301
threadCount = 0
clients_list = []
# init a random list to be sorted
total_len = 11
toBeSorted = []
for i in range(total_len):
    toBeSorted.append(random.randrange(0,99,1))
print('toBeSorted: ', toBeSorted)

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('waiting for a connection')
# 5 is our max buffer size
ServerSocket.listen(5)

def merge2(left, right):
    answer = []
    l = r = 0
    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            answer.append(left[l])
            l += 1
        else:
            answer.append(right[r])
            r += 1
    while l < len(left):
        answer.append(left[l])
        l += 1
    while r < len(right):
        answer.append(right[r])
        r += 1
    return answer

# merge our 3 sorted arrays into the final answer
def merge3(left, center=[], right=[]):
    answer = []
    if right == []: 
        return merge2(left, center)
    else:
        return merge2(merge2(left, center), right)
    # print('merge3', answer)
    return answer

# A class for each client thread
class MyThread(threading.Thread):
    def __init__(self, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.list_to_sort = args[0]
        self.sorted_list = []
        self.connection = args[1]
        self.num = args[2] # which client should this thread talk to

    def run(self):
        # Convert List to string to send
        list_to_str = ''
        for x in range(len(self.list_to_sort)-1):
            list_to_str += str(self.list_to_sort[x]) + ','
        list_to_str += str(self.list_to_sort[len(self.list_to_sort)-1])
        clients_list[self.num].send(str.encode(list_to_str))
        
        self.connection.settimeout(7)
        try:        
            data = self.connection.recv(2048)
        except socket.timeout:
            exit()
            # kill this thread because it didn't work fast enough

        answer = data.decode('utf-8')
        # Convert answer from a string to a list of ints
        answer1 = answer.split(',')
        for x in range(len(answer1)):
            self.sorted_list.append(int(answer1[x]))
        print(threading.currentThread().getName(), self.sorted_list)
    
    def get_sorted_list(self):
        return self.sorted_list

stop = False
clients = 0
threads = []
while not stop:
    try:
        Client, address = ServerSocket.accept()
        clients_list.append(Client)
        clients += 1
        print('clients =', clients)
    except socket.timeout:
        # we will only wait a finite amount of time for the clients to connect
        stop = True
    except socket.error as e:
        print(e)
    
if clients == 0:
    toBeSorted.sort()
    print(toBeSorted)
    print('All work done at the master node because we had no clients connect')
    ServerSocket.close()
    exit()

# split the list based on the number of clients 
for x in range(clients):
    fraction = len(toBeSorted)//clients   
    a = x * fraction
    b = a + fraction
    # this if stmt handles if the length of our list toBeSorted is not divisible by the number of clients
    if x == clients - 1:
        b = len(toBeSorted)
    arr = toBeSorted[a:b]
    threads.append(MyThread( args=(arr, clients_list[x], x)))
    threadCount += 1
    threads[x].start()
    print('Thread Number', threadCount, toBeSorted[a:b])
    
# wait 7 seconds for the clients to return their sorted lists    
time.sleep(7)

# get all the sorted array parts here and merge
# we also need to handle client failures here
list1 = threads[0].get_sorted_list()
if threadCount > 1:
    list2 = threads[1].get_sorted_list()
if threadCount == 3:
    list3 = threads[2].get_sorted_list()

if threadCount == 1:
    if len(list1) > 0:
        print('Our final sorted list is', list1)
    else:
        toBeSorted.sort()
        print('Our final sorted list is', toBeSorted)
elif threadCount == 2:
    if len(list1) == 0:
        list1 = toBeSorted[:fraction]
        list1.sort()
    if len(list2) == 0:
        list2 = toBeSorted[fraction:]
        list2.sort()
    print('Our final sorted list is', merge3(list1, list2))    
elif threadCount == 3:
    if len(list1) == 0:
        list1 = toBeSorted[:fraction]
        list1.sort()
    if len(list2) == 0:
        list2 = toBeSorted[fraction:2*fraction]
        list2.sort()
    if len(list3) == 0:
        list3 = toBeSorted[2*fraction:]
        list3.sort()
    print('Our final sorted list is', merge3(list3, list2, list1))
else:
    toBeSorted.sort()
    print('Our final sorted list is', toBeSorted)

ServerSocket.close()
# print('socket is closed')
exit()



