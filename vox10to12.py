import os

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
    
    
def processAsVoxTen():
    #print("\n\nProcessing Left\n\n")
    
    oldTsumamiSplitArrayLeft.pop(0)
    oldTsumamiSplitArrayRight.pop(0)
    
    if len(oldTsumamiSplitArrayLeft) == 0 or len(oldTsumamiSplitArrayRight) == 0:
        return
    if len(oldTsumamiSplitArrayLeft[0]) <= 7:
        oldTsumamiSplitArrayLeft[0].extend(['0','0']) 
    if len(oldTsumamiSplitArrayRight[0]) <= 7:        
        oldTsumamiSplitArrayRight[0].extend(['0','0']) 
    
    for i in range(0,len(oldTsumamiSplitArrayLeft)):
        if i == 0:
            continue
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
        
        oldTsumamiSplitArrayLeft[i][1] = "{:1.6f}".format(position)    
        
    for i in range(0,len(oldTsumamiSplitArrayRight)):
        if i == 0:
            continue
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
        
    for i in range(0,len(oldTsumamiSplitArrayRight)):
        if int(oldTsumamiSplitArrayRight[i][1]) != 64:
            if int(oldTsumamiSplitArrayRight[i][1]) != 127:
                position = int(oldTsumamiSplitArrayRight[i][1])/128
            else:
                position = 1    
        else:
            position = 0.5
        
        oldTsumamiSplitArrayRight[i][1] = "{:1.6f}".format(position) 
        
        
        


def mainProcessing(filename):

    f = open(filename, "r",encoding='shift_jisx0213')
    ll = filename.split('/')
    if len(ll) < 5:
        f.close()
        return
    
    processflagLeft = False
    processflagRight = False
    passflag = False
    readVersionFlag = False
    is12Flag = False
    while (c := f.readline()):
        if "#FORMAT" in c:
            readVersionFlag = True
        if "#TRACK1" in c:
            processflagLeft = True
            processflagRight = False
        if "#TRACK8" in c:
            processflagLeft = False
            processflagRight = True
        
        if "#END" in c:
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

    f.seek(0)
    if not is12Flag:
        processAsVoxTen()
        Path("data_mods/test/music/"+ll[3]).mkdir(parents=True,exist_ok=True)
        a = open("data_mods/test/music/"+filename[13:],"w+")
        printLFlag = False
        printRFlag = False
        noPrintFlag = False
        printFormatFlag = False
        while (c := f.readline()):
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
                pp = 1
            else:
                a.write(c)
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
