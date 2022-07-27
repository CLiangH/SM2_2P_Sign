import random
import socket
import SM3

HOST = ''
PORT = 10888



    
def Coprime(a, b):
    while a != 0:
        a, b = b % a, a
    if b != 1 and b != -1:
        return 1
    return 0

def gcd(a, m):
    if Coprime(a, m):
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    if u1 > 0:
        return u1 % m
    else:
        return (u1 + m) % m

def T_add(P,Q):
    if (P == 0):
        return Q
    if (Q == 0):
        return P
    if P == Q:
        aaa=(3*pow(P[0],2) + a)
        bbb=gcd(2*P[1],p)
        k=(aaa*bbb)%p 
    else:
        aaa=(P[1]-Q[1])
        bbb=(P[0]-Q[0])
        k=(aaa*gcd(bbb,p))%p 

    Rx=(pow(k,2)-P[0] - Q[0]) %p
    Ry=(k*(P[0]-Rx) - P[1])%p
    R=[Rx,Ry]
    return R



def T_mul(n, l):
    if n == 0:
        return 0
    if n == 1:
        return l
    t = l
    while (n >= 2):
        t = T_add(t, l)
        n = n - 1
    return t

a = 2
b = 2       
p = 17 #椭圆曲线参数，y^2=x^3+2x+2
G = [5, 1]
n = 19
message='Satoshi'
e=hash(message)
k=2
d = 7
Pubk = T_mul(d, G)
ID='1234567812345678'
ZZ=str(len(ID))+ID+str(a)+str(b)+str(G[0])+str(G[1])+str(Pubk[0])+str(Pubk[1])
Za=SM3.SM3_test(ZZ)

def Sign1():
    global n,G,d
    P1=T_mul(gcd(d,n),G)
    return P1

def Sign3():
    global Za,message,k,G
    M_=Za+message
    e=hash(M_)
    Q1=T_mul(k,G)
    return Q1,e

def Sign5(r,s2,s3):
    s=((d*k)*s2+d*s3-r)%n
    if(s!=0 or s!=n-r):
        return r,s
    return 0,0

aa=[]
P1=Sign1()
Q1,e=Sign3()
aa.append(str(P1[0]))
aa.append(str(P1[1]))
aa.append(str(Q1[0]))
aa.append(str(Q1[1]))
aa.append(str(e))
i=-1
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
conn, addr = s.accept()
while True:
    i += 1
    data = conn.recv(2048)
    if data.decode('utf-8') == 0:
        break
    conn.send(aa[i].encode('UTF-8'))
    if i == 4:
        break


bb=[]

for i in range(4):
    conn.send('1'.encode('UTF-8'))
    data = conn.recv(2048)
    if data.decode('utf-8') == 0:
        break
    bb.append(data.decode('utf-8'))
conn.close()

r=int(bb[0])
s2=int(bb[1])
s3=int(bb[2])
r,s = Sign5(r,s2,s3)
print('签名消息为：',r,s)







