#Application Name: Quiz
#Name: Will Aldridge
#Date: 7th December 2019

import glob #glob is a module that helps find files by pattern matching  
import csv #csv will be used to convert the files into a more useful format
import datetime #to get the current date and time
import sys
import operator

#Declaring variables and assigning them temporary values
score = 0
total_questions = 0
user_name = ""
chosen_file = "Assessment_Questions.txt"

def display_divider(text_line):
    #Nicely format headers for each section
    print("")
    print("------------------------------------")
    if len(text_line)>0:
        print("|")
        print("|    ",text_line)
        print("|")
        print("------------------------------------")
    print("")
    
def select_quiz_from_directory():
    display_divider("Which Quiz Would You Like To Play?")
    file_count = 1
    #create the quiz files list
    quiz_files = []
    #get all files in the directory with the .txt suffix
    quiz_files = glob.glob("Quizs/*.txt") 

    #for every quiz in the file, print the name of the quiz and move to the next 
    if quiz_files:
        for quiz in quiz_files:
            print("(",file_count,")",quiz)
            file_count = file_count + 1
    else:
        #if no quizes are found, exit the application and display error
        sys.exit("No Quizs Found")

    #Ask the user to enter quiz number
    selected_quiz = input("Enter Quiz Number: ")

    #check is integer, is not 0, is not empty, is less than or equal to file count 
    if (selected_quiz != "0") and (selected_quiz.isdigit()) and (int(selected_quiz) <= file_count-1):

        selected_quiz = int(selected_quiz)
        #get file name of selected quiz number 
        chosen_file = quiz_files[selected_quiz - 1]

        #removes directory from file name
        chosen_file = chosen_file[6:]

        return chosen_file

    else:
        display_divider("Please Input A Valid Number")
        return select_quiz_from_directory()
        
    

   
def do_quiz():
    display_divider("Lets Begin!")

    #assumes file format is csv even though file in brief had .txt extension
    score = 0
    total_questions = 0
    #open the selected quiz
    with open("Quizs\\"+chosen_file, newline = '') as csv_file:
        all_question_data = csv.reader(csv_file)
        

        #Loop through the questions asking the first line and then displaying options
        for question_data in all_question_data:

            #Check question_data is not empty
            if question_data:
                num_data_elements = len(question_data)
                #check at least 3 elements, question, options, and answer
                if num_data_elements > 2:

                    #assume question is first element and answer is the last
                    answer_correct = question_data[-1]

                    #Checks to see that the number given as the answer is actually viable
                    if int(answer_correct) > num_data_elements-2:
                        sys.exit("Answer Number is Bigger then Number of Answer Options")
                        
                    print("Question: ", question_data[0])
                    

                    #assume everything inbetween are multi-choice answers
                    for option_count in range(1, num_data_elements-1):
                        print("(",option_count,")",question_data[option_count])

                    total_questions = total_questions + 1
                    
                    #ask user to input the number of the answer
                    answer_guess = input("Enter The Number Of The Answer: ")
                    #Check guess is a number and within range, is not blank
                    if (answer_guess != "0") and (answer_guess.isdigit()) and (int(answer_guess) <= num_data_elements-2):
                        

                        #check that the number they inputted is the same as the correct answer
                        if int(answer_guess) == int(answer_correct):
                            score = score + 1
                            print("CORRECT!")
                        else:
                            print("INCORRECT.")
                        print("Your Score is", score, "out of", total_questions)
                        display_divider("")

                    else:
                        display_divider("Please Input a Valid Number")

                else:
                    print("")

    return chosen_file, total_questions, score

def display_results(total_questions, score):
    print("End of Quiz")
    #simple feedback for the player
    if score/total_questions >= 0.75:
        print("CONGRATULATIONS,", user_name,", you did great!")
    elif score/total_questions > 0.5 and score/total_questions < 0.75:
        print("You did alright,", user_name)
    else:
        print("Not good,", user_name,", you can do better!")
    print("Your Score is", score, "out of", total_questions)

    display_divider("")

def update_results_file():
    #get the date and time and store in that format
    current_datetime = datetime.datetime.now()
    date_and_time = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

    #adds the results folder to whatever quiz the user chose to get the corresponding results file
    quiz_results_file = "Results/"+chosen_file

    results_file = open(quiz_results_file, "a+", newline='')

    #layout of the results table, splitting each elemnt with a comma
    results_writer = csv.writer(results_file, delimiter = ',', quotechar = '"')
    results_writer.writerow([chosen_file, date_and_time, user_name, score, total_questions])
    results_file.close()

def sort_and_display_leaderboard():
    display_divider("Leaderboard")
    
    results_file = open("Results\\"+chosen_file, newline = '') 
    with results_file as csv_file:
        results_reader = csv.reader(csv_file)
        #sort through the results file by column 3 which is score, and reverse so highest value is at the top
        sorted_results = sorted(results_reader, key=lambda row: row[3], reverse=True)

        #format the leaderboard
        for question_data in sorted_results:
            leader_name = '{:<20}'.format(question_data[2])
            leader_score = '{:<4}'.format(question_data[3])
            leader_date = '{:<20}'.format(question_data[1])

            print(leader_name, "Score:", leader_score, "Date:", leader_date)

    results_file.close()


#Display Introduction
display_divider("Welcome To The Quiz!")

#Ask Users name
user_name = str(input("What Is Your Name?: "))
user_name = user_name.strip()

#Ask which quiz the user wants to do
chosen_file = select_quiz_from_directory()

#Load and perform the selected quiz
chosen_file, total_questions, score = do_quiz()

#Display results
display_results(total_questions, score)

#Update files with new record
update_results_file()

#Sort and Display Leaderboard
sort_and_display_leaderboard()






