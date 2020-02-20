class Stack :

    def __init__ (self):
        self.arr = [] 
    
    def isEmpty(self):
        return self.arr == []

    def top(self):
        if self.arr:               
            return self.arr[-1]     
        else : 
            return "Empty list"

    def __len__(self) :
        return len(self.arr)

    def push(self,elem):
        self.arr.append(elem)

    def pr(self):
        print(self.arr)

if __name__ == "__main__" :
    s = Stack()
    print(s.isEmpty())
    print(len(s)) 

    s.push(0)
    s.push(1)
    s.push(7) 
    s.push('hello') 
    print(s.isEmpty())
    s.pr()  
    print(s.top())
    print(len(s)) 
    s.pr() 
