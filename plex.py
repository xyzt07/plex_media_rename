#!/usr/bin/python3
import os
# import pathlib
# import mimetypes
import re
# import json
# import urllib
import shutil
import filetype


def loopDir(dir):
    fileArray = []
    for s in os.listdir(dir):
        p = os.path.join(dir, s)

        # print(s)
        if os.path.isfile(p):

            fileArray.append(s)

            # # 若只是要返回文件文，使用这个

            # Filelist.append(os.path.basename(dir))

        elif os.path.isdir(p):

            files = loopDir(p)
            fileArray.append({s: files})

    return fileArray


def getFileMimeType(file):

    kind=filetype.guess(file)
    if kind is None:
        print('Cannot guess file type!')
        return None
    print(file,kind.mime,'mime')
    return kind.mime
    # type = mimetypes.guess_type(file)[0]
    # return type


# def safeFileName(file_path, file_name):
#     path = pathlib.Path("path/file")
#     if(path.is_file()):
#         if(file_name.find('#') != -1):
#             new_file = file_name.replace("#", "No-")
#             if(os.rename(file_path + file_name, file_path + new_file)):
#                 return new_file
#             else:
#                 print('name error')
#                 # dd()

#         else:
#             return file_name


# def getFileName(file):
#     matchObj = re.match("/(.+\/)(.+)/", file)
#     if(matchObj):
#         print(matchObj.group(1)+(matchObj.group(2)))
#     return file


# def safeExecFile(file):
#     file = file.replace(' ', '\ ')
#     file = file.replace('!', '\!')
#     file = file.replace('[', '\[')
#     file = file.replace(']', '\]',)
#     file = file.replace("'", "\'")
#     file = file.replace("&", "\&")
#     file = file.replace("|", "\|")
#     file = file.replace("#", "\#")
#     file = file.replace("", "\\")
#     # // file = str_replace(",", "\,", file)
#     file = file.replace('(', '\(')
#     file = file.replace(')', '\)')
#     return file


def filterMedia(file, media_type):
    mime = getFileMimeType(file)
    if not mime:
        print(file,mime,'error mime')

    if(mime and media_type):
        return mime.startswith(media_type)

    return False


def checkVideo(file):
    # import re
    sp = re.compile(r'([sS][pP])|([oO][pP])|([eE][dD])\[?\s?([0-9]\d*)')
    # init
    ep = re.compile(r'\D+(\d+)\D*')
    # mep = ep.match(file)
    # rep = ep.sub(r'--s01e\1--',file,count=1)
    # print(sp.search(file),'sp')
    # print(mep,'ep')
    all_num = re.findall(r'(\d+)', file)
    print(all_num, 'ep')

    # print(mep.groups(),'ep')


# def getChmod(filepath):
#     return substr(base_convert(@fileperms(filepath),10,8),-4)


def getMediaInfo(file):
    file = safeExecFile(file)
    # // dd(file)
    # ob_start()
    fileobj = os.popen(
        "ffprobe -v quiet -show_format -show_streams -print_format json :file 2>&1").read()
    # info = ob_get_contents()
    # ob_end_clean()

    return fileobj


def setMedia(dir, files):
    # import copy
    # 判断存在媒体文件
    for i in files:
        if(isinstance(i, dict)):
            for j in i:
                file_tmp = []
                for m in i[j]:
                    
                    # print(m,'m')
                    if(isinstance(m, dict)):
                        #是目录
                        # print(m, 'm1')
                        # 判断二级目录存在Season
                        # for son_path in m:
                        #     if isSeasonPath(son_path):
                        #         print(son_path,'remve has son path')
                        #         i[j] = []
                        continue

                    else:
                        fp = os.path.join(os.path.join(dir, j), m)
                        
                       
                        # for x in i[j]:
                            
                            # if not isinstance(x, dict):
                        if filterMedia(fp, 'video') == True:
                            print(m,'add video')
                            file_tmp.append(m)
                        # else:
                        #     print(m,'not video')
                file_tmp.sort()
                i[j] = file_tmp

    return list(filter(filterDir, files))
    # return files

# 判断是否是剧集目录
def isSeasonPath(path):
    print(path)
    if path=='S01' or path=='S1' or path=='Season 01' or path=='Season1':
        return True
    return False

'''
@Author: Xy
@Date: 2021-07-06 14:15:18
@Description: 过滤处理文件夹
@param {*} oj
'''
def filterDir(oj):
    has = 0
    if(isinstance(oj, dict)):
        for i in oj:
            # print(oj[i],'i')

            if(len(oj[i]) > 0):
                return True
            else:
                return False
                # return False
    else:
        return False

    return has > 0

'''
@Author: Xy
@Date: 2021-07-06 14:14:48
@Description: 重命名文件 移动文件
@param {*} dir
@param {*} files
'''
def reMoveFile(dir, files):

    for i in files:
        # need_rename = False
        for j in i:
            print(j,'move floder')
            path = os.path.join(dir, j)
            new_path = os.path.join(path, 'Season 01')
            folder = os.path.exists(new_path)
            # print(i[j],'ij')
            floder_files = getFolderFiles(path)
            if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                
                os.makedirs(new_path)
                

                # need_rename = True
                # move 文件

                # for m in i[j]:

                #     print(m)
            nums = []
            for file in i[j]:
                print(file,'file')
                nums.append(getFolderNum(file))

                    # if not isinstance(m, dict):
                        # nums.append(getFolderNum(file))

            for m in range(0, len(nums[0])):
                file_index = array_column(nums, m)
                if checkIncrementalArr(file_index):
                    # To Do Rename
                    for fi in range(0, len(file_index)):
                        new_name = 'S01E'+file_index[fi]+'--'+i[j][fi]
                        checkAssMove(path,new_path,floder_files,i[j][fi],new_name)
                        shutil.move(os.path.join(path, i[j][fi]),  os.path.join(
                            new_path, new_name))
                        print(
                            'remove '+path+i[j][fi] + ' TO '+new_path+new_name)
                    print(file_index, 'file_index')
                    break
                else:
                    print('continue')
                    continue
        # if need_rename:



'''
@Author: Xy
@Date: 2021-07-06 10:21:34
@Description: 检查递增数组
@param {*} arr
'''
def checkIncrementalArr(arr):
    m = None
    for i in arr:
        if m:
            if (i <= m):
                return False
        else:
            m = i
    return True


'''
@Author: Xy
@Date: 2021-07-06 14:30:30
@Description: 获取文件夹中文件
@param {*} dir
'''
def getFolderFiles(dir):
    fileArray = []
    for s in os.listdir(dir):
        p = os.path.join(dir, s)

        # print(s)
        if os.path.isfile(p):

            fileArray.append(s)
    return fileArray


'''
@Author: Xy
@Date: 2021-07-06 10:21:54
@Description: 获取文件名中的数字
@param {*} file_name
'''
def getFolderNum(file_name):
    all_num = re.findall(r'(\d+)', file_name)
    return all_num


def formatPlexName(dir, files):
    n = []
    for f in files:
        all_num = re.findall(r'(\d+)', f)
        n.append(all_num)
    # print(n)
    for num in n:
        print(num, 'num')

    # return True


'''
@Author: Xy
@Date: 2021-07-06 09:47:18
@Description: 获取单列数据
@param {*} arr
@param {*} col
'''
def array_column(arr, col):
    col_arr = []
    for i in range(0, len(arr)):
        col_arr.append(arr[i][col])
    return col_arr

def checkAssMove(path,new_path,files,media_file,new_name):
    # dir_files = getFolderFiles(path)
    name = os.path.splitext(media_file)[0]
    new_file_name = os.path.splitext(new_name)[0]
    for df in files:
        if( df.startswith(name) and (df.endswith('.ass') or df.endswith('.ASS') or df.endswith('.ssa') or df.endswith('SSA'))):
            
            shutil.move(os.path.join(path,df),  os.path.join(
                                new_path, new_file_name+os.path.splitext(df)[1]))
            


# dir = 'D:\ACGN\A'
dir = '/mnt/user/docunment-tmp/Transmission/anvideo'
# checkVideo(u'[VCB-Studio]\ Iya\ na\ Kao\ Sare\ Nagara\ Opantsu\ Misete\ Moraitai\ 2\ OP [01][Ma10p_1080p][x265_flac].mkv ')
all_files = loopDir(dir)
medias = setMedia(dir, all_files)
# print(medias)
reMoveFile(dir, medias)

# print(json.dumps(medias,ensure_ascii=False))
# print(json.dumps(medias,ensure_ascii=True))
# test()
