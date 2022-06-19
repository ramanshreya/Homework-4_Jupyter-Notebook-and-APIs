#!/usr/bin/env python
# coding: utf-8

# # Last FM API (Music)
# 
# Spotify's API is dead to us, so we're using Last.fm's - it's still music, just not as nice of an API.
# 
# 1. Create an account at https://www.last.fm/api/
# 2. Create an "application" to get a key: https://www.last.fm/api/account/create
#     - It isn't a real application, it's just your project
#     - Name/description doesn't matter, ignore callback key and callback url
# 3. And save the API key that shows up on the next screen
# 
# You can find documentation at https://www.last.fm/api/
# 
# The domain for the API is `http://ws.audioscrobbler.com`, so all of your endpoints will be connected to that. To test your API key, check the following URL in your browser: `http://ws.audioscrobbler.com/2.0/?method=artist.search&artist=cher&api_key=XXXXXXXXXXXXXXXXXXXX&format=json` (change the `XXXXXX` to be your API key, of course!).
# 
# > Last.fm used to be called **AudioScrobbler**, which is why its URLs don't have "last.fm" in them.
# > While we're asking about URLs, notice that the API endpoints have a lot of `?` and `&` in them - these are key/value pairs, kind of like dictionaries, but for URLs instead of Python.

# # FIRST: SETUP

# ## 1) Import the libraries/packages you might need
# 
# We need a library to read in the data for us! We don't like `urllib2`, so it must be something cooler and better.

# In[1]:


import requests


# ## 2) Save your API key
# 
# Write your API key here so you don't forget it - it's the "api key" one, not the "shared secret" one
# 

# **8cf2c54479961787b9d765bca8e5c5f9**

# ## 3) The death of an API
# 
# I used to have some code here that allowed you to display images, but _the images don't work any more._ Let this be an important lesson: when you depend on external services, they can die at any time.

# :( :( :(

# # NOW: YOUR ASSIGNMENT

# ## 1) Search for and print a list of 50 musicians with `lil` in their name, along with the number of listeners they have
# 
# There are a lot of musicians with "Lil" in their name - it used to be all Lil Wayne and Lil Kim, but we live in a new world now!
# 
# - *Tip: Remember, the domain for the API is `http://ws.audioscrobbler.com`*
# - *Tip: Make sure you ask the API for 50 musicians! This involves adding another parameter to the URL - notice they all have a `&` before them. [Read the documentation](http://www.last.fm/api/show/artist.search) to find the parameter's name.* 
# - *Tip: When you are looking at any piece of data - is it a dictionary? Look at the keys! Is it a list? Look at the first element!*
# - *Tip: LOOK AT THE KEYS. and then the other keys and the other keys and the other keys. It's an ugly series of dictionaries!*

# Making a request for artists with lil in their name and used the parameter called 'limit' to limit the number of entries to 50

# In[2]:


lil_url="http://ws.audioscrobbler.com/2.0/?method=artist.search&artist=lil&limit=50&api_key=8cf2c54479961787b9d765bca8e5c5f9&format=json"


# In[3]:


response_lil=requests.get(lil_url)


# In[4]:


lil_data=response_lil.json()


# The requested data is a dictionary with one key called 'results' which is a dictionary with 6 keys, mostly with data on the query and the result. There is a key called 'artistmatches' which is a dictionary with one key called 'artists' which is a list with details on the artists including name and number of listeners. Printing that out using a for loop

# In[5]:


for artist in lil_data['results']['artistmatches']['artist']:
    print(f"{artist['name']} has {artist['listeners']} listeners")


# Your results should begin something like this:
#     
# ```
# Lil' Wayne has 3086628 listeners
# Lily Allen has 2074266 listeners
# Lil B has 194116 listeners
# Lilly Wood & The Prick has 359886 listeners
# Lil Ugly Mane has 31955 listeners
# LIL UZI VERT has 88517 listeners
# ```

# ## 2) How many listeners does your list have in total?
# 
# The answer should be roughly **15,000,000**. If it's lower, make sure you have 50 artists instead of 30 artists.
# 
# - *Tip: What's the data type of the `listeners` count? It's going to cause a problem!*
# - *Tip: If you were crazy you could use sum and a list comprehension. But you really don't have to!*

# Creating a list comprehension for number of listeners. The number of listeners is a string value. Converting that into integers so that I can use the sum function

# In[6]:


listeners=[int(artist['listeners'])for artist in lil_data['results']['artistmatches']['artist']]


# In[7]:


print(f"The list has a total of {sum(listeners):,} listeners")


# ## 3) Show each artist's name and the URL to the extra-large image
# 
# The images don't work any more, but we'll print their URLs out anyway.

# Each artist **has a list of images of different sizes**. We're interested in the second-to-last one, where `size` is `extralarge`. Print their name and use `display_image` to display their extra-large image.
# 
# - *Tip: The URL should look like this: `https://lastfm-img2.akamaized.net/i/u/300x300/0fc7d7a1812dc79e9925d80382cde594.png`*
# - *Tip: You can always assume it's the second to the last, or assume it's `extralarge`, or whatever you want to do to find it.*
# - *Tip: Make sure the URL is correct before you try to display it.*
# 
# Your output should look something like
# 
# ```
# Lil' Wayne
# https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png
# ---
# LIL UZI VERT
# https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png
# ---
# Lily Allen
# https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png
# ---
# ```
# 
# (but with more people, obviously)

# In the list called 'artist', there is dictionary with a key called 'image' which is a list. Inside this list, the fourth element has the link for extralarge sized images. Printing that out with the name

# In[8]:


for artist in lil_data['results']['artistmatches']['artist']:
    print(artist['name'])
    print(artist['image'][3]['#text'])
    print("---")


# ## 4) Find Lil Jon's `mbid` (or anyone else's!).
# 
# Oftentimes in an API, you can do a few things: you can **search** for items, and you can **see more information** about items. To find more information about the item, you need to use their **unique id**. In this dataset, it's called an `mbid` (MusicBrainz, I think - another company associated with last.fm!).
# 
# Go through the artists and print their **name and mbid**. Find Lil Jon's `mbid`. I *wanted* Lil Uzi Vert's, but for some reason it isn't there. Then I wanted us to look at Lily Allen's, but I just couldn't bring myself to do that. If you'd rather do someone else, go for it.

# In[9]:


for artist in lil_data['results']['artistmatches']['artist']:
    if artist['name']=='Lil Wayne':
        print(f"Lil Wayne's mbid is {artist['mbid']}")


# ## 5) Find the artist's name and bio using their `mbid`.
# 
# It can either be Lil Jon or whoever you selected above.
# 
# If you look at the [last.fm documentation](http://www.last.fm/api/show/artist.getInfo), you can see how to use the artist's `mbid` to find more information about them. Print **every tag associated with your artist**.
# 
# - *Tip: It's a new request to the API*
# - *Tip: Use the `mbid`, and make sure you delete the `&name=Cher` from the sample endpoint*
# - *Tip: If you use `print` for the bio it looks a little nicer than it would otherwise*

# Requesting details on Lil Wayne based on the mbid

# In[10]:


mbid_url="http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid=ac9a487a-d9d2-4f27-bb23-0f4686488345&api_key=8cf2c54479961787b9d765bca8e5c5f9&format=json"


# In[11]:


response_mbid=requests.get(mbid_url)


# In[12]:


mbid_data=response_mbid.json()


# Printing out the bio of the artist

# In[13]:


print(mbid_data['artist']['bio']['summary'])


# ## 6) Print every tag of that artist

# Printing the name of the tags associated with Lil Wayne.

# In[14]:


for tag in mbid_data['artist']['tags']['tag']:
    print(tag['name'])


# # GETTING A LITTLE CRAZY
# 
# So you know your original list of musicians? I want to get tag data for ALL OF THEM. How are we going to do that?
# 
# ## 7) Find the mbids (again)
# 
# If we have a musician with an mbid of `AAA-AAA-AAA`, we get their info from a url like `http://ws.audioscrobbler.com/blahblah/?api_key=12345&mbid=AAA-AAA-AAA`.
# 
# |artist|url|
# |---|---|
# |`AAA-AAA-AAA`|`http://ws.audioscrobbler.com/blahblah/?api_key=12345&mbid=AAA-AAA-AAA`|
# |`BBB-BBB-BBB`|`http://ws.audioscrobbler.com/blahblah/?api_key=12345&mbid=BBB-BBB-BBB`|
# |`CCC-CCC-CCC`|`http://ws.audioscrobbler.com/blahblah/?api_key=12345&mbid=CCC-CCC-CCC`|
# 
# I guess we should start trying to get a list of all of the mbids.
# 
# **Loop through your artists, and print out the `mbid` for each artist**
# 
# - *Tip: You probably need to request your artist search result data again, because you probably saved over `data` with your other API request. Maybe call it `artist_data` this time?*
# - *Tip: If the artist does NOT have an `mbid`, don't print it.*

# Printing artist's mbid from the first request dictionary called lil_data. Added a conditional to print only the mbids where the field is not empty

# In[15]:


for artist in lil_data['results']['artistmatches']['artist']:
    if artist['mbid']!='':
        print(artist['mbid'])


# Your results should look something like
# 
# ```
# 6e0c7c0e-cba5-4c2c-a652-38f71ef5785d
# 1550f952-c91b-40d7-9b4d-d26a259ee932
# 1b72331b-3a97-4981-a81c-eeee9c275d28
# 5f1adfe1-4d07-4141-b181-79e5d379d539
# a95384b1-6aec-468c-ae0d-8c6daf87c4c2
# bc1b5c95-e6d6-46b5-957a-5e8908b02c1e
# 243c6f61-d83b-4459-bebd-5899df0da111
# ```

# ## 8) Saving those mbids
# 
# For those `mbid` values, instead of printing them out, save them to a new list of just mbid values. Call this list `mbids`.
# 
# - *Tip: Use `.append` to add a single element onto a list*

# First creating a blank list variable called mbids

# In[16]:


mbids=[]


# Copy pasting the same for loop from previous answer. Instead of printing the mbid codes, adding them to the newly created mbids list

# In[17]:


for artist in lil_data['results']['artistmatches']['artist']:
    if artist['mbid']!='':
        mbids.append(artist['mbid'])


# Your results should look something like
# 
# ```['6e0c7c0e-cba5-4c2c-a652-38f71ef5785d',
#  '1550f952-c91b-40d7-9b4d-d26a259ee932',
#  '1b72331b-3a97-4981-a81c-eeee9c275d28',
#  '5f1adfe1-4d07-4141-b181-79e5d379d539',
#  'a95384b1-6aec-468c-ae0d-8c6daf87c4c2',
#  'bc1b5c95-e6d6-46b5-957a-5e8908b02c1e',
#  '243c6f61-d83b-4459-bebd-5899df0da111',
#  '8ba17cf6-bec2-4ae4-9820-b1cda47adc08',
#  'ad29ae1c-2eda-4071-9dc8-31910e7e546c',
#  '3268f062-6e76-480a-a384-e1dd2a276afb',
#  '3ad4f6ec-253f-4050-8849-ca26266edfb8',
#  '9b5ce0c1-1bc0-4ea2-a8d3-f5ee7af9eda8',
#  '981d39fc-bd00-4cc6-ac67-6410f8b89098',
#  'b89f4c50-72f5-48ce-b08c-a643b191b24f',
#  'bc21df5c-3d79-479b-b638-8ddb5ecea403',
#  'c9cd225b-4883-428e-82c2-73e0b6282fb6',
#  '9acaf734-b380-4c48-954c-a2cf1d7990a9',
#  'd4d5ae85-700c-4a55-8a39-7f923da07ef2',
#  '77fafce8-a32f-4d42-bdce-266bbf913cee',
#  '50ad1cde-1536-4268-a55f-e47a7b8280ab',
#  '9803d120-716d-45ba-9eb7-9a120813f908',
#  'b27560ea-2783-4a91-be45-9e8711917562',
#  '194e87c9-b3fe-4fbd-82a7-8c54b4dd4c76',
#  'fd90af91-ed07-4e85-8816-26c954fe5286',
#  '5652bb3e-f225-49de-9637-5aa1539b4a7c']```

# ## 9) Printing our API urls
# 
# To get tag data for each artist, you need to use those `mbid` values to access their artist page on the API. Loop through the mbids, displying the URL you'll need to access.
# 
# - *Tip: You don't want to use a comma when printing, because commas add spaces into your text and URLs can't have that*
# - *Tip: Make sure your URL has `artist.getinfo` in it - if not, you're using the wrong endpoint.*

# In[18]:


for mbid in mbids:
    print(f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={mbid}&api_key=8cf2c54479961787b9d765bca8e5c5f9&format=json")


# Your results should look something like
# 
# ```http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=XXXXX&format=json&mbid=6e0c7c0e-cba5-4c2c-a652-38f71ef5785d
# http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=XXXXX&format=json&mbid=1550f952-c91b-40d7-9b4d-d26a259ee932
# http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=XXXXX&format=json&mbid=1b72331b-3a97-4981-a81c-eeee9c275d28
# http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=XXXXX&format=json&mbid=5f1adfe1-4d07-4141-b181-79e5d379d539
# http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=XXXXX&format=json&mbid=a95384b1-6aec-468c-ae0d-8c6daf87c4c2
# http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=XXXXX&format=json&mbid=bc1b5c95-e6d6-46b5-957a-5e8908b02c1e```

# ## OKAY HERE IS A LITTLE INFORMATION: Using our API urls
# 
# This time instead of just *displaying* the URL, we're going to *request and process it*. **But first I'm going to teach you something.**
# 
# When you're dealing with an API, you don't want to make a million requests, have bad code, and then need to do those million requests again. It's usually best to test your code with a few of the results first.
# 
# So, if we have a list of numbers like this:

# In[19]:


numbers = [4, 5, 6, 7]
numbers


# You can actually say to Python, **give me the first two**, and it will only give you the first two.

# In[20]:


numbers[:2]


# The is **very convenient** with loopng with APIs, because instead of trying to use all FIFTY artists, you can just say "hey, please try this out with 2 of them" and you don't waste time.

# ## 10) Using the first three `mbids`, request the API urls and print the artist's name.
# 
# You built the URLs in the last question, now it's time to use them! Use `requests` etc to grab the URL and get out the artist's name.
# 
# - *Tip: The code is the same as last time you got an artist's name from their info page, it's just going to be inside of a loop*
# - *Tip: USE `PRINT` TO SEE WHAT YOU ARE LOOKING AT!!!!!*

# First, creating a list with all the urls using append function

# In[21]:


urls=[]
for mbid in mbids:
    urls.append(f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={mbid}&api_key=8cf2c54479961787b9d765bca8e5c5f9&format=json")


# Now creating a for loop with the new list to run requests on artists and printing out their names

# In[22]:


for links in urls[:3]:
    url=links
    response=requests.get(url)
    data=response.json()
    
    print(data['artist']['name'])


# ## 11) Using the first three `mbids`, request the API urls and print the artist's name and their tags
# 
# - *Tip: The code is the same as last time you got an artist's name from their info page, it's just going to be inside of a loop*
# - *Tip: It's a for loop in a for loop!*

# In[23]:


for links in urls[:3]:
   url=links
   response=requests.get(url)
   data=response.json()
   
   print(f"Artist name: {data['artist']['name']}")
   for tag in data['artist']['tags']['tag']:
       print(tag['name'])
   print("---")
   


# ## 12) Using the first ten mbids, print the artist's name and whether they're a rapper
# 
# Only print their name ONCE and only print whether they are hip hop or not ONCE.
# 
# - *Tip: Rap tags include hip hop, swag, crunk, rap, dirty south, and probably a bunch of other stuff! You can include as many categories as you'd like.*
# - *Tip: You can use `2 in [1, 2, 3]` to find out if `2` is in the list of `[1, 2, 3]`.*
# - *Tip: Every time you look at a new artist, you can say they are NOT a rapper. And once you find out one of their tags is hip hop or rap, then you can note that they're a rapper. Then once you're done looking at their tags, then you can say HEY this is a rapper, or HEY this is not a rapper.*

# First, creating a list of tags associated with rap and naming it rap_tags. Then assigning "False" value to a variable named rap_yes. Then creating a boolean conditional for the 'rap_yes' variable based on whether tag names match any of the variables in the rap_tag list. Then adding another conditional for printing "YES rap" and "No rap" based on the rap_yes boolean. 
# 
# *(Shoutout to Jasmine Teng for helping me figure this out on slack)*

# In[24]:


for links in urls[:10]:
    url=links
    response=requests.get(url)
    data=response.json()
    
    
    rap_tags=['rap','hip hop','swag','Gangsta Rap','memphis rap','Hip-Hop','Crunk','Dirty South']
    

    print(f"Artist name: {data['artist']['name']}")
    
    rap_yes=False

    for tags in data['artist']['tags']['tag']:
        if tags['name'] in rap_tags:
            rap_yes=True
        else:
            rap_yes=False
            
    if rap_yes:
        print("YES Rap")
    else:
        print("No Rap")
    
      


# Your results might look something like
# 
# ```ARTIST: Lily Allen
# NO hip hop
# ARTIST: Lil B
# YES hip hop
# ARTIST: Lilly Wood & The Prick
# NO hip hop
# ARTIST: Lil Ugly Mane
# YES hip hop
# ARTIST: Lil Jon
# YES hip hop
# ARTIST: Lil' Kim
# YES hip hop
# ARTIST: Lil Jon & The East Side Boyz
# YES hip hop
# ```

# ## 13) What percent of "lil" results are rappers?

# First, counting the number of rappers by copying code from previous answer and changing the printing conditional to one that counts the number of instances where the artists have rap tags

# In[25]:


count=0

for links in urls:
    url=links
    response=requests.get(url)
    data=response.json()
    
    
    rap_tags=['rap','hip hop','swag','Gangsta Rap','memphis rap','Hip-Hop','Crunk','Dirty South']
    
    
    rap_yes=False
    
    for tags in data['artist']['tags']['tag']:
        if tags['name'] in rap_tags:
           rap_yes=True 
            
    if rap_yes:
        count=count+1


# Now calculating the percentage by dividing the count by total number of artists in the lil data list that had mbid code

# In[26]:


perc_rappers=count/len(mbids)*100
print(f"{perc_rappers:.2f}% of 'lil' results with mbid codes are rappers")


# ## 14) Seriously you are all-powerful now.

# YAYYYYY! 
