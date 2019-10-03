import rpyc
import threading
test = []
uname = []
flag_duplicate = False
myReferences= set()
CallBackLock = threading.Lock()
class MyService(rpyc.Service):
 
  def on_connect(self):
    self.fn = None
    print("onconnect")
    

  ##duplicate error handling
  def exposed_serverPrint(self,message):
    global test
    global duplicate_flag
    if message in uname:
      print("cant use this name!")
      duplicate_bool = True

    else:
      uname.append(message)
    
      for i in myReferences:
        if i is not self.fn:
        
          i(message +" joined the room")

  def exposed_serverExit(self,name):
    global test
    myReferences.remove(self.fn)
    uname.remove(name)
  
  def exposed_serverPrintMessage(self,message):
    global test
    test.append(message)
    print(message)

    
                  
  def exposed_replyWith(self,number):
    return test[number]

  def exposed_replyLength(self,length):
    return len(test)

  def exposed_setCallback(self,fn):
    global myReferences
    self.fn = fn
    with CallBackLock:
      myReferences.add(self.fn)
    with CallBackLock:  
      print (myReferences)
      for i in myReferences:
        print (i),

    
if __name__ == "__main__":
   from rpyc.utils.server import ThreadedServer
   t = ThreadedServer(MyService, port = 5555)
   t.start()
  
