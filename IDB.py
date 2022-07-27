import random
import socket
import SM3

HOST = 'localhost'
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
k2=11
k3=7
d = 5
Pubk = T_mul(d, G)
ID='1234567812345678'
ZZ=str(len(ID))+ID+str(a)+str(b)+str(G[0])+str(G[1])+str(Pubk[0])+str(Pubk[1])
Za=SM3.SM3_test(ZZ)


def Sign(P1,Q1,e):
    global n,G,d,p,k2,k3
    P_=T_mul(gcd(d,n),P1)
    G_=G
    G_[1]= p - G_[1]
    P=T_add(P_,G_)
    Q2=T_mul(k2,G)
    R=T_add(T_mul(k3,Q1),Q2)
    r=(R[0]+e)%n
    s2=(d*k3)%n
    s3=(d*(r+k2))%n
    return r,s2,s3


    
bb=[]
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
for i in range(6):
    if i == 5:
        break
    s.sendall('1'.encode('UTF-8'))
    data = s.recv(512)
    bb.append(data.decode('utf-8'))

P1=[]
P1.append(int(bb[0]))
P1.append(int(bb[1]))
Q1=[]
Q1.append(int(bb[2]))
Q1.append(int(bb[3]))
e=int(bb[4])
r,s2,s3=Sign(P1,Q1,e)
aa=[]
b=0
aa.append(str(r))
aa.append(str(s2))
aa.append(str(s3))
for i in range(4):
    data = s.recv(512)
    if i == 3:
        s.sendall('0'.encode('UTF-8'))
        break
    s.sendall(aa[b].encode('UTF-8'))
    b += 1
s.close()














