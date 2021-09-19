import os
# import numpy as np
# from scipy.interpolate import make_interp_spline
# import matplotlib.pyplot as plt 
# import matplotlib.axes.Axes as ax
from pathlib import Path

inputpath = "./data/music"
ouputpath = "./data_mods/test/music"

def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for tt in os.scandir(dir):
        if tt.is_dir():
            subfolders.append(tt.path)
        if tt.is_file():
            if os.path.splitext(tt.name)[1].lower() in ext:
                files.append(tt.path)


    for dir in list(subfolders):
        sf, tt = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(tt)
    return subfolders, files



# with open("0021_survali_ym_3e.vox","r") as vox:
#     # while True:
#     #     print(vox.read())
#     #     if vox.eof(): 
#     #         break
#     while True:
#         try:
#             s=vox.read()
#             print(s)
#         except EOFError:
#             break        
oldTsumamiSplitArrayLeft = []
oldTsumamiSplitArrayRight = []

def addVoxTenLeft(tsumamiString):
    tsumamiSplitArray = tsumamiString.split('\t');
    tsumamiSplitArray[-1] = tsumamiSplitArray[-1].replace('\n','')
    oldTsumamiSplitArrayLeft.append(tsumamiSplitArray)

def addVoxTenRight(tsumamiString):
    tsumamiSplitArray = tsumamiString.split('\t');
    tsumamiSplitArray[-1] = tsumamiSplitArray[-1].replace('\n','')
    oldTsumamiSplitArrayRight.append(tsumamiSplitArray)
    # for i in range(0,len(tsumamiSplitArray)-1):
    #     if i == 0:
    #         continue
    #     print(tsumamiSplitArray[i])
        
    #     if abs(int(tsumamiSplitArray[i][2]) - int(tsumamiSplitArray[i-1][2])) == 1:
    #         tsumamiSplitArray[i][2] = tsumamiSplitArray[i][2]
        
    # print(tsumamiSplitArray)
    
def processAsVoxTen():
    #print("\n\nProcessing Left\n\n")
    
    #print(oldTsumamiSplitArrayLeft)
    oldTsumamiSplitArrayLeft.pop(0)
    oldTsumamiSplitArrayRight.pop(0)
    
    if len(oldTsumamiSplitArrayLeft) == 0 or len(oldTsumamiSplitArrayRight) == 0:
        return
    if len(oldTsumamiSplitArrayLeft[0]) <= 7:
        oldTsumamiSplitArrayLeft[0].extend(['0','0']) 
    if len(oldTsumamiSplitArrayRight[0]) <= 7:        
        oldTsumamiSplitArrayRight[0].extend(['0','0']) 
    # print(len(oldTsumamiSplitArrayLeft))
    for i in range(0,len(oldTsumamiSplitArrayLeft)):
        # print(i)
        if i == 0:
            continue
        # print([i,i-1])
        # print(oldTsumamiSplitArrayLeft[i])
        # print(i)
        t = abs(int(oldTsumamiSplitArrayLeft[i][1]) - int(oldTsumamiSplitArrayLeft[i-1][1]))
        
        if t == 1 or t == 2:
            oldTsumamiSplitArrayLeft[i][1] = oldTsumamiSplitArrayLeft[i-1][1]
        t = int(oldTsumamiSplitArrayLeft[i][1])
        if t == 1:
            oldTsumamiSplitArrayLeft[i][1] = '0'
        if t == 31 or t == 30 or t == 33 or t == 34:
            oldTsumamiSplitArrayLeft[i][1] = '32'
        if t == 62 or t == 63 or t == 65 or t == 66:
            oldTsumamiSplitArrayLeft[i][1] = '64'
        if t == 94 or t == 95 or t == 97 or t == 98:
            oldTsumamiSplitArrayLeft[i][1] = '96'
        if t == 126 or t == 125:
            oldTsumamiSplitArrayLeft[i][1] = '127'
        if len(oldTsumamiSplitArrayLeft[i]) <= 7:
            oldTsumamiSplitArrayLeft[i].extend(['0','0']) 
        
    for i in range(0,len(oldTsumamiSplitArrayLeft)):
        
        if int(oldTsumamiSplitArrayLeft[i][1]) != 64:
            if int(oldTsumamiSplitArrayLeft[i][1]) != 127:
                position = int(oldTsumamiSplitArrayLeft[i][1])/128
            else:
                position = 1    
        else:
            position = 0.5
        # print([oldTsumamiSplitArrayLeft[i][1],position])
        oldTsumamiSplitArrayLeft[i][1] = "{:1.6f}".format(position)    
        # print(oldTsumamiSplitArrayLeft[i])
        # print(i)
    # timeArr = []
    # test = []
    # for i in oldTsumamiSplitArrayLeft:
    #     # print(i)
    #     timestrArr = i[0].split(',')
    #     currentTimePoint = float(timestrArr[0])+(float(timestrArr[1])-1)*0.25+float(timestrArr[2])/192
    #     test.append(float(i[1]))
    #     timeArr.append(currentTimePoint)
    # firstDifferences = False
    # previousIsChokaku = False
    # previousIsChokaku2 = False
    # skipPass = False
    # skipPass1 = False
    # potentialCurve = 0
    # for i in range(0,len(oldTsumamiSplitArrayLeft)):
          
    # print("\n\nProcessing Right\n\n")          
    for i in range(0,len(oldTsumamiSplitArrayRight)):
        # print(i)
        if i == 0:
            continue
        # print(oldTsumamiSplitArray[i][1])
        # print(oldTsumamiSplitArray[i-1][1])
        t = abs(int(oldTsumamiSplitArrayRight[i][1]) - int(oldTsumamiSplitArrayRight[i-1][1]))
        if t == 1 or t == 2:
            oldTsumamiSplitArrayRight[i][1] = oldTsumamiSplitArrayRight[i-1][1]

        t = int(oldTsumamiSplitArrayRight[i][1])
        if t == 1:
            oldTsumamiSplitArrayRight[i][1] = '0'
        if t == 62 or t == 63 or t == 65 or t == 66:
            oldTsumamiSplitArrayRight[i][1] = '64'
        if t == 126 or t == 125:
            oldTsumamiSplitArrayRight[i][1] = '127'
        
        
        if len(oldTsumamiSplitArrayRight[i]) <= 7:        
            oldTsumamiSplitArrayRight[i].extend(['0','0'])  
        # oldTsumamiSplitArrayRight[i].extend(['0','0'])
        
    for i in range(0,len(oldTsumamiSplitArrayRight)):
        # if int(oldTsumamiSplitArrayRight[i][1]) != 64:
        #     position = int(oldTsumamiSplitArrayRight[i][1])/127
        # else:
        #     position = 0.5
            
        if int(oldTsumamiSplitArrayRight[i][1]) != 64:
            if int(oldTsumamiSplitArrayRight[i][1]) != 127:
                position = int(oldTsumamiSplitArrayRight[i][1])/128
            else:
                position = 1    
        else:
            position = 0.5
        # print([oldTsumamiSplitArrayRight[i][1],position])
        
        oldTsumamiSplitArrayRight[i][1] = "{:1.6f}".format(position)  
        # print(oldTsumamiSplitArrayRight[i])  
    #print(oldTsumamiSplitArrayLeft)
      
        
        
        


def mainProcessing(filename):
    # f = open("0809_endroll_uno_dwatt_3e.vox", "r")
    # a = open("0809_endroll_uno_dwatt_3e_new.vox","w+")

    # f = open("0366_bangin_burst_kameria_4i.vox", "r")
    # a = open("0366_bangin_burst_kameria_4i_new.vox","w+")

    f = open(filename, "r",encoding='shift_jisx0213')
    ll = filename.split('/')
    if len(ll) < 5:
        f.close()
        return
    # print(ll)
    



    # c = f.readline()
    # print(c)
    processflagLeft = False
    processflagRight = False
    passflag = False
    readVersionFlag = False
    is12Flag = False
    while (c := f.readline()):
        if "#FORMAT" in c:
            readVersionFlag = True
        if "#TRACK1" in c:
            # print("track 1 get")
            processflagLeft = True
            processflagRight = False
            # a.write(c)
            # passflag = False
        if "#TRACK8" in c:
            processflagLeft = False
            processflagRight = True
            # passflag = False
            # a.write(c)
            # print("track 8 get")
        # if "#" in c:
            # print(c)
            # passflag = True
        
        if "#END" in c:
            # passflag = True
            processflagLeft = False
            processflagRight = False
            readVersionFlag = False
            
        
        if processflagLeft:
            addVoxTenLeft(c)
        elif processflagRight:
            addVoxTenRight(c)
        elif readVersionFlag:
            if '12' in c:
                is12Flag = True
        elif is12Flag:
            break
        # else:
            # a.write(c)
            
            
            
    
    # a.seek(0)
    f.seek(0)
    if not is12Flag:
        processAsVoxTen()
        Path("data_mods/test/music/"+ll[3]).mkdir(parents=True,exist_ok=True)
        a = open("data_mods/test/music/"+filename[13:],"w+")
        # contents = a.readlines()
        # location_of_lineA = 0
        # location_of_lineB = 0
        # for index, line in enumerate(contents):
        #     if line.startswith('#TRACK1'):
        #         location_of_lineA = index
        #     if line.startswith('#TRACK8'):
        #         location_of_lineB = index
        # print(location_of_lineA)
        # print(location_of_lineB)
        # print(a.tell())
        # a.close()
        # a = open("0021_survali_ym_3e_new.vox","a+")
        printLFlag = False
        printRFlag = False
        noPrintFlag = False
        printFormatFlag = False
        while (c := f.readline()):
            # print("\nTHISLINE\n"+c)
            if "#TRACK1" in c:
                printLFlag = True
                noPrintFlag = True
            if "#TRACK8" in c:
                printRFlag = True
                noPrintFlag = True
            if "#FORMAT" in c:
                # print("?")
                printFormatFlag = True
                noPrintFlag = True
            if "#END" in c:
                printLFlag = False
                printRFlag = False
                printFormatFlag = False
                noPrintFlag = False
            
            if printFormatFlag:
                a.write("#FORMAT VERSION\n")
                a.write("12\n")
                printFormatFlag = False
            elif printLFlag:
                a.write("#TRACK1\n")
                for i in oldTsumamiSplitArrayLeft:
                    for j in i:
                        a.write(j)
                        a.write('\t')
                    a.write('\n')
                printLFlag = False
            elif printRFlag:
                a.write("#TRACK8\n")
                for i in oldTsumamiSplitArrayRight : 
                    for j in i:
                        a.write(j)
                        a.write('\t')
                    a.write('\n')
                printRFlag = False
            elif noPrintFlag:
                # print(c)
                pp = 1
            else:
                a.write(c)
            # print(a.tell())    
            #print(c)

        f.close()
        a.close()
    else:
        print("Find FORMAT 12   SKIPPED")

if __name__ == "__main__":
    subfolders, files = run_fast_scandir(inputpath, [".vox"])
    # print(files)
    for i in files:
        print('Process' + i)
        mainProcessing(i)
        oldTsumamiSplitArrayLeft = []
        oldTsumamiSplitArrayRight = []