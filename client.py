# Emily Haigh
# Client code on Waterfalls

import socket
import time

# Create a socket
ClientSocket = socket.socket()
host = 'Paradise'
port = 6301

# Merge sort
def mergeSort(arr):
    length = len(arr)
    if length > 1:
        left = arr[:length//2]
        right = arr[length//2:]
        mergeSort(left)
        mergeSort(right)
        l = r = x = 0
        while l < len(left) and r < len(right):
            if left[l] < right[r]:
                arr[x] = left[l]
                l += 1
            else:
                arr[x] = right[r]
                r += 1
            x += 1
        while l < len(left):
            arr[x] = left[l]
            x += 1
            l += 1
        while r < len(right):
            arr[x] = right[r]
            x += 1
            r += 1
    return arr

print('Waiting for a connection')
try:
    ClientSocket.connect((host,port))
    print('connected')
except socket.error as e:
    print('There is a socket error')
    print(str(e))

# Get the list we need to sort here 
Response = ClientSocket.recv(2048).decode('utf-8')

# Convert Response from a string to an array of numbers 
array = Response.split(',')
array1 = []
for x in range(len(array)):
    array1.append(int(array[x]))
answer = mergeSort(array1)
print(answer)

# Convert the array to a string to send back
string_answer = ''
for x in range(len(answer)-1):
    string_answer += str(answer[x]) + ','
string_answer += str(answer[len(answer)-1])
    
# Send the sorted list 
ClientSocket.send(str.encode(string_answer))
    
ClientSocket.close()
    




