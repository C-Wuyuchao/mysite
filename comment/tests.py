from django.test import TestCase

# Create your tests here.
# 递归求和
def add(i):
    if i < 0:
        raise ValueError
    elif i <=1:
        return 1
    else:
        result = add(i-1) + i
        return result



# 斐波那契数列：就是前两个数的和为后一个数的值（0，1，1，2，3，5，8，13.........）

def foo(arg1, arg2, stop):
    if arg1 == 0:
        print(arg1, arg2)
    arg3 = arg1 + arg2
    print(arg1, arg2, arg3)
    if arg3 < stop:
        foo(arg2, arg3, stop)

# 利用切片递归方式，查找数据
def twosplit(sourceDate,findData):
    sp = int(len(sourceDate)/2)  #序列长度
    if sourceDate[0] == findData:
        print('找到数据:',sourceDate[0])
        return 0
    else:
        if findData in sourceDate[:sp]: #判断在左边
            print('数据在左边[%s]' %sourceDate[:sp])
            twosplit(sourceDate[:sp],findData)  #递归函数
        elif findData in sourceDate[sp:]: #判断在右边
            print('数据在右边[%s]' %sourceDate[sp:])
            twosplit(sourceDate[sp:], findData)
        else:
            print('找不到数据')

# if __name__ == '__main__':
#     data = [1,2,'c',3,4,5,6,7,8,17,26,15,14,13,12,11,'a','b']
#     #data = list(range(1000000))
#     twosplit(data,'c')
#
# print(int(5/2))
# print(5//2)
# a = [[col for col in range(4)] for row in range(4)]
# for i in a:print(i)   #打印二维数组
# print('--------------------')
# for lf,rig in enumerate(a):  #循环数组，打印数组下标和元素
#     for cf in range(lf,len(rig)):  #从下标数组开始循环到列表长度
#         tmp = a[cf][lf]      #存储列表元素中的元素
#         a[cf][lf] = rig[cf]
#         a[lf][cf] = tmp
#     print('+++++++++++++++++')
#     for i in a:print(i)

import threading  #线程模块
import time

# def sayhi(num):  #定义每个线程要运行的函数
#     print('running on number',num)
#     time.sleep(3)

# if __name__ == "__main__":
#     t1 = threading.Thread(target=sayhi,args=(33,)) #生成一个线程实例
#     t2 = threading.Thread(target=sayhi,args=(22,)) #生成另一个线程实例
#
#     t1.start()  #启动线程
#     t2.start()
#     print(t1.getName()) #获取线程名
#     print(t2.getName())
#     t1.join()  #阻塞主线程，等待t1子线程执行完后再执行后面的代码
#     t2.join()  #阻塞主线程，等待t2子线程执行完后再执行后面的代码
#     print('-----end')


class animal(object):

    def __init__(self):
        self.food = '肉'
        self.act = '叫'



class pig(animal):
    def __init__(self):
        super(pig, self).__init__()
        self.food = '猪肉'

pig = pig()
print(pig.act)


