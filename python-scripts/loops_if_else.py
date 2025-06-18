#####
# Practicing for if/else and while and for loop

# for loop is used when you know how many times you want to loop, like a list, string, or range

for i in range(1,11):
    print (i)

## this will print 1 to 10 , in python if you specify a range it will display the last number as n-1 in your range so in our case 11-1 = 10

## while loop is used when you need to loop until a condition

## Count from 1 to 5 Using while Loop

counter = 1

while counter <=5:
    print("Count is:",counter)
    counter += 1

# counter = 1 → We start counting from 1.
# while counter <= 5: → Keep looping as long as counter is ≤ 5.
# print(...) → Shows the current value of counter.
# counter += 1 → Increments the counter by 1 every time the loop runs.
# Output will be
# Count is: 1
# Count is: 2
# Count is: 3
# Count is: 4
# Count is: 5
############################################
## combining if/else/elif and for/while loop
####  Password Checker with Limited Attempts

attempts = 3
while attempts > 0:
    password = input("Enter password :")
    if password == "pass123":
        print ("Access granted")
        break
    else :
        attempts -=1
        print (f"Wrong password. Attempts left: {attempts}")
if attempts == 0:
    print ("Account locked. Too many wrong attempts")

## Output -- Enter password :admin123
# Wrong password. Attempts left: 2
# Enter password :dem
# Wrong password. Attempts left: 1
# Enter password :eerr
# Wrong password. Attempts left: 0
# Account locked. Too many wrong attempts
## Key takeaways
# while attempts > 0:	Loop runs until attempts run out
# f"string with {variable}"	Clean way to print variables inside strings
# break	Exits the loop immediately when condition is met



