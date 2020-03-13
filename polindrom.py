import math

# def isPolindrom(N): 
#     if N >=0 and N < 10 :
#         return True  
#     t = True
#     count = 0 
#     temp = N
#     while N > 0 :
#         N //= 10
#         count += 1
#     while temp > 0 :
#         first = temp // ( 10 ** ( count - 1 ))
#         last=temp%10
#         if first != last:   
#             t=False
#             break
#         temp=(temp-(first*(10**(count-1))) ) //10
#         count-=2   
#     return t
        
# print(isPolindrom(4))


def isPolindrom(N): 
    
    if N >=0 and N < 10 :
        return True  
    t = True
    
    while N > 0 :
        
        first = N // 10 ** (int(math.log(N, 10) ) )
        last=N%10
        
        if first != last:   
            t=False
            break
        
        N = (N-(first*(10**( (int(math.log(N, 10) ) ) ) ) ) ) // 10 
         
    return t

print(isPolindrom(1591))
