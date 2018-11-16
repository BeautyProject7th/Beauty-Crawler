
# coding: utf-8

# # Youtuber Video List
# * video_title, video_address, video_thumbnail

# In[1]:


import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time


# In[2]:


youtube_address = "https://www.youtube.com"
youtuber_list_path = "../csv/youtuber_list.csv"
youtuber_video_list_path = "../csv/youtuber_video_list.csv"


# In[3]:


data_script = "return window['ytInitialData']['contents']['twoColumnBrowseResultsRenderer']                 ['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]                 ['itemSectionRenderer']['contents'][0]['gridRenderer']"

scroll_script = "window.scrollTo(0, document.getElementById('items').offsetHeight)"
continue_script = "{}['continuations']['length']".format(data_script)

item_script = "{}['items']".format(data_script)

item_cnt_script = "{}['length']".format(item_script)
item_title_script = "{}[{}]['gridVideoRenderer']['title']['simpleText']"
item_address_script = "{}[{}]['gridVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']"
item_thumbnail_script = "{}[{}]['gridVideoRenderer']['thumbnail']['thumbnails']"


# In[4]:


youtuber_df = pd.read_csv(youtuber_list_path, encoding="utf-8")
youtuber_df.head(3)


# In[5]:


driver = webdriver.Firefox()


# In[6]:


youtuber_video_list = []

for i, row in youtuber_df.iterrows():
    driver.get(row["videos_address"])
    time.sleep(5)
    
    while(True):
        driver.execute_script(scroll_script)
        time.sleep(5)     
        script_result = driver.execute_script(continue_script)
        if script_result == 0:
            break
    
    source = driver.page_source
    bs = BeautifulSoup(source, "html.parser")
    
#     item_list = bs.find_all("a", {"class" : "yt-simple-endpoint style-scope ytd-grid-video-renderer"})[1:]
    item_cnt = driver.execute_script(item_cnt_script)
    youtuber_name = row['user_name']    
    
    for cnt in range(item_cnt):
        video_title = driver.execute_script(item_title_script.format(item_script, cnt))
        video_address = driver.execute_script(item_address_script.format(item_script, cnt))['url']
        video_thumbnail = driver.execute_script(item_thumbnail_script.format(item_script, cnt))[0]['url']
        video_thumbnail = video_thumbnail.split('?sqp')[0].replace('hqdefault.jpg', 'maxresdefault.jpg')
        
        youtuber_video_list.append([youtuber_name, video_title, youtube_address + video_address, video_thumbnail])

    print("{}: {}".format(row['user_name'], item_cnt))
print("TOTAL: {}".format(len(youtuber_video_list)))


# In[8]:


driver.quit()


# In[9]:


column_list = ["youtuber_name", "video_title", "video_address", "video_thumbnail"]
youtuber_video_list_df = pd.DataFrame(youtuber_video_list, columns=column_list)
youtuber_video_list_df.to_csv(youtuber_video_list_path, encoding="utf-8", index=False)
youtuber_video_list_df.head(10)

