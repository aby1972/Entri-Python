def add_expense():
    exhead=input('Enter the Expense category : ')
    examt=input('Enter the Expense amount : ')
    exdate=input('Enter the Expense Date as DD/MM/YY: ')
    f=open('expense.txt',"a")
    f.write(f"{exhead},{examt},{exdate},\n")

def view_expense():
    print('Ex.Head          Ex.Amount         Ex.Date')
    f=open('expense.txt','r')
    for i in f:
        l=i.split(',')
        print(l[0],"          ",l[1],"              ",l[2])

def total_expense():
    tot=0
    f=open('expense.txt','r')
    for i in f:
        l=i.split(',')
        tot=float(l[1])+tot
    print('Total Expense as of today is : ',tot)
try:
    while True:
        a = 0
        a=int(input('1. Add Expense\n2. View Expense\n3. Total Expense\n4. Any other key to exit : '))
        if a==1:
            add_expense()
        elif a==2:
            view_expense()
        elif a==3:
            total_expense()
        else:
            print('Thank you for using our Expense Tracking Application')
            break
except ValueError:
    print('Thank you for using our Expense Tracking Application')
    quit()

