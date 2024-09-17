import re
from collections import Counter
from datetime import datetime

def parse_logs(file_path):
    # Counter to store (description, recommended_page) counts
    log_counter = Counter()
    
    with open(file_path, 'r') as file:
        # Read the entire file content
        content = file.read()
        
        # Regular expression to match description and recommended page parts
        pattern = r'Description:\s*(.*?)\s*Recommended Page:\s*(.*?)\s*-'
        log_entries = re.findall(pattern, content, re.DOTALL)
        
        # Count each unique (description, recommended_page) pair
        log_counter.update(log_entries)
    
    return log_counter

def summarize_logs(log_counter, output_file_path):
    # Get the current date for the footer
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    with open(output_file_path, 'w') as file:
        for (description, recommended_page), count in log_counter.most_common():
            file.write(f"- Description: {description.strip()}\n")
            file.write(f"- Recommended Page: {recommended_page.strip()} {count} times\n")
            file.write(f"$====================@stijn / - / {current_date}@====================$\n\n")

if __name__ == "__main__":
    # Provide the path to your log file and the output file
    log_file_path = 'data_log.txt'
    output_file_path = 'summary_output.txt'
    
    # Parse the logs and summarize descriptions
    log_counter = parse_logs(log_file_path)
    summarize_logs(log_counter, output_file_path)
