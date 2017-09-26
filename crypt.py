#!/usr/bin/python3

import os
import time

alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(),./;'[]-=<>?:{} ")
alphabet.append('"')

def encrypt(s,p):
    secret = list(s)
    for c in range(0,len(secret)):
        if not secret[c] in alphabet:
            secret[c] = '?'
    password = list(p)
    for x in range(0,len(password)):
        for y in range(0,len(secret)):
            key = (alphabet.index(password[x])+1)*(y+1)*(x+1)
            secret[y] = alphabet[(alphabet.index(secret[y])+key+1)%len(alphabet)]
            
    return str(''.join(secret))

def decrypt(s,p):
    secret = list(s)
    password = list(p[::-1])
    for x in range(0,len(password)):
        for y in range(0,len(secret)):
            key = (alphabet.index(password[x])+1)*(y+1)*(len(password)-x)
            secret[y] = alphabet[(alphabet.index(secret[y])-key-1)%len(alphabet)]
            
    return str(''.join(secret))
        

            
while True:
    action = input('Encrypt or decrypt your vault or a file?(E/D & V/F) >>>')
    if len(action) == 2:
        if action[1] == 'V':
            os.chdir('/home/david/Documents/Scripts')
            if action[0] == 'E':
                message = input('Enter your message >>>')
                password = input('Enter your password >>>')
                data = encrypt(message,password)
                with open('vault','w') as f:
                    f.write(data)
                break
            elif action[0] == 'D':
                password = input('Enter your password >>>')
                with open('vault','r') as f:
                    data = f.readlines()[0]
                print(decrypt(data,password))
                break
            else:
                print('Invalid flag')
                time.sleep(2)
        elif action[1] == 'F':
            path = input('Enter path to file >>>')
            filepath = path[:len(path)-path[::-1].index('/')]
            filename = path[len(path)-path[::-1].index('/'):]
            try:
                os.chdir(filepath)
                if action[0] == 'E':
                    with open(filename,'r')as f:
                        message = f.readlines()
                        for l in range(0,len(message)):
                            if message[l][-1] == '\n':
                                message[l] = message[l][:-1]
                    password = input('Enter your password >>>')
                    data = []
                    for line in message:
                        data.append(encrypt(line,password)+'\n')
                    with open(filename,'w') as f:
                        f.writelines(data)
                    break
                elif action[0] == 'D':
                    with open(filename,'r') as f:
                        message = f.readlines()
                        for l in range(0,len(message)):
                            if message[l][-1] == '\n':
                                message[l] = message[l][:-1]
                    password = input('Enter your password >>>')
                    data = []
                    for line in message:
                        data.append(decrypt(line,password)+'\n')
                    with open(filename,'w') as f:
                        f.writelines(data)
                    break
                else:
                    print('Invalid flag')
                    time.sleep(2)
            except:
                print('File could not be found')
                time.sleep(2)
        else:
            print('Invalid flag')
            time.sleep(2)
    else:
        print('Invalid flag')
        time.sleep(2)
        
