# Flo MDFF Reader
 MDFF Reader for Flo's Technical Assignment

## What does your repository do?
This is a simple MDFF loader built in Python that receives a NEM12 file as an input and returns an SQL file populated with corresponding INSERT statements, formatted to be functional within the specified database table as shown within the Technical Assessment prompt.
It uses a rudimentary state setup to ensure correct flow is maintained while parsing through NEM 12 files, and to perform error-handling to confirm that the file is formatted correctly and there are no missing mandatory fields. From that point the CSV is separated, row by row, with relevant data sliced out and subsequently placed into INSERT statements (split via occurrence of 200).
I have sourced and attached multiple test files provided from the AEMO website, (alongside a small amount of personal tests to unit test simple errors such as missing or malformed rows.). These have been packaged alongside the application and were sourced from: 

https://aemo.com.au/en/energy-systems/electricity/national-electricity-market-nem/market-operations/retail-and-metering/metering-procedures-guidelines-and-processes


