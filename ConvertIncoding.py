import codecs
from os import listdir
from os.path import isfile, join


def encodeFile(file):
    try:
        s = open(file, mode = 'r', encoding = 'UTF8').read()
        open(file, mode = 'w', encoding = 'ANSI').write(str(s))
    except Exception as ex:
        print(ex)

def encodeFileInDir(dirPath):
    for file in listdir(dirPath): # 경로지정
        path = join(dirPath, file)
        if isfile(path) and '.csv' in file: # 파일 여부
            encodeFile(path)


if __name__ == "__main__":
    name = "충청북도"
    dirPath = f"D:\부동산\아파트목록-20220131T094410Z-001\아파트목록\{name}"    # utf8 -> ANSI 변환할 dir path    
    encodeFileInDir(dirPath)
    print("Convertion Complete!!")