#!/usr/bin/env python
# coding: utf-8

# # WeatherAPI (Weather)
# 
# Answer the following questions using [WeatherAPI](http://www.weatherapi.com/). I've added three cells for most questions but you're free to use more or less! Hold `Shift` and hit `Enter` to run a cell, and use the `+` on the top left to add a new cell to a notebook.
# 
# Be sure to take advantage of both the documentation and the API Explorer!
# 
# ## 0) Import any libraries you might need
# 
# - *Tip: We're going to be downloading things from the internet, so we probably need `requests`.*
# - *Tip: Remember you only need to import requests once!*

# In[1]:


import requests


# ## 1) Make a request to the Weather API for where you were born (or lived, or want to visit!).
# 
# - *Tip: The URL we used in class was for a place near San Francisco. What was the format of the endpoint that made this happen?*
# - *Tip: Save the URL as a separate variable, and be sure to not have `[` and `]` inside.*
# - *Tip: How is north vs. south and east vs. west latitude/longitude represented? Is it the normal North/South/East/West?*
# - *Tip: You know it's JSON, but Python doesn't! Make sure you aren't trying to deal with plain text.* 
# - *Tip: Once you've imported the JSON into a variable, check the timezone's name to make sure it seems like it got the right part of the world!*

# In[2]:


vasai_url = "https://api.weatherapi.com/v1/current.json?key=e9e2ab61a22a4e12b81111053221506&q=Vasai&aqi=no"


# In[3]:


response_vasai = requests.get(vasai_url)


# In[4]:


vasai_weather = response_vasai.json()


# ## 2) What's the current wind speed? How much warmer does it feel than it actually is?
# 
# - *Tip: You can do this by browsing through the dictionaries, but it might be easier to read the documentation*
# - *Tip: For the second half: it **is** one temperature, and it **feels** a different temperature. Calculate the difference.*

# In[5]:


print(f"The current wind speed is {vasai_weather['current']['wind_kph']} kilometres per hour")


# In[6]:


diff=vasai_weather['current']['temp_c']-vasai_weather['current']['feelslike_c']


# In[7]:


if diff>0:
    print(f"It feels {diff:.1f} degrees colder in {vasai_weather['location']['name']}")
else:
    print(f"It feels {abs(diff):.1f} degrees warmer in {vasai_weather['location']['name']}")


# ## 3) What is the API endpoint for moon-related information? For the place you decided on above, how much of the moon will be visible tomorrow?
# 
# - *Tip: Check the documentation!*
# - *Tip: If you aren't sure what something means, ask in Slack*

# The API endpoint for moon-related information is https://api.weatherapi.com/v1/astronomy.json. For data on moon's visibility tomorrow, changing the date of request

# In[8]:


vasai_moon= "https://api.weatherapi.com/v1/astronomy.json?key=e9e2ab61a22a4e12b81111053221506&q=vasai&dt=2022-06-19"


# In[9]:


response_moon= requests.get(vasai_moon)


# In[10]:


moon= response_moon.json()


# As per the documentation, data on moon illumination is in the 'astro' key within the 'astronomy' key of the directory we requested. Printing that out.

# In[11]:


print(f"{moon['astronomy']['astro']['moon_illumination']}% of moon will be visible tomorrow")


# ## 4) What's the difference between the high and low temperatures for today?
# 
# - *Tip: When you requested moon data, you probably overwrote your variables! If so, you'll need to make a new request.*

# I did not rewrite the variables so do not have to make a new request. But data on high and low temperatures are in the Forecast API. Requesting that

# In[12]:


forecast_url="https://api.weatherapi.com/v1/forecast.json?key=e9e2ab61a22a4e12b81111053221506&q=vasai&days=3&aqi=no&alerts=no"


# In[13]:


response_forecast=requests.get(forecast_url)


# In[14]:


vasai_forecast=response_forecast.json()


# As per the documentation, maximum and minimum temperatures are in the 'day' element inside 'forecastday' list in 'forecast' dictionary. Extracting the data

# In[15]:


max_temp=vasai_forecast['forecast']['forecastday'][0]['day']['maxtemp_c']
min_temp=vasai_forecast['forecast']['forecastday'][0]['day']['mintemp_c']
difference=(max_temp-min_temp)


# In[16]:


print(f"The difference between the high and low temperatures for today is {difference:.2f} degree celsius")


# ## 4.5) How can you avoid the "oh no I don't have the data any more because I made another request" problem in the future?
# 
# What variable(s) do you have to rename, and what would you rename them?

# I renamed the variables every time I made a request and will continue to do so to avoid this problem

# ## 5) Go through the daily forecasts, printing out the next three days' worth of predictions.
# 
# I'd like to know the **high temperature** for each day, and whether it's **hot, warm, or cold** (based on what temperatures you think are hot, warm or cold).
# 
# - *Tip: You'll need to use an `if` statement to say whether it is hot, warm or cold.*

# I requested next three days' predictions for the previous question. Printing data on temperatures from that and adding conditionals based on my idea of what is hot, warm and cold. I have assigned all temperatures above 30 degree celsius to be hot, all below 16 degree celsius to be cold and everything else warm.

# In[17]:


for day in vasai_forecast['forecast']['forecastday']:
    if day['day']['maxtemp_c']>=30:
        print(f"The high temperature for {day['date']} is {day['day']['maxtemp_c']} degree celsius. That is hot!")
    elif day['day']['maxtemp_c']<=16:
        print(f"The high temperature for {day['date']} is {day['day']['maxtemp_c']} degree celsius. That is cold!")
    else:
        print(f"The high temperature for {day['date']} is {day['day']['maxtemp_c']} degree celsius. That is warm.")


# ## 5b) The question above used to be an entire week, but not any more. Try to re-use the code above to print out seven days.
# 
# What happens? Can you figure out why it doesn't work?
# 
# * *Tip: it has to do with the reason you're using an API key - maybe take a look at the "Air Quality Data" introduction for a hint? If you can't figure it out right now, no worries.*

# The free version of the API only provides data for 3 days as stated on the [pricing page](https://www.weatherapi.com/pricing.aspx)

# ## 6) What will be the hottest day in the next three days? What is the high temperature on that day?

# First, creating a list comprehension and using the max function on it to find out the max value of highest temperatures.

# In[18]:


highest_temp=max([day['day']['maxtemp_c'] for day in vasai_forecast['forecast']['forecastday']])


# Now, creating a conditional to find the hottest day in the next three days

# In[19]:


for day in vasai_forecast['forecast']['forecastday']:
    if day['day']['maxtemp_c']==highest_temp:
        print(f"The hottest day in the next three days will be {day['date']} with a maximum temperature of {day['day']['maxtemp_c']}")


# ## 7) What's the weather looking like for the next 24+ hours in Miami, Florida?
# 
# I'd like to know the temperature for every hour, and if it's going to have cloud cover of more than 50% say "{temperature} and cloudy" instead of just the temperature. 
# 
# - *Tip: You'll only need one day of forecast*

# Requesting one day forecast data for Miami

# In[20]:


miami_url="https://api.weatherapi.com/v1/forecast.json?key=e9e2ab61a22a4e12b81111053221506&q=miami&days=1&aqi=no&alerts=no"


# In[21]:


response_miami=requests.get(miami_url)


# In[22]:


miami_data=response_miami.json()


# Creating a for loop for the list called 'hour' which has data on hourly forecasts. Also added a conditional based on the element 'cloud' which has cloud coverage data as %

# In[23]:


print(f"Here is the hourly forecast for Miami for the next 24 hours.")
for hours in miami_data['forecast']['forecastday'][0]['hour']:
    if (hours['cloud'])>50:
        print(f"{hours['time']}: {hours['temp_c']} and cloudy")
    else:
        print(f"{hours['time']}: {hours['temp_c']}")
          


# ## 8) For the next 24-ish hours in Miami, what percent of the time is the temperature above 85 degrees?
# 
# - *Tip: You might want to read up on [looping patterns](http://jonathansoma.com/lede/foundations-2017/classes/data%20structures/looping-patterns/)*

# I am assuming you of course mean 85 degree fahrenheit. Assigning a 0 value to count and then creating a conditional for the 'temp_f' element in the 'hour' list

# In[24]:


count=0
for hours in miami_data['forecast']['forecastday'][0]['hour']:
    if hours['temp_f']>85:
        count=count+1


# Now, calculating percentage by dividing count by 24 and multiplying by 100.

# In[25]:


print(f"For the next 24-ish hours in Miami, the temperature will be above 85 degrees fahrenheit {count/24*100:.1f}% of the time")


# ## 9) How much will it cost if you need to use 1,500,000 API calls?
# 
# You are only allowed 1,000,000 API calls each month. If you were really bad at this homework or made some awful loops, WeatherAPI might shut down your free access. 
# 
# * *Tip: this involves looking somewhere that isn't the normal documentation.*

# It would cost $4 per month to be able to use 1.5 million API calls. It is mentioned on the [pricing page](https://www.weatherapi.com/pricing.aspx)

# ## 10) You're too poor to spend more money! What else could you do instead of give them money?
# 
# * *Tip: I'm not endorsing being sneaky, but newsrooms and students are both generally poverty-stricken.*

# I think the best option would be to create multiple (would only need 2 if we only need 1.5 million calls) and split the requests between those IDs so that it would be equally distributed. This way, around 750,000 requests can be used on 1 ID.
