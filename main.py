import sys
import logging
from processor import process_nem12_file
from writer import write_sql_statements

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input file path as an argument. Eg. python main.py <input file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = 'output.sql'
    sql_statements = process_nem12_file(input_file)
    write_sql_statements(sql_statements, output_file)