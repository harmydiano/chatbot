import time
# Function adding an item to the list
def addItem(todo):
    f = open('list.txt', 'a')
    f.write(todo + "\n")
    #f.close()
    print(todo + " added successfuly.")

# Function to view items on the list
def viewItem():
    f = open('list.txt', 'r')
    data = f.read()
    print(data)

# function to remove item from list
def removeItem(num):
    f = open("list.txt", "r")
    data_2 = f.readlines()
    deleted_file = data_2[num]
    del data_2[num]
    done = data_2
    for a in done:
        #print (a)
        f = open("list.txt", "w")
        f.writelines(a)
    print(deleted_file + " was successfully deleted.")
    #f.close()
    #welcome(2)

task=1
while(task!=0):
    print ("==============================================")
    print ("0. Exit")
    print ("1. Insert Data")
    print ("2. Show Data")
    print ("3. Delete Data")
    print ("4. Update Data")
    print ("==============================================")
    task=int(input("Enter your choice : "))
    print ("==============================================")

    if task == 1:
        myTodo = input("Add an Item: \n")
        addItem(myTodo)
        time.sleep(2)
    elif task == 2:
        viewItem()
        task = 1
        time.sleep(2)
    elif task == 3:
        myTodo = int(input("Delete an Item:\n"))
        removeItem(myTodo)
        time.sleep(2)
    elif task ==0:
        print("you have successfully eneded the program")
        task = 0



