from termcolor import colored, cprint

class Queue:
    def __init__(self, length):
        self.length = length
        self.queue = [None]*(length+1)
        self.head = 0
        self.tail = 0

    def enqueue(self, x):
        if self.is_full():
            print( 'Overflow' )
        self.queue[self.tail] = x
        if self.tail == self.length:
            self.tail = 0
        else:
            self.tail = self.tail + 1

    def dequeue(self):
        if self.is_empty():
            print( 'Underflow')
        x = self.queue[self.head]
        if self.head == self.length:
            self.head = 0
        else:
            self.head = self.head + 1
        return x

    def is_empty(self):
        if self.head == self.tail:
            return True
        return False

    def is_full(self):
        if self.head == self.tail+1 or (self.head == 0 and self.tail == self.length):
            return True
        return False

    def show(self):
        print ('Queue contents are:')
        for i in range(self.length):
            print ( self.queue[int((i+self.head)% self.length)],end=' ')
            
        print('\n')


if __name__ == "__main__":
    q = Queue(7)  

    print(colored("Checking is empty : output `",'green', attrs=['reverse', 'blink']) , q.is_empty())

    q.enqueue(1)
    q.enqueue(1)
    q.enqueue(1)
    q.enqueue(1)
    q.enqueue(1)
    # Check is full when ,we doesn`t enqueued all items
    print(colored('Check is full when ,we doesn`t enqueued all items  : output `','red', attrs=['reverse', 'blink']) , q.is_full())

    q.enqueue(1)
    q.enqueue(1)
    
    print(colored('Check is full when ,we enqueued all items : output `' ,'green', attrs=['reverse', 'blink']) , q.is_full())
    q.show()
    # adding more element then queue length
    q.enqueue(1)
    q.dequeue() 
    q.dequeue()
    q.dequeue()
    q.dequeue()
    q.dequeue()
    q.dequeue()
    q.dequeue()

    q.dequeue()
    # removing more elements then we have in queue
    print(colored('Check is empty  : output `','green', attrs=['reverse', 'blink'])  , q.is_empty())