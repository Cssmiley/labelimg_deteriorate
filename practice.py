
def rotateRight(arr):
    A = arr[::-1] #利用切片上下翻轉
    return list(map(list,(zip(*A)))) #行列互換，再利用map函數將zip內的元組轉列表


arr =[
  [1,2,3],
  [4,5,6,7],
]

print(rotateRight(arr))
