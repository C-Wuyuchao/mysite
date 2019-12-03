from django.test import TestCase

# # 冒泡排序
#
# list_sort = [31, 4, 5, 24, 35, 13]
#
# def bubble_sort(list_sort):
#     n = len(list_sort)
#     for i in range(n):
#         for j in range(1, n-i):
#             print(list_sort[j])
#             if list_sort[j-1] > list_sort[j]:
#                 temp = list_sort[j-1]
#                 list_sort[j-1] = list_sort[j]
#                 list_sort[j] = temp
#
#     return list_sort
#
#
# # 选择排序
#
# def select_sort(list_sort):
#     n = len(list_sort)
#     for i in range(n):
#         min = i
#         for j in range(i+1, n):
#             if list_sort[min] > list_sort[j]:
#                 min = j
#         temp = list_sort[min]
#         list_sort[min] = list_sort[i]
#         list_sort[i] = temp
#     return list_sort
#
# print(select_sort(list_sort))

# python创建二叉树
# class TreeNode(object):
#     def __init__(self, data=None, left=None, right=None):
#         self.data = data
#         self.left = left
#         self.right = right
#
#     def __str__(self):
#         return str(self.data)
#
#
#
# A, B, C, D, E, F, G, H, I = [TreeNode(x) for x in 'ABCDEFGHI']
# A.left, A.right = B, C
# B.right = D
# C.left, C.right = E, F
# E.left = G
# F.left, F.right = H, I
# print(F.right)
# # 得到二叉树深度
# def TreeDepth(TreeNode):
#     if TreeNode is None:
#         return 0
#     count = max(TreeDepth(TreeNode.left), TreeDepth(TreeNode.right)) + 1
#     return count
# print(TreeDepth(A))

# x = [x ** 3 for x in range(5)]
# print(x)
# # 生成器
# x = (x ** 3 for x in range(5))
# while True:
#     try:
#         print(x.__next__())
#     except StopIteration as e:
#         print('Done', e.value)
#         break



