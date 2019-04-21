from urllib import request
from urllib.request import urlopen
from dotenv import load_dotenv
from twython import Twython 
import random
import sys 
import os

# Load the API twitter secret key 
load_dotenv()
APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.getenv("OAUTH_TOKEN_SECRET")

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
# Example how to update status on twitter:
# twitter.update_status(status='')

# Constants:
# Comments made by the publisher that need to be removed.
BEGINNING_PUBLISHER_COMMENT = 1000
END_PUBLISHER_COMMENT = 18753
# Range of book ids, there are 1300 that are publicly available on project Gutenberg
SMALEST_BOOK_ID = 10
LARGEST_BOOK_ID = 1300
# Tweet size:
SMALEST_TWEET_SIZE = 15
LARGEST_TWEET_SIZE = 276



# This function:
# 1) Generates random int within the range of book ids.
# 2) Generates a url with the book id.
# 3) 
def get_book():
	

	url_is_OK = False
	while url_is_OK == False:

		random_book_number = random.randint(SMALEST_BOOK_ID, LARGEST_BOOK_ID)
		random_book_number = str(random_book_number)
		url = 'http://www.gutenberg.org/files/'+random_book_number+'/'+random_book_number+'.txt'
		print(url)		

		#Check if the url is OK. If for some reason the url is broken it will generate a new link.
		try:
			response = urlopen(url)
			raw = response.read().decode('utf8')
			url_is_OK = True
			
			return raw

		except Exception:
			print('error')
			pass

def get_quote(book):

	random_index=random.randint(BEGINNING_PUBLISHER_COMMENT,(len(book)-END_PUBLISHER_COMMENT))
	temp = random_index	

	quote_forward=''
	quote_backward=''

	while book[random_index]!='.':

		quote_backward=quote_backward+(book[random_index])
		random_index = random_index-1

	random_index=temp

	while book[random_index]!='.':

		quote_forward=quote_forward+(book[random_index])
		random_index = random_index+1

	complete_quote=quote_backward[::-1]+quote_forward

	return complete_quote


book=get_book()
book=repr(book)
book=book.replace("\\r\\n",'*')


#get title 
title_start = book.find('Title')
condition=0
j=7
i=book[title_start+j]
title=''

while condition == 0:	
	
 	if(i=='*'):
 		condition=1
 	else:
 		j+=1
 		
 		title=title+i
 		i=book[title_start+j]


#get author, put unknown if cant find author 
author_start = book.find('Author')
if author_start != -1:
	condition=0
	j=8  
	i=book[author_start+j]
	author=''

	while condition == 0:
		
	 	if(i=='*'):
	 		condition=1
	 	else:
	 		j+=1
	 		author=author+i
	 		i=book[author_start+j]
else:
	author='Unknown'

condition = 0
while condition == 0:
	 quote_of_the_day = get_quote(book)

	 if len(quote_of_the_day+title+author)<LARGEST_TWEET_SIZE and len(quote_of_the_day+title+author)>SMALEST_TWEET_SIZE:
	 	condition = 1
	 		
print(title)
print(author)
print(quote_of_the_day)


twitter.update_status(status=title+', '+author+'\n'+quote_of_the_day)