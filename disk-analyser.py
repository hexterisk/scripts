#!/usr/bin/python3
# coding=utf-8
from sys import argv

endian="little"

def printer(initPoint,data):
    dataHex=""
    for i,j in enumerate(data):
        if not i%16:dataHex+=(hex(i+initPoint)+': ').zfill(8)
        dataHex+=(hex(ord(j))[2:].zfill(2)+' ')
        if i%16==15:dataHex+='\n'
    return dataHex

def fixHSC(hscData):
        
    if endian=="little":
        h=hscData[0]
        s=hscData[1]
        c=hscData[2]
    else:
        h=hscData[2]
        s=hscData[1]
        c=hscData[0]
    if hscData=='\xfe\xff\xff':return hex(ord(c))[2:].zfill(2),hex(ord(h))[2:].zfill(2),hex(ord(s))[2:].zfill(2)
    
    h=ord(h)
    binS=bin(ord(s))[2:].zfill(8)
    s=int(binS[2:],2)
    c=binS[:2]+bin(ord(c))[2:].zfill(8)
    c=int(c,2)
    return hex(c)[2:].zfill(2),hex(h)[2:].zfill(2),hex(s)[2:].zfill(2)

def parsePartitionTable(data):
    sp=446
    tables=[data[i:i+16] for i in range(0,64,16)]
    
    for i,j in enumerate(tables):
        print("-----------------------Partition {}-----------------------".format(i+1))
        pos=(sp+(i*16))
        print("Boot Indicator             : "+printer(pos,j[0:1]))
        pos+=1
        print("Starting Sector(HSC Value) : "+printer(pos,j[1:4]))
        C,H,S=fixHSC(j[1:4])
        print("Starting Sector(CHS Value) : "+"{}: {} {} {}".format(hex(pos).zfill(6),C,H,S))
        pos+=3
        print("Partition Type Descriptor  : "+printer(pos,j[4:5]))
        pos+=1
        print("Ending Sector(HSC Value)   : "+printer(pos,j[5:8]))
        C,H,S=fixHSC(j[5:8])
        print("Ending Sector(CHS Value)   : "+"{}: {} {} {}".format(hex(pos).zfill(6),C,H,S))
        pos+=3
        print("Starting Sector(LBA Value) : "+printer(pos,j[8:12]))
        pos+=4
        print("Partition Size(in sectors) : "+printer(pos,j[12:16]))
        pos+=4

def mbr(hdData,Endian):
    global endian
    endian=Endian
    print("Assuming {} endian".format(endian))
    uniqueDiskID=hdData[436:446]
    codeSection=hdData[0:440]
    diskSignature=hdData[440:444]
    genNull=hdData[444:446]
    primaryPartitionTable=hdData[446:510]
    mbrSignature=hdData[510:512]
    
    print("-----------------Unique Disk ID(optional)----------------")
    print(printer(436,uniqueDiskID))
    print("--------------------Start Code Section--------------------")
    print(printer(0,codeSection))
    print("----------------------Disk Signature----------------------")
    print(printer(440,diskSignature))
    print("-----------------------Null Section-----------------------")
    print(printer(444,genNull))
    print("------------------Primary Partition Table-----------------")
    print(printer(446,primaryPartitionTable))
    print("-----------------------MBR Signature----------------------")
    print(printer(510,mbrSignature))

    parsePartitionTable(primaryPartitionTable)

def bootSector(hdData,Endian):
    global endian
    endian=Endian
    print("Assuming {} endian".format(endian))
    spacePadValue=50
    dashSize=90
    i=0
    print("-"*dashSize)
    print("JMP Instruction(0xEB5290)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+3]))
    print("-"*dashSize)
    i+=3
    print("OEM ID(NTFS[space]*4)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+8]))
    print("-"*dashSize)
    i+=8
    print("Bytes Per Sector(0x0200)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+2]))
    print("-"*dashSize)
    i+=2
    print("Sectors Per Clustor(0x08)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+1]))
    print("-"*dashSize)
    i+=1
    print("Reserved Sectors(0x0000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+2]))
    print("-"*dashSize)
    i+=2
    print("Unused(0x000000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+3]))
    print("-"*dashSize)
    i+=3
    print("Unused by NTFS(0x0000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+2]))
    print("-"*dashSize)
    i+=2
    print("Media Descriptor(0xF8)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+1]))
    print("-"*dashSize)
    i+=1
    print("Unused(0x0000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+2]))
    print("-"*dashSize)
    i+=2
    print("Sectors per Track(0x003F)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+2]))
    print("-"*dashSize)
    i+=2
    print("Number Of Heads(0x00FF)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+2]))
    print("-"*dashSize)
    i+=2
    print("Hidden Sector(0x0000003F)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+4]))
    print("-"*dashSize)
    i+=4
    print("Unused(0x00000000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+4]))
    print("-"*dashSize)
    i+=4
    print("Unused(0x00800080)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+4]))
    print("-"*dashSize)
    i+=4
    print("Total Sectors(0x00000000007FF54A)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+8]))
    print("-"*dashSize)
    i+=8
    print("MFT Cluster Number(0x0000000000000004)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+8]))
    print("-"*dashSize)
    i+=8
    print("MFT Mirror Cluster Number(0x000000000007FF54)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+8]))
    print("-"*dashSize)
    i+=8
    print("Cluster Per File Record Segment(0xF6)".ljust(spacePadValue)+" : " +printer(i,hdData[i:i+1]))
    print("-"*dashSize)
    i+=1
    print("Unused(0x000000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+3]))
    print("-"*dashSize)
    i+=3
    print("Cluster Per Index Buffer(0x01)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+1]))
    print("-"*dashSize)
    i+=1
    print("Unused(0x000000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+3]))
    print("-"*dashSize)
    i+=3
    print("Volume Serial Number(0x1C741BC9741BA514)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+8]))
    print("-"*dashSize)
    i+=8
    print("checksumUnused(0x00000000)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+4]))
    print("-"*dashSize)
    i+=4
    print("Bootstrap Code:\n"+printer(i,hdData[i:i+426]))
    print("-"*dashSize)
    i+=426
    print("End Of Sector Marker(0xAA55)".ljust(spacePadValue)+" : " + printer(i,hdData[i:i+2]))
    print("-"*dashSize)
    i+=2

if __name__ == "__main__":

    if len(argv) > 1:
        fname=argv[1].strip()
        mode=1 #1 for MBR and 2 for NTFS
        Endian="little"
        if len(argv)>3:Endian=argv[3].strip()
        if len(argv)>2:mode=int(argv[2].strip())
        hdData=open(fname.strip(),'r').read()
        if mode == 1:mbr(hdData,Endian)
        if mode == 2:bootSector(hdData,Endian)
    else:
        print("Usage for MBR sector: python {} filename".format(argv[0]))
        print("Usage for NTFS boot sector: python {} filename".format(argv[0]))
