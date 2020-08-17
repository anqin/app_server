from PIL import Image
from os import listdir
'''
result_path_target  图片存放目标路径
cut_pictures 待拼接图片存放路径
num 图片命名以数字按序增加

'''

cut_pictures = r'D:\pesonal\QA\专利\all'
result_path_target = r'D:\pesonal\QA\专利\all\temp'
num = 1

ims = [Image.open(cut_pictures+'\\'+fn)for fn in listdir(cut_pictures)  if fn.endswith(".jpg")]       #  打开路径下的所有图片
width,height = ims[0].size  #获取拼接图片的宽和高
print(ims)
result = Image.new(ims[0].mode,(width,height*len(ims)))
for j , im in enumerate(ims):
    result.paste(im,box=(0,j*height))
    print(j)
result.save(result_path_target+'\\'+'%s.jpg'%num)
