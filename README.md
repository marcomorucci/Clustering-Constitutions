# README

This is the code for an exploratory analysis of language similarities between constitutions. 
The analysis is performed with Python using nltk, and scikit-learn, a full list of dependencies is included below.

Results from the sample run shown in the paper are in the sample_run folder.
They include datasets and tables created by the script.

## Data
All dataset used and created are included in the repo. 
The constitutions of 192 countries in plaintext format are also included. 
These were downloaded from [constitute](https://www.constituteproject.org/) They can be downloaded again using the download.py script.

Other datasets used are:

[Freedom House Country Ratings and Status, 1973-2014](http://www.freedomhouse.org/sites/default/files/Country%20Ratings%20and%20Status%2C%201973-2014%20%28FINAL%29.xls)

[State Fragility Index and Matrix](http://www.systemicpeace.org/inscr/SFIv2013.xls)

[Latent Judicial Independence Around the Globe, 1948-2010](http://polisci.emory.edu/faculty/jkstato/resources/Data/All-Indicators.zip)

Please use the versions included here to run the analysis, as they were slightly modified to be read by the script.
If the analysis is run on downloaded versions of these datasets, not all countries will have their scores read by the script and the program will most likely hang and throw some errors. 
## Instructions
To begin simply chdir into the src folder and do

	python main.py

If you prefer running the module from a python shell import it and do:
	
	>>> import main.py
	>>> data = main.run_analysis()

the results of the analysis will be stored in the data object returned by the
run_analysis function.

## Dependencies:
All these packages have to be installed for the main analysis code to work.

[Numpy](http://www.numpy.org/)

[Scipy](http://www.scipy.org/)

[Nltk](http://www.nltk.org/)

[Scikit-learn](http://scikit-learn.org/stable/)

[Pandas](http://pandas.pydata.org/)

[Statsmodels](http://statsmodels.sourceforge.net/)

[Xlrd](https://github.com/python-excel/xlrd)

For the download.py script to work additional dependencies are needed.

[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

[Requests](http://docs.python-requests.org/en/latest/)

## Version
The version of python the sample run was performed on is 2.7.5. 