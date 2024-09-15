import sys
import logging

def write_sql_statements(statements, output_file):
     #add -debug to console args to print to console
    if '-debug' in sys.argv:
        for statement in statements:
            logging.info(statement) 
    else:
        with open(output_file, 'w') as file:
            for statement in statements:
                file.write(statement + '\n')
