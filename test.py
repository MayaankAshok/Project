import sys
import mysql.connector
import random
mydb=mysql.connector.connect(host= "localhost" ,user= "root",\
	passwd="root",database= "quiz")
mycursor=mydb.cursor()
def Home():
	f=1
	while f!=3:
		print("Welcome to Quiz")
		print("********************")
		print("1. Enter Questions")
		print("2. Take Quiz")
		print("3. Exit")
		f=int(input("Enter your choice: "))
		if f==1:
			Question()
		elif f==2:
			Quiz()
		elif f==3:
			print("Exiting the Quiz")
			mycursor.close()
			mydb.close()
			sys.exit()
		else:
			Home()
def Question():
	ch='Y'
	while ch=='Y' or ch=='y':
		print("Welcome to Question Portal")
		print("***********************")
		q=input("Enter the question :")
		op1=input("Enter the option 1 :")
		op2=input("Enter the option 2 :")
		op3=input("Enter the option 3 :")
		op4=input("Enter the option 4 :")
		ans=0
		while ans==0:
			op=int(input("Which option is correct answer (1,2,3,4) :"))
		if op==1:
			ans=op1
		elif op==2:
			ans=op2
		elif op==3:
			ans=op3
		elif op==4:
			ans=op4
		else:
			print("Please choose the correct option as answer")
			mycursor.execute("Select * from question")
			data=mycursor.fetchall()
			qid=(mycursor.rowcount)+1
			mycursor.execute("Insert into question values (%s,%s,%s,%s,%s,%s,%s)",(qid,q,op1,op2,op3,op4,ans))
			mydb.commit()
			ch=input("Question added successfully.. Do you want to add more (Y/N)")
			Home()
def Quiz():
	print("Welcome to Quiz portal")
	print("***********************")

	mycursor.execute("Select * from question")
	data=mycursor.fetchall()
	name=input("Enter your name :")
	rc=mycursor.rowcount
	noq=int(input("Enter the number of questions to attempt (max %s):"%rc))
	l=[]
	while len(l)!=noq:
		x=random.randint(1,rc)
		if l.count(x)>0:
			l.remove(x)
		else:
			l.append(x)
	print("Quiz has started")
	c=1
	score=0
	for i in range(0,len(l)):
		mycursor.execute("Select * from question where qid=%s",(l[i],))
		ques=mycursor.fetchone()
		print("--------------------------------------------------------------------------------------------")
		print("Q.",c,": ",ques[1],"\nA.",ques[2],"\t\tB.",ques[3],"\nC.",ques[4],"\t\tD.",ques[5])
		print("--------------------------------------------------------------------------------------------")
		c+=1
		ans=None
		while ans==None:
			choice=input("Answer (A,B,C,D) :")
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
				score=score+1
			else:
				print("Incorrect.. Correct answer is :",ques[6])
	print("Quiz has ended !! Your final score is :",score)
	input("Press any key to continue")
	Home()

Home()