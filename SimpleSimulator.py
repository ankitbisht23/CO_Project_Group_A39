import sys

def DecimalTobin(n):
    num=''
    if '.' in n:
        w,d=n.split('.')
        d='0.'+d
        d=float(d)
    else:
        w=n
        d=0
    w=int(w)
    if(w==0):
        num='0'
    while w!=0:
        r=w%2
        j=str(r)
        w=w//2
        num+=j
    num=num[::-1]
    if '.' not in n:
        return num
    flno='.'
    for j in range(5):
        r=d*2
        x=int(r)
        if x>1:
            break
        j=str(x)
        flno+=j
        d=r-x
    num+=flno
    return num
def floatTobinaryconvert(a):
    no=DecimalTobin(a)
    pow=0
    if '.' in no:
        pow=no.index('.')-1
    else:
        pow=len(no)-1
    pow=str(pow)
    
    pow=DecimalTobin(pow)
    while(len(pow)!=3):
        pow='0'+pow
    no=no.replace('.','',1)
    mentisa=''
    if(len(no)<6):
        mentisa=no[1:]
        while(len(mentisa)!=5):
            mentisa+='0'
    else:
        mentisa=no[1:6]
    num=8*'0'+pow+mentisa
    return num

def binToDecimal(n):
    num=0
    if '.' in n:
        w,d=n.split('.')
        c=len(w)-1
    else:
        c=len(n)-1
    for i in n:
        if i=='.':
            continue
        j=int(i)
        num+=j*2**c
        c-=1
    num=str(num)
    return num
def binToFloat(a):
    no='1'+a[3:]
    pow=int(a[:3],2)
    no=no[:pow+1]+'.'+no[pow+1:]
    b=binToDecimal(no)
    
    return float(b)
    
def checkoverflow(a):
    if(float(a)>(2**16-1)or float(a)<0):
        return True
    return False

def inttobinary(a,l):
    b=bin(a)[2:]
    b='0'*(l-len(b))+b
    return b

def resetflag():
    return '0000000000000000'

def execute(inst,pc):
    opcode=inst[:5]
    if(opcode=="00000"):
        #addf r1 r2 r3
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16] 
        if((binToFloat(reg[b])+binToFloat(reg[c]))>252):
            reg[a]=='0'*16
            reg["111"]='0000000000001000'
        else:
            reg[a]=floatTobinaryconvert(binToFloat(reg[b])+binToFloat(reg[c]))
            reg['111']=resetflag()
        pc+=1
    if(opcode=="00001"):
        #subf r r r
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16]
        if((binToFloat(reg[b])-binToFloat(reg[c]))<1):
            reg[a]=='0'*16
            reg["111"]='0000000000001000'
        else:
            reg[a]=floatTobinaryconvert(binToFloat(reg[b])-binToFloat(reg[c]))
            reg['111']=resetflag()
        pc+=1
    if(opcode=="00010"):
        # movf r $
        a=inst[5:8]
        b=inst[8:16]
        reg[a]='0'*8+b
        pc+=1
        reg['111']=resetflag()
    if(opcode=="10000"):
        #add r1 r2 r3
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16]
        y=int(reg[b],2)+int(reg[c],2)
        if(checkoverflow(y)):
            y=y%2**16
            reg[a]=inttobinary(y,16)
            reg["111"]='0000000000001000'
        else:
            reg[a]=inttobinary(y,16)
            reg['111']=resetflag()
        pc+=1
        
    if(opcode=="10001"):
        #sub r r r
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16]
        y=int(reg[b],2)-int(reg[c],2)
        if(checkoverflow(y)):
            y=0
            reg[a]=inttobinary(y,16)
            reg["111"]='0000000000001000'
        else:
            reg[a]=inttobinary(y,16)
            reg['111']=resetflag()
        pc+=1
    if(opcode=="10110"):
        # mul r r r
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16]
        y=int(reg[b],2)*int(reg[c],2)
        if(checkoverflow(y)):
            y=y%2**16
            reg[a]=inttobinary(y,16)
            reg["111"]='0000000000001000'
        else:
            reg[a]=inttobinary(y,16)
            reg['111']=resetflag()
        pc+=1
    if(opcode=="10111"):
        # div r r
        b=inst[10:13]
        c=inst[13:16]
        reg["000"]=inttobinary(int(reg[b],2)/int(reg[c],2),16)
        reg["001"]=inttobinary(int(reg[b],2)%int(reg[c],2),16)
        pc+=1
        reg['111']=resetflag()
    
    if(opcode=="11011"):
        # or r r r
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16]
        reg[a]=inttobinary(int(reg[b],2)|int(reg[c],2),16)
        pc+=1
        reg['111']=resetflag()
    if(opcode=="11100"):
        # and r r r
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16]
        reg[a]=inttobinary(int(reg[b],2)&int(reg[c],2),16)
        pc+=1
        reg['111']=resetflag()
    if(opcode=="11101"):
        # not r r
        b=inst[10:13]
        c=inst[13:16] 
        reg[c]=inttobinary(~int(reg[b],2),16)
        pc+=1
        reg['111']=resetflag()
    if(opcode=="11010"):
        # xor r r r
        a=inst[7:10]
        b=inst[10:13]
        c=inst[13:16]
        reg[c]=inttobinary(int(reg[b],2)^int(reg[c],2),16)
        pc+=1
        reg['111']=resetflag()
    if(opcode=="11000"):
        # rs r $
        a=inst[5:8]
        b=inst[8:16]
        reg[a]=inttobinary(int(reg[a],2)>>int(b,2),16)
        pc+=1
        reg['111']=resetflag()
    if(opcode=="11001"):
        # ls r $
        a=inst[5:8]
        b=inst[8:16]
        reg[a]=inttobinary(int(reg[a],2)<<int(b,2),16)
        pc+=1
        reg['111']=resetflag()
    if(opcode=="10010"):
        # mov r $
        a=inst[5:8]
        b=inst[8:16]
        reg[a]='0'*8+b
        pc+=1
        reg['111']=resetflag()
    if(opcode=="10011"):
        # mov r r
        a=inst[10:13]
        b=inst[13:16]
        reg[b]=inttobinary(int(reg[a],2),16)
        pc+=1
        reg['111']=resetflag()
    if(opcode=="10100"):
        # ld r mem
        a=inst[5:8]
        b=int(inst[8:16],2)
        reg[a]=mem[b]
        pc+=1
        reg['111']=resetflag()
    if(opcode=="10101"):
        # st r mem
        a=inst[5:8]
        b=int(inst[8:16],2)
        mem[b]=reg[a]
        pc+=1
        reg['111']=resetflag()
    if(opcode=="11110"):
        # cmp r r
        a=inst[10:13]
        b=inst[13:16]
        if(int(reg[a],2)==int(reg[b],2)):
            reg['111']='0000000000000001'
        if(int(reg[a],2)>int(reg[b],2)):
            reg['111']='0000000000000010'
        if(int(reg[a],2)<int(reg[b],2)):
            reg['111']='0000000000000100'
        pc+=1
    if(opcode=="11111"):
        # jmp mem
        a=inst[8:16]
        pc=int(a,2)
        reg['111']=resetflag()
    if(opcode=="01100"):
        # jlt mem
        a=inst[8:16]
        if(reg["111"][13]):
            pc=int(a,2)
        else:
            pc+=1
        reg['111']=resetflag()
    if(opcode=="01101"):
        # jgt mem
        a=inst[8:16]
        if(int(reg["111"][14])):
            pc=int(a,2)
        else:
            pc+=1
        reg['111']=resetflag()
    if(opcode=="01111"):
        # je mem
        a=inst[8:16]
        if(int(reg["111"][15])):
            pc=int(a,2)
        else:
            pc+=1
        reg['111']=resetflag()
    if(opcode=="01010"):
        # hlt
        pc+=1
        reg['111']=resetflag()

    
    if(opcode=="01010"):
        return True,pc
    else:
        return False,pc

reg={"000":'0000000000000000',"001":'0000000000000000',"010":'0000000000000000',"011":'0000000000000000',
    "100":'0000000000000000',"101":'0000000000000000',"110":'0000000000000000',"111":"0000000000000000"}
mem=[]

for line in sys.stdin:
    mem.append(line)
while(len(mem)<=255):
    mem.append('0000000000000000')
pc=0
new_pc=0
halt=False
while(not halt):
    Instruction=mem[pc]
    halt,new_pc=execute(Instruction,pc)
    print(inttobinary(pc,8),end=" ")
    for i in reg:
        print(reg[i],end=" ")
    print()
    pc=new_pc
for line in mem:
    print(line)
