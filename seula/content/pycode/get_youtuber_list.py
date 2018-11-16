
# coding: utf-8

# In[1]:


from selenium import webdriver
from bs4 import BeautifulSoup # import urllib
import time 
import pandas as pd


# In[2]:


driver = webdriver.Firefox()
youtube_address = "https://www.youtube.com"


# # Search Channel

# In[3]:


query = "뷰티"
query_url = "https://www.youtube.com/channels?q={}&page=".format(query)
csv_path = "../csv/channel_list.csv"


# In[4]:


driver.get(query_url)
source = driver.page_source
bs = BeautifulSoup(source, "html.parser")


# In[5]:


url_list = bs.find_all("a", {"class" : " yt-uix-sessionlink"})


# In[6]:


channel_list = []
for url in url_list:
    channel_list.append([url.getText(), youtube_address + url['href'], None])


# In[7]:


channel_list_df = pd.DataFrame(channel_list, columns = ['channel_name', 'channel_address', 'subscribers_num'])
channel_list_df.head(5)


# In[8]:


for i, row in channel_list_df.iterrows():
    driver.get(row["channel_address"])
    time.sleep(5)
    
    source = driver.page_source
    bs = BeautifulSoup(source, "html.parser")
    
    subscribers = bs.find_all("yt-formatted-string", {"class" : "style-scope ytd-c4-tabbed-header-renderer"})[1].getText()
    subscribers = subscribers.replace("구독자 ", "").replace(",", "").replace("명", "")
    
    if subscribers is '':
        channel_list_df["subscribers_num"][i] = 0
    else:
        channel_list_df["subscribers_num"][i] = int(subscribers)
        
channel_list_df.head(5)


# In[10]:


channel_list_df = channel_list_df.sort_values(by="subscribers_num", ascending=False)
channel_list_df.to_csv(csv_path, encoding="utf-8", index=False)
channel_list_df.head(5)


# # Search Video

# In[11]:


query = "메이크업"
query_url = "https://www.youtube.com/results?search_query=" + query
csv_path = "../csv/youtuber_list.csv"


# In[12]:


driver.get(query_url)
source = driver.page_source
bs = BeautifulSoup(source, "html.parser")


# In[13]:


# ("a", {"class", "yt-uix-button vve-check yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default"})
# ("a", {"class" : "g-hovercard yt-uix-sessionlink spf-link "})
url_list = bs.find_all("a", {"class", "yt-simple-endpoint style-scope yt-formatted-string"})


# In[14]:


youtuber_list = []
for url in url_list:
    youtuber_list.append([url.getText(), youtube_address + url['href'], None])


# In[20]:


youtuber_list_df = pd.DataFrame(youtuber_list, columns = ['user_name', 'user_address', 'videos_address'])
youtuber_list_df.head(5)


# In[21]:


for i, row in youtuber_list_df.iterrows():
    driver.get(row["user_address"])
    time.sleep(5)
    
    tabs_info = "return window['ytInitialData']['contents']['twoColumnBrowseResultsRenderer']['tabs']"
    video_tabs = driver.execute_script(tabs_info)[1]['tabRenderer']['endpoint']['commandMetadata']['webCommandMetadata']['url']
    
    youtuber_list_df["videos_address"][i] = youtube_address + video_tabs


# In[22]:


youtuber_list_df.to_csv(csv_path, encoding="utf-8", index=False)
youtuber_list_df.head(5)


# In[23]:


driver.quit()

