############################################################################
# This is a tutorial and practice for if else condition, this contains few beginner and intermediate exercise
############################################################################

## If Elif Else condition when to use

purse = 50
food_price =110 

if (food_price <= purse):
    print ("can buy food")
else:
    print  ("go hungry") 

## Multiple conditions
# say a grading system

marks = 75

if (marks >=90):
    print ("A+")
elif (marks >=80):
    print ("A")
elif (marks >=70):
    print ("B+")
elif (marks >=60):
    print ("B")
else:
    print("fail")

## try with all marks possible to test
# you will get output as per your conditions,this script explain if else condition and how to use it in python
##########
# Write a program to check if a number is even or odd.

number = 3  

if (number%2==0):
    print ("even")
else:
    print ("odd")

##  modulus operator % to check if there is any remainder after division
# tested with even and odd numbers and got the correct result
##########
# Take an integer input and print if it's positive, negative, or zero.

integer = 1

if (integer < 0):
    print ("negative")
elif (integer > 0):
    print ("positive")
else:
    print ("zero")

## tested with negative and postive and zero value for integer and output as expected
#####

username= "admin"
password= "pass1123"

if username != "admin":
    print ("invalid username")
elif password != "pass123":
    print ("invalid password")
else:
    print ("login successful")

## Alternate way

if username == "admin" and password == "pass123":
    print ("login successful")
else :
    print ("invalid credentials")

######
# Input two numbers and an operator (+, -, *, /) Output the result using if/elif.

num1 = float(input("Enter first number"))   
operator = input("Enter operator(+,-,*,/):")
num2 = float(input("Enter 2nd number"))

if operator == "+":
    print (num1+num2)
elif operator == "-":
    print (num1-num2)
elif operator == "/":
    if num2 !=0:
        print (num1/num2)
    else:
        print ("invalid number")
elif operator == "*":
    print (num1*num2)
else:
    print ("invalid operator")


# Float used in numbers so that decimal numbers can be used , Input prameter used to input number and operator
# Another if condition used in division to check if the second number is not zero before dividing (to avoid error).
