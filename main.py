import csv
from datetime import datetime

def read_csv_to_dict(file_path):
    data_dict = {}
    
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            # Convert "month-year" to datetime format
            date_str = row['Date']
            date_obj = datetime.strptime(date_str, '%b-%y')
            
            # Store in the dictionary
            data_dict[date_obj] = float(row['Profit/Losses'])
    
    return data_dict

def calculate_sum_profits_months(data_dict):
    profits = []
    months =[]   
    # Sort the dictionary by date
    sorted_data = sorted(data_dict.items(), key=lambda x: x[0])
    for i in range(0, len(sorted_data)):
        current_date, current_profit = sorted_data[i]
        profits.append(current_profit)
        months.append(current_date)
    # Calculate the sum of profit/loss        
    return int(len(months)),sum(profits)


def calculate_changes_and_average(data_dict):
    changes = []
    
    # Sort the dictionary by date
    sorted_data = sorted(data_dict.items(), key=lambda x: x[0])

    # Calculate changes in Profit/Losses
    for i in range(1, len(sorted_data)):
        current_date, current_profit = sorted_data[i]
        prev_date, prev_profit = sorted_data[i - 1]
        change = current_profit - prev_profit
        changes.append(change)

    # Calculate the average of changes
    average_change = sum(changes) / len(changes)

    return changes, average_change


def calculate_greatest_increase_and_decrease(data_dict):
    sorted_data = sorted(data_dict.items(), key=lambda x: x[0])

    greatest_increase_date, greatest_increase_amount = None, float('-inf')
    greatest_decrease_date, greatest_decrease_amount = None, float('inf')
    change = 0
    for i in range(1, len(sorted_data)):
        current_date, current_profit = sorted_data[i]
        prev_date, prev_profit = sorted_data[i - 1]
        change = current_profit - prev_profit

        if change > greatest_increase_amount:
            greatest_increase_amount = change
            greatest_increase_date = current_date

        if change < greatest_decrease_amount:
            greatest_decrease_amount = change
            greatest_decrease_date = current_date

    return greatest_increase_date.strftime('%b-%y'), greatest_increase_amount, greatest_decrease_date.strftime('%b-%y'), greatest_decrease_amount


def print_bank_results_to_text_file(months_total, profits_total,average_change, greatest_increase_date, greatest_increase_amount, greatest_decrease_date, greatest_decrease_amount, output_file):
    with open(output_file, 'w') as text_file:
        # Write header
        text_file.write("Financial Analysis\n")
        text_file.write("----------------------------\n")

        # Write results
        text_file.write(f"Total Months: {months_total}\n")
        text_file.write(f"Total: ${profits_total:.2f}\n")
        text_file.write(f"Average Change: ${average_change:.2f}\n")
        text_file.write(f"Greatest Increase in Profits: {greatest_increase_date} (${greatest_increase_amount:.0f})\n")
        text_file.write(f"Greatest Decrease in Profits: {greatest_decrease_date} (${greatest_decrease_amount:.0f})\n")


def run_PyBank():
    # run the functions to process result from the CSV file
    csv_file_path = 'Resources/budget_data.csv'
   
    data_dict = read_csv_to_dict(csv_file_path)

    # run Total Profits and total months function
    months_total,profits_sum = calculate_sum_profits_months(data_dict)

    # run  average change function
    changes, average_change = calculate_changes_and_average(data_dict)
    # run greates increase and decreasted amount function
    greatest_increase_date, greatest_increase_amount, greatest_decrease_date, greatest_decrease_amount = calculate_greatest_increase_and_decrease(data_dict)

    # Save result to the text file budget_data.txt
    output_file_path = 'analysis/budget_data.txt'
    print_bank_results_to_text_file(months_total, profits_sum,average_change, greatest_increase_date, greatest_increase_amount, greatest_decrease_date, greatest_decrease_amount, output_file_path)

    # Print the results in terminal for testing
    print(f'Financial Analysis')
    print('----------------------------')
    print(f'Total Months: {months_total}')
    print(f'Total: ${profits_sum}')
    # print(f'Changes in Profit/Losses over the entire period: {changes}')
    print(f'Average Change: ${average_change}')
    print(f'Greatest Increase in Profits: {greatest_increase_date} (${greatest_increase_amount})')
    print(f'Greatest Decrease in Profits: {greatest_decrease_date} (${greatest_decrease_amount})')

####################################################################


def analyze_poll(csv_file_path):
    total_votes = 0
    candidates_votes = {}
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            total_votes += 1

            candidate_name = row['Candidate']

            # Update candidate name not in the candiates list, 
            # then add one and set poll value = 1 for the starting one
            if candidate_name not in candidates_votes:
                candidates_votes[candidate_name] = 1
            else:
                candidates_votes[candidate_name] += 1 #add one vote when found candidate name in the list

    return total_votes,candidates_votes

def calculate_percentages(candidate_votes, total_votes):
    percentages = {}

    for candidate_name, votes in candidate_votes.items():
        percentage = (votes * 100) / total_votes
        percentages[candidate_name] = round(percentage,3)

    return percentages

def print_poll_results_to_text_file(total_votes,candidate_votes,percentages,output_file):
    with open(output_file, 'w') as text_file:
        # Write header
        text_file.write("Election Results\n")
        text_file.write("----------------------------\n")
        text_file.write(f"Total Votes: {total_votes}\n")
        text_file.write("----------------------------\n")
        for candidate_name, votes in percentages.items():
            text_file.write(f"{candidate_name}: {votes}% ({candidate_votes[candidate_name]})\n")

        text_file.write("----------------------------\n")
        
        winner = max(percentages, key=percentages.get)
        text_file.write(f"Winner: {winner}\n")

        text_file.write("----------------------------\n")

def run_PyPoll():    
    csv_file_path = 'Resources/election_data.csv'
    total_votes,candidate_votes  = analyze_poll(csv_file_path)
    percentages = calculate_percentages(candidate_votes, total_votes)

    # Save result to the text file election_data.txt
    output_file_path = 'analysis/election_data.txt'
    print_poll_results_to_text_file(total_votes, candidate_votes, percentages,output_file_path)

    # Print the results in terminal for testing
    # print(f"Total Votes: {total_votes}")
    # print(f'{candidate_votes}')
    # print(f'{percentages}')
    winner = max(percentages, key=percentages.get)
    # Print the results in terminal for testing
    print(f'Election Results')
    print('----------------------------')
    print(f'Total Votes:: {total_votes}')
    for candidate_name, votes in percentages.items():
        print(f'{candidate_name}: {votes}% ({candidate_votes[candidate_name]})')


    print('----------------------------')
    print(f'Winner: {winner}')
    print('----------------------------')
    
    



########################################################


# Python script to analyse the financial records
run_PyBank()

print('----------------------------')
print('----------------------------')

# Python script to analyse the financial records
run_PyPoll()







