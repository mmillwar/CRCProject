import socket
import time
import matplotlib.pyplot as plt # Plots, code taken from matplotlib.org
from numpy.random import randint 

def getCRC(ht,div):
    #add your code here
    #print(ht + " Caw")
    hexstr = ht
    print(str(hexstr) + " Hello" )
    bt=[int(b) for b in bin(int(hexstr,16))[2:].zfill(8)]
    print(str(bt) + " BT")
    #q = len(div)-1
    #bt = ht
    #bt=[bin(int(ht,16)).zfill(8)]
    #bt=[int(c) for c in bin(int(ht,16))[:2].zfill(8)]
    x =[]
    y =[0,0,0,0]
    for a in range(len(div)):
        x.append(9)
    #bt = int(bt, base=16)
    for i in range(len(div)-1):
        bt.append(0)
        #bt+=0
    #print(bt)
    #for i in range(len(bt)):
    #while bt[0] != 1 and len(bt) > 5:
    while bt[0] != 1 and len(bt) > len(div):
        #print(bt) #debug
        bt.pop(0)
        #x = bt[0:4] ^ div
    for j in range(len(div)):
        #print(bt[j])
        #x = [1,1,1,1,0]
        x[j] = int(bt[j]) ^ div[j]
    count = len(div)
    #print("Debug length of bt = " + str(len(bt)))
    while (count) < len(bt):
        while x[0] != 1 and (count) < len(bt):
            x.pop(0)
            x.append(int(bt[count]))
            count = count+1
        #print(" x = " + str(x))
        for j in range(len(div)):
            x[j] = int(x[j]) ^ div[j]
            #print(j)
            #bt[0:4] = x
        #print("Count  =" + str(count) + " len of bt is still" + str(len(bt)) )
    #print(bt)
    #print(x)
    while x[0] != 1:
        x.pop(0)
    if len(x) == len(div):
        for j in range(len(div)):
            x[j] = int(x[j]) ^ div[j]
        x.pop(0)
    for k in range(len(x)):
        bt[-k-1] = x[-k-1]
    #print(bt)
    #print(str(x) + "CRC")
    if(len(x)<len(div)-1):
        for j in range(len(x)):
            y[j+len(div)-1-len(x)] = x[j]
        #print(str(y) + "CRC")
        return y
    #print(str(x) + "CRC")    
    return x

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('199.223.115.24', 9996) 
cnt = 0
attempts = 0
latency = [0]*100
countForPlot = [0]*100
dropAVG = [0]*100
frame = '7e'
msg = ''
hexi= ''
div = [1,0,0,1,1]
lst = randint(256, size = 10) 
for n in lst:
    msg += str(hex(n)[2:]) 
    #msgH = msg.encode("hex")
    for i in range(10): 
        attempts +=1
        print(msg)
        crc = ''
        
        #
        count = str(cnt)
        counter = hex(int(count))[2:]
        msg1 =frame + counter  + msg
        #
        #CRCmsg = getCRC(msg,div)
        print("CCCCC"+ str(msg1))
        CRCmsg = getCRC(msg1,div)
        #print(CRCmsg)
        for i in range(len(CRCmsg)):
            crc += str(CRCmsg[i])
        #print(crc)
        hexi = hex(int(crc, 2))
        #print(hexi)
        hexi = hexi[2:]
        #msg+='0'
        count = str(cnt)
        counter = hex(int(count))[2:]
        #print(str(counter) + " Counter ")
        msg1 =frame + counter  + msg + hexi
        #print(msg1)
        print("CAWCAWCAW " +str(msg1))
        print('.............' + str(cnt) + '.............') 
        sent = sock.sendto(msg1.encode(), server_address)
        ts1 = time.time()
        print('package sent at: ' + str(ts1) + 'us') 
        data, server = sock.recvfrom(1024) 
        ts2 = time.time()
        #print(str(data)+" This is data")
        date = str(data)[2:len(data)+2]
        #print(str(date) + " CAW")
        CRCdata = getCRC(data,div)
        while CRCdata != [0,0,0,0]:
        #while date != msg1:
            sent = sock.sendto(msg1.encode(), server_address)
            data, server = sock.recvfrom(1024) 
            ts2 = time.time()
            date = str(data)[2:len(data)+2]
            CRCdata = getCRC(data,div)
            attempts+=1
        print('package recevied at: ' + str(ts2) + 'us')
        latency[cnt] = ts2-ts1
        countForPlot[cnt] = cnt+1
        dropAVG[cnt] = 1 - (cnt+1)/attempts
        cnt += 1
print("Total sent packets = " + str(cnt))
print("Total attempts = " + str(attempts))
plt.plot(countForPlot,latency)
plt.ylabel('Latency')
plt.xlabel('Packets')
plt.grid(True)
plt.show()
sock.close()
plt.plot(countForPlot,dropAVG)
plt.ylabel('Drop rate')
plt.xlabel('Packets')
plt.grid(True)
plt.show()
sock.close()
print('socket closed')