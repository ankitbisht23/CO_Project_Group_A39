import sys
def binaryconvert(a):
    b=str(bin(int(a)))
    no='0'*(10-len(b))+b[2:]
    return no
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
    num=pow+mentisa
    return num
    
dict_instruction={ 
    'sub': '10001','add': '10000','mov': ['10010', '10011'],    'ld' : '10100','st' : '10101','mul': '10110',
    'div': '10111','rs' : '11000','ls' : '11001','xor': '11010','or' : '11011','and': '11100','not': '11101',
    'cmp': '11110','jmp': '11111','je' : '01111','jlt': '01100','jgt': '01101','hlt': '01010' ,'movf':'00010',
    'addf':'00000','subf':'00001'
    }
dict_register = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100',
            'R5': '101','R6': '110','FLAGS': '111'}
Inputcode= []
for line in sys.stdin:
    Inputcode.append(list(map(str,line.split())))
emptyline=0
variables_No=0
variables=dict()
lables=dict()
errorlist=[]
output=[]
hlt_no=0
for line in Inputcode:
    if not line:
        emptyline+=1
for line in Inputcode:
    if line:
        if line[0]=='var':
            variables_No+=1
        else:
            break
    else: continue
codelength=len(Inputcode)-emptyline
variable_address=codelength-variables_No
line_no=0
hlt_present=False
hlt_line=dict()

for line in Inputcode:
    if not line: continue
    else:
        if line[0]=='var':
            line_no+=1
            if len(line)==2:
                if line[1] in variables: errorlist.append(f"Error in line {line_no}: Multiple Variable declaration ")
                else:
                    variables[line[1]]=binaryconvert(variable_address)
                    variable_address+=1
            else:
                errorlist.append(f"Error in line {line_no}: Variable declaration is wrong ")
        else: break
line_no=0
for line in Inputcode:
    if not line: continue
    else:
        line_no+=1
        if line[0][-1]==':':
            if line[0][:-1] in lables: errorlist.append(f"Error in line {line_no}: Multiple labels declaration ")
            else:
               lables[line[0][:-1]]=binaryconvert(line_no-variables_No-1)
                
line_no=0
for line in Inputcode:
    if not line: continue
    else:
        line_no+=1 
        if line[0][:-1] in lables:
            line.pop(0)
            
        if not line: 
            errorlist.append(f"Error in line {line_no}: Wrong syntax")
            continue
        if line[0][-1]==':': errorlist.append(f"Error in line {line_no}: Multiple lables present")
        elif line[0] in ["add", "sub", "mul", "xor", "or", "and"] :
            if len(line)==4:
                if line[1] in dict_register and line[2] in dict_register and line[3] in dict_register:
                    if(line[1]!='FLAGS' and line[2]!='FLAGS' and line[3]!='FLAGS'):
                        lc=dict_instruction[line[0]]+"00"+dict_register[line[1]]+dict_register[line[2]]+dict_register[line[3]]
                        output.append(lc)
                    else: errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                else:
                    errorlist.append(f"Error in line {line_no}: Use of wrong register name")
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
        
        elif line[0] in [ "rs", "ls"]:
            if len(line)==3:
                if line[1] in dict_register:
                    if(line[1]!='FLAGS'):
                        if line[2][0]=="$":
                            try:
                                if '.' not in line[2][1:]:
                                    if int(line[2][1:])>255 or int(line[2][1:])<0:
                                        errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                                    else:
                                        lc=dict_instruction[line[0]]+dict_register[line[1]]+binaryconvert(line[2][1:])
                                        output.append(lc)
                                else: errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                            except:
                                errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                        else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
                    else: errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")    
                else: errorlist.append(f"Error in line {line_no}: Use of wrong register name")
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
 
        elif line[0] in [ "div", "not", "cmp"]:
            if len(line)==3:
                if line[1] in dict_register and line[2] in dict_register:
                    if(line[1]!='FLAGS' and line[2]!='FLAGS'):
                        lc=dict_instruction[line[0]]+"00000"+dict_register[line[1]]+dict_register[line[2]]
                        output.append(lc)
                    else: errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                else:
                    errorlist.append(f"Error in line {line_no}: Use of wrong register name")
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
            
        elif line[0] in ["ld", "st"]:
            if len(line)==3:
                if line[1] in dict_register:
                    if(line[1]!='FLAGS'):
                        if line[2] in variables:
                            lc=dict_instruction[line[0]]+dict_register[line[1]]+variables[line[2]]
                            output.append(lc)
                        else: errorlist.append(f"Error in line {line_no}: Variable not defined")
                    else: errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                else: errorlist.append(f"Error in line {line_no}: Use of wrong register name")
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
            
        elif line[0] in ["jmp", "jlt", "jgt", "je"]:
            if len(line)==2:
                if line[1] in lables:                   
                    lc=dict_instruction[line[0]]+"000"+lables[line[1]]
                    output.append(lc)
                else: errorlist.append(f"Error in line {line_no}: Label not defined")    
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
        elif line[0]=='mov':
            if len(line)==3:
                if line[2] in dict_register:
                    if line[1]=="FLAGS": 
                        if line[2]=="FLAGS": errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                        else:
                            lc=dict_instruction[line[0]][1]+"00000"+dict_register[line[1]]+dict_register[line[2]]
                            output.append(lc)
                       
                    elif line[1] in dict_register:
                        if line[2]=="FLAGS": errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                        else:
                            lc=dict_instruction[line[0]][1]+"00000"+dict_register[line[1]]+dict_register[line[2]]
                            output.append(lc) 
                    else: errorlist.append(f"Error in line {line_no}: Wrong register name")
                elif line[2][0]=="$":
                    try:
                        if '.' not in line[2][1:]:
                            if int(line[2][1:])>255 or int(line[2][1:])<0:
                                    errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                            else:
                                if line[1]=="FLAGS": errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                                elif line[1] in dict_register:
                                    lc=dict_instruction[line[0]][0]+dict_register[line[1]]+binaryconvert(line[2][1:])
                                    output.append(lc) 
                                else: errorlist.append(f"Error in line {line_no}: Wrong register name")
                        else: errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                    except:
                        errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                else: errorlist.append(f"Error in line {line_no}: Use of wrong register name")   
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")

        elif line[0]=='movf':
            if len(line)==3:
                if line[1] in dict_register:
                    if line[1]!="FLAGS":
                        if line[2][0]=='$':
                            if '.' in line[2][1:]:
                                try:
                                    no=float(line[2][1:])
                                    if no>252 or no<1:
                                            errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                                    else:     
                                        lc=dict_instruction[line[0]]+""+dict_register[line[1]]+""+floatTobinaryconvert(line[2][1:])
                                        output.append(lc)           
                                except:
                                    errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                            else: errorlist.append(f"Error in line {line_no}: Illegal Immediate value")
                        else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
                    else: errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                else: errorlist.append(f"Error in line {line_no}: Use of wrong register name")   
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")

        elif line[0] in ["addf", "subf"] :
            if len(line)==4:
                if line[1] in dict_register and line[2] in dict_register and line[3] in dict_register:
                    if(line[1]!='FLAGS' and line[2]!='FLAGS' and line[3]!='FLAGS'):
                        lc=dict_instruction[line[0]]+"00"+dict_register[line[1]]+""+dict_register[line[2]]+""+dict_register[line[3]]
                        output.append(lc)
                    else: errorlist.append(f"Error in line {line_no}: Illegal use of FLAGS registers")
                else:
                    errorlist.append(f"Error in line {line_no}: Use of wrong register name")
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")


        elif line[0]=="hlt":
            if len(line)==1:
                hlt_no+=1
                hlt_line[hlt_no]=line_no
                if(codelength==line_no):
                    hlt_present=True
                    output.append("0101000000000000")

                else:errorlist.append(f"Error in line {line_no}: hlt not being used as the last instruction")
            else: errorlist.append(f"Error in line {line_no}: Wrong syntax")
        elif line[0]=='var' and line_no>variables_No:
            errorlist.append(f"Error in line {line_no}: Variable not declared in beginning")
        elif line_no>variables_No: errorlist.append(f"Error in line {line_no}: Wrong instruction")
        
if not hlt_present:
    errorlist.append(f"Error in line {codelength}: hlt not present")
if hlt_no>1:
    errorlist.append(f"Error in line {hlt_line[1]}: multiple hlt present")
    
if errorlist:   
    for i in errorlist:
            print(i)
else:
    for l in output:
            print(l)
