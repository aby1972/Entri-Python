import random
i=0
b=random.randint(1,100)
while True:
    a=int(input('Enter a number between 1-100 : '))
    i+=1
    if a==b or i==7:
        if a==b:
            print('Congratulations! You found the lucky number on :',i,' tries')
            break
        else:
            print('Try another time, the lucky number is :',b)
            break
    elif a>b:
        print('Too High!')
    elif a<b:
        print('Too Low!')


