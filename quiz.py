import sys
import random
import mysql.connector
import matplotlib.pyplot as plt
import pymysql

mydb=mysql.connector.connect(host='localhost',user='root',passwd ='raj28',database = 'project')
mycursor=mydb.cursor()
'''print(mydb ,"connection")
print(mycursor, "connection ")'''
def Home():
    opt=1
    while opt!=4:
        print('\n\n\n')
        print("*"*30+"G.K Quiz Competetion"+"*"*30)
        print('\t\t       ----    -  -   ----  -    -  ----- ----- ')
        print('\t\t      |        | /   |    | |    |    |       / ')
        print('\t\t      | _ _    |/    |    | |    |    |      /  ')
        print('\t\t      |    |   |\    |   \| |    |    |     /   ')
        print('\t\t      |    |   | \   |    \ |    |    |    /    ') 
        print('\t\t       ----   .|  \ . ---- \ ----   -----  -----')
        print("*"*100)
        print("Welcome to Quiz")
        print("********************")
        print("1. REGISTER YOURSELF")
        print("2. LOGIN & START QUIZ")
        print("3. LEARDERBOARD")
        print("4. EXIST")
        opt=int(input("Enter your choice: "))
        if opt==1:
            Login()
        elif opt==2:
            Quiz()
        elif opt==3:
            Board()
        elif opt==4:
            Exist()
        else:
            Home()

def Login():
    print("\t\t\t ALL information prompted are mandatory to be filled")
    pname=input("PLAYER-NAME: ")
    roll=input("ID/ENROLLMENT-NO: ")
    pwd=int(input("Enter your PASSWORD (IN NUMERIC): "))
    pwd1=int(input("RE-ENTER PASSWORD : "))
    if pwd==pwd1:
        insert_query =("insert into students(Player_Name,Enrollment_No,Pwd) values('{}','{}',{})".format(pname,roll,pwd))
        mycursor.execute(insert_query.format(pname,roll,pwd))
        print("\t\t\t ***READY FOR QUIZ***")
    else:
        print("\t\t **Terminate Program!!! Again start and SIGN IN yourself**")
    mydb.commit()

def Quiz():
    print("-" * 95)
    print("Login Yourself")
    print("***********************")
    mycursor.execute("Select * from Questions")
    data=mycursor.fetchall()
    roll=input("Enter your Enrollment_No: ")
    name=input("Enter your Name: ")
    total_question=mycursor.rowcount
    print("Welcome to Quiz portal")
    print("***********************")
    to_attempt=int(input(f"Enter the number of questions to attempt (max 10):"))
    question_no=[i for i in range(1, total_question+1)]
    question_no=random.sample(question_no, to_attempt) 
    print("Quiz has started")
    c=1
    points=0
    for i in range(0,len(question_no)):
        mycursor.execute("Select * from Questions where ques_id=%s",(question_no[i],))
        ques=mycursor.fetchone()
        print("--------------------------------------------------------------------------------------------")
        print("Q.",c,": ",ques[1],"\nA.",ques[2],"\t\tB.",ques[3],"\nC.",ques[4],"\t\tD.",ques[5])
        print("--------------------------------------------------------------------------------------------")
        c+=1
        ans=None
        while ans==None:
            choice=input("Answer (A,B,C,D): ")
            if choice=='A' or choice=='a':
                    ans=ques[2]
            elif choice=='B' or choice=='b':
                    ans=ques[3]
            elif choice=='C' or choice=='c':
                    ans=ques[4]
            elif choice=='D' or choice=='d':
                    ans=ques[5]
            else:
                print("Kindly select A,B,C,D as option only")
        if ans==ques[6]:
            print("Correct")
            points=points+1
        else:
            print("Incorrect.. Correct answer is: ",ques[6])
    print("Quiz has ended !! Your final score is: ",points)
    mycursor.execute("Select * from users")
    data=mycursor.fetchall()
    mycursor.execute("Insert into users values (%s,%s,%s)",(roll,name,points))
    mydb.commit()

def Board():
    mycursor.execute("Select name , points from users")
    result = mycursor.fetchall()
    name = []
    points = []
    for r in result:
        name.append(r[0])
        points.append(r[1])
    plt.bar(name,points)
    plt.xlabel("Player Name")
    plt.ylabel("Points")
    plt.title("Leaderboard")
    plt.show()
    

def Exist():
     print("Exiting the Quiz")
     mycursor.close()
     mydb.close()
     sys.exit();
Home()
