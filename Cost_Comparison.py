import pandas
import math
from tabulate import tabulate
# this function return a decorated statement i.e.: === Hello World ===
def make_statement(statement,icon):
    s=(icon*3)+" "+statement+" "+(icon*3)
    return s

# intruction
def instruction():
    print('''
          
                    📈 Price Comparison 📈
          
    - Price Comparison program will collect information about products that you are
confused or not sure which to choose due to its variability of price and weight/volume.
          
    - Price Comparison then will give you a summaries and suggestions based on the information provided. 
This brings you a better view about those products to have a better shopping decision.
          
    🛟 How to use? 🛟
          * Firstly, you have a list of items that you want to consider.
          * Second, follow the input instruction of the program to enter the appropriate input.
          * Third, the program will based on what you have entered to generate a suggestions table.
          * Fourth, you could based on the Suggestions table to consider which item is suitable to buy.
    
    Happy shopping 🛍️🛒
          ''')
    
# Return True or False bases on use response
def yes_no(question):
    print(question,end="")
    while True:
        response = input().lower()
        if response=="yes" or response=="y":
            return True
        if response=="no" or response=="n":
            return False
        print("Please enter a valid response(Yes or No)")

    

def alt_unit_instruction():
    print("""               ----Alternative Unit---
    - We suggest using this as your input values may lead to miscalculate or difficulty for you to compare product.
Means that the unit_price may be miscalculate as we round it to 5sf, if cost is way too smaller than
amount in unit, then the unit_price will be less than 1 i.e. 0.0000004, this makes it difficult for both we and you to compare.
    - The alternative unit is an unit that we create based on your input, which makes sure that the cost is large enough to produce
an unit price that is larger than 1.    
             
           """)
def yes_no_alt_unit(question):
    print(question,end="")
    while True:
        response = input().lower()
        if response=="yes" or response=="y":
            return True
        if response=="no" or response=="n":
            return False
        if response=="i" or response=="information" or response=="info":
            print("\n\n")
            alt_unit_instruction()
            print(question,end="")
            continue
        print("Please enter a valid response(Yes or No)")
 

# This function makes sure users' input will be a valid number, integer
def num_check(question,num_type):
    print(question, end="")
    if num_type==int:
        error_message_value_error = "Please input an integer(i.e. 1, 2, 3,...)"
        error_message_lesser_0 = "Please input an integer that is greater than 0"
    else:
        error_message_value_error="Please input a valid number"
        error_message_lesser_0="Please input a number that is greater than 0"
    while True:
        try:
            res=input()
            res=num_type(res)
            if res<=0:
                print(error_message_lesser_0)
                continue
            return res
        except ValueError:
            print(error_message_value_error)

# Erases spaces before first valid character and after last valid character
def space_eraser(raw_string):
    length=len(raw_string)
    #take the index of the first letter of the string and delete invalid space
    index_1=-1
    for i in range (0,length):
        if raw_string[i]!=" ":
            index_1=i
            break
        
    #take the index of the last letter of the string and delete invalid space
    for i in range (0,length):
        if raw_string[length-1-i]!=" ":
            index_2=(length-1-i)+1
            break
    new_string=""
    if index_1==-1:
        return ""
    for i in range (index_1,index_2):
        new_string+=raw_string[i]
    return new_string

# Makes sure user input the valid string
def blank_checker(question):
    print(question, end="")
    while True:
        response = input()
        """   After put my raw string into the space eraser, if its only space, the return will be "", so I used space_eraser 
         to check all_space cases without having another loop running along the raw string to check if its all space"""
        response=space_eraser(response)
        if response=="" :
            print("Input cannot be blank, please enter a valid response...")
        else:
            return response
        
# Add $ sign before a number
def currency(x):
    return f"${x:.2f}"

# Check and return the most gaps between cost and unit in form 10^n with n is the biggest gaps.
def check_alt_unit(total_cost,total_amount_in_unit):
    Net=0
    for i in range (0,len(total_cost)):
        net=int(math.log(total_amount_in_unit[i],10))-int(math.log(total_cost[i],10))
        if net==0 and total_amount_in_unit[i]<=total_cost[i]:
            net=0
        elif net>0:
            net=math.pow(10,net)
        elif net==0 and total_amount_in_unit[i]>total_cost[i]:
            net=1
        else:
            net=0
        Net=max(net,Net)
    return Net
    
# Collect information of products
def information_collector(unit):
    total_product_name=[]
    total_amount_in_unit=[]
    total_cost=[]
    total_unit_price=[]
    print("\n\n")
    print(make_statement("Item's Information","_"))
    amount_of_item=1
    while True:
        print(f"""\nItem {amount_of_item} (Input "xxx" at "Name" to exit)""")
        if amount_of_item==1:   # force user to input at least one item here
            while True:
                product_name = blank_checker("""Name: """) 
                if(product_name!="xxx"):
                    break
                print("Please input at least 1 product...")
        else:
            product_name = blank_checker("""Name: """)
            if product_name=="xxx":
                break

        amount_in_unit = float(f"{num_check(f"How much in {unit}? ",float)}")
        cost=num_check("How much does it cost? $", float)
        total_product_name.append(product_name)
        total_amount_in_unit.append(amount_in_unit)
        total_cost.append(cost)
        unit_price=float((cost/amount_in_unit))
        total_unit_price.append(unit_price)
        amount_of_item+=1

    Net=check_alt_unit(total_cost,total_amount_in_unit)
    information_dict={
        'Name':total_product_name,
        f'{unit}':total_amount_in_unit,
        'Cost':total_cost,
        f'Unit Price ($/{unit})':total_unit_price
    }
    information_frame=pandas.DataFrame(information_dict)
    print("_"*26)
    return information_frame,total_unit_price,total_cost,amount_of_item-1,Net

def round_5sf(number):
    return f"{number:.5f}"
def alternative_unit(information_frame,Net,unit):
    alt_frame=pandas.DataFrame()
    alt_frame['Name']=information_frame['Name']
    alt_frame[f'{unit}']=information_frame[unit]
    alt_frame[f'Cost ($/{Net})']=information_frame['Cost']*Net
    alt_frame[f'Alt Unit Price ($/{unit}*{Net})']=(alt_frame[f'Cost ($/{Net})']/alt_frame[f'{unit}'])
    alt_frame[f'Alt Unit Price ($/{unit}*{Net})']=alt_frame[f'Alt Unit Price ($/{unit}*{Net})'].apply(round_5sf)
    return alt_frame


# ‼️‼️Main‼️‼️
if yes_no("Do you want to read the instruction? "):
    instruction()

#asking initial value, input
product_type = blank_checker("What type of product you want to consider today? ")
unit=blank_checker("What is the unit for that product? ")
budget = num_check("What is your budget? $", float)

# collecting information of products
information = information_collector(unit)
information_frame=information[0]
total_unit_price=information[1]
total_cost=information[2]
product_amount=information[3]
Net=information[4]

                    # SPECIAL : ‼️ ALTERNATIVE UNIT ‼️
if Net>1:
    alt_frame=alternative_unit(information_frame,Net,unit)

# apply $ marks into cost
information_frame['Cost']=information_frame['Cost'].apply(currency)

# get the index of the FIRST product that has lowest unit price
suggestion_index_initial=0
for i in range(0,product_amount):
    if total_cost[i]<=budget and total_unit_price[i]<total_unit_price[suggestion_index_initial]:
        suggestion_index_initial=i

# check if there is another valid product with the same unit price
suggestion_index=[]
for i in range(0,product_amount):
    if total_unit_price[i]==total_unit_price[suggestion_index_initial] and total_cost[i]<=budget:
        suggestion_index.append(i)
# Round the unit price to 5sf
information_frame[f'Unit Price ($/{unit})']=information_frame[f'Unit Price ($/{unit})'].apply(round_5sf)


# checking cases of suggestions
Suggestion_announce = ""
suggestion_table=(information_frame.iloc[suggestion_index])  # find and create a pandas table of all products that have the lowest unit price
suggestion_table=tabulate(suggestion_table, headers="keys", tablefmt="grid") # from pandas table, create a tabulate(decorated) table

#suggestion but ALTERNATIVE
alt_suggestion=(alt_frame.iloc[suggestion_index])
alt_frame=tabulate(alt_frame,headers="keys", tablefmt="grid")
alt_suggestion=tabulate(alt_suggestion,headers="keys", tablefmt="grid")

if total_cost[suggestion_index_initial]>budget: # Worst cases, none of the option is valid as its all greater than budget
    Suggestion_announce=f"\nUnfortunately, there is no valid product for you to buy as the product's costs are greater than your budget."
    alt_output="" 
else:
    Suggestion_announce=f"\nThis is the list of valid suggestion(s) for you:\n{suggestion_table}"
    # ALTERNATIVE UNIT‼️
    # Asking if they want to see alternative table
    alt_output=""   # Create a variable in advance, regardless what user answer in yes_no_unit, the program still print alt_output out
    # if user say "yes" then alt_output will be every output involve alternative table; otherwise alt_ouput is empty so its output nothing
    if yes_no_alt_unit("""Do you want to see Alternative-Unit Suggestions?(enter "i" for more information) """):
        alt_output=f"""{make_statement("Alternative Unit","=")}\n\n{make_statement("Alternative Unit Information","-")}\n{alt_frame}\n\nThis is the list of suggestion(s) for you based on our Alternative Unit:\n{alt_suggestion}"""
information_frame=tabulate(information_frame, headers="keys", tablefmt="grid")




# Varibles of things will be output
HEADING=make_statement("Price comparison","=")
product_file=f"- Type of product: {product_type}"
budget_file=f"- Budget: ${budget}"
product_heading=make_statement("Product Information","-")



    
suggestion_heading=make_statement("Suggestions","-")
# list of things will be printed out
output_list=["\n\n","            ",
HEADING,"\n\n",
product_file,"\n",
budget_file,"\n\n",
product_heading,"\n",
information_frame,"\n\n",
suggestion_heading,"\n",
Suggestion_announce,"\n\n",
alt_output
]
# print in the program first
for i in range (0,len(output_list)):
    print(output_list[i],end="")

# print in file
write_to="Price_Comparison.txt"
text_file=open(write_to,"+w")

for item in output_list:
    text_file.write(item)
