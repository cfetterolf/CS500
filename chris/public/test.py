def mystery2(num1, num2):
    return [num2]*num1

def mystery3(a_list):
    for i in range(len(a_list) // 2):
        other_index = len(a_list)-i-1
        temp = a_list[i]
        a_list[i] = a_list[other_index]
        a_list[other_index] = temp
    return a_list

print("hello world")

print(mystery2(6,3))
print(mystery3([1,2,3,4,5]))
