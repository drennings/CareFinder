----------------------------------------------
Note: The user needs the following packages

1. numpy
2. pandas
3. termcolor
4. geopy.geocoders

The script is validated to work in Python 2.7

-----------------------------------------------

User guide:

1. start python
2. import the doctor_finder library. Type: from doctor_finder import *
3. call the function to define a query: Type: find_doctor()
4. The console will ask you to 
	4.1 specify a query (no " or ' marks needed)
	4.2 give your location (several formats of address can be used)
	4.3 confirm your location, type y or n
	4.4 define a range (as the crows fly) from your location in km, just give a number

5. The console will suggest the 5 top ranked doctors + hospital in your range that are active in the field of your needs
