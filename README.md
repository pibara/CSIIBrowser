# CSIIBrowser
Simple Cherrypy based dataset browser for China Study II data-set

This is a work in progress. A simple cherrypy server serving up poly fit regression lines for any two variables
from the China Study II dataset.

The file CS89.JSON contains the original data.
A simple script extra.py processes this file and adds a few composite variables such as the probability to live to
the age of at least 80 years old, or the omega6 / omega 3 ratio. The resulting data is combines in NW89.JSON, the data file
used by the server script.

The script will run a basic webserver on port 8080, where it will allow to pick any two variables from the dataset together 
with the degrees of freedom to use in plotting a polifit regression line. 

It's a real simple straightforward script at the moment and it does not do any analysis, it is just meant as a visualisation 
tool for the CS-II data. 

I've published the code of this server in an act of defense, showing I'm not doing anything strange with the data that
makes the equally named book look bad. It is all just visualisation of data that is there, no fancy stats tricks designed 
to make the veganism or proteinophobia look badly, just straight forward code, showing that without the weapons of
eloquence and multi-layered deductive reasoning, two attributes that the books author abundantly posesses, the actual data
shows an often completely opposite picture from the one described in the book. 

So to you vegan militants accusing me of misrepresenting the data, see for yourself, it really is only visualisation,
this is actually how the data looks, sorry about that. 