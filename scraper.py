import praw
import re
import os
from collections import Counter #for getting word counts
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv, dotenv_values

#load env variables
load_dotenv()

#create connection to reddit
reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"), user_agent=os.getenv("USER_AGENT"))

#take user input
print("--------------------------\nREDDIT POST WORD-COUNTER\n--------------------------\nHOW TO USE:")
print("\nEnter the name of a valid subreddit to get the count of all words used in the bodies of each of the 15 hottest posts on that thread\n\n")
subname = input("Enter a subreddit name to get the most commonly used words!: ")
posts=reddit.subreddit(subname).hot(limit=15)

title_list = []
#since posts is not a list and we can't check the length,
# we will just put a try-catch around our title processing
try:
    for post in posts:
        title_list.append(post.selftext)
except:
    print("Subreddit does not exist or experienced an error", end="\n"*2)


#process text and get a collection of words with their counts
#Use the Counter from collections
#I want to remove common words "the", "and", etc., also known as stop words
title_texts = ""
for t in title_list:
    title_texts += t + " "
#remove punctuation
title_texts = re.sub(r'[^\w\s]', '', title_texts)
tok_text = word_tokenize(title_texts)

filtered = [word for word in tok_text if not word.lower() in stopwords.words()]


#create dict that has words with counts
word_counts = Counter(filtered)
count = 1
for word in word_counts:
    print(word, word_counts[word], end="   ")
    if count % 10 == 0:
        print ("\n")
    count+=1

#this can use cleaning
# I can do:
#remove more stop words??
#de-pluralize words
#remove contractions
#add options for title or body or both