
# coding: utf-8

# # Youtuber Playlist Video List

# In[34]:


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


# In[40]:


youtube_address = "https://www.youtube.com"
user_name = "PONY Syndrome"
user_address = "https://www.youtube.com/channel/UCT-_4GqC-yLY1xtTHhwY0hA"
youtuber_playlist_video_list_path = "../csv/youtuber_playlist_video_list.csv"


# In[4]:


tabs_info_script = "return window['ytInitialData']['contents']['twoColumnBrowseResultsRenderer']['tabs']"
playlist_tabs_script = "{}[2]['tabRenderer']['endpoint']['commandMetadata']['webCommandMetadata']['url']".format(tabs_info_script)
playlist_item_script = "{}[2]['tabRenderer']['content']['sectionListRenderer']['contents'][0]                         ['itemSectionRenderer']['contents'][0]['gridRenderer']['items']".format(tabs_info_script)

item_script = "{}[0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']                 ['contents'][0]['playlistVideoListRenderer']['contents']".format(tabs_info_script)


# In[5]:


driver = webdriver.Firefox()


# In[6]:


driver.get(user_address)
playlist_tabs = youtube_address + driver.execute_script(playlist_tabs_script)


# In[7]:


driver.get(playlist_tabs)
playlist = driver.execute_script(playlist_item_script)


# In[32]:


playlist_video_list = []
for item in playlist:
    playlist_title = item['gridPlaylistRenderer']['title']['runs'][0]['text']
    playlist_url = youtube_address + item['gridPlaylistRenderer']['viewPlaylistText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']

    driver.get(playlist_url)
    playlist_item_list = driver.execute_script(item_script)
    for item in playlist_item_list:
        video_title = item['playlistVideoRenderer']['title']['simpleText']
        video_address = youtube_address + item['playlistVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        video_thumbnail = item['playlistVideoRenderer']['thumbnail']['thumbnails'][0]['url']
        video_thumbnail = video_thumbnail.split('?sqp')[0].replace('hqdefault.jpg', 'maxresdefault.jpg').replace("//s", "https://s")
        
        playlist_video_list.append([user_name, playlist_title, playlist_url, video_title, video_address, video_thumbnail])


# In[41]:


column_list = ["youtuber_name", "playlist_title", "playlist_url", "video_title", "video_address", "video_thumbnail"]
youtuber_playlist_video_list_df = pd.DataFrame(playlist_video_list, columns=column_list)
youtuber_playlist_video_list_df.to_csv(youtuber_playlist_video_list_path, encoding="utf-8", index=False)
youtuber_playlist_video_list_df.head(10)

