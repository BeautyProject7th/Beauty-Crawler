
# coding: utf-8

# # Videos Information
# * update, description

# In[8]:


import pandas as pd
from selenium import webdriver
import time


# In[9]:


youtuber_video_list_path = "../csv/youtuber_video_list.csv"
youtuber_video_info_path = "../csv/youtuber_videos_info.csv"


# In[3]:


youtuber_video_list_df = pd.read_csv(youtuber_video_list_path, encoding="utf-8")
youtuber_video_list_df.head(3)


# In[4]:


column_list = ['youtuber_name', 'video_title', 'video_address', 'video_thumbnail', 'video_updated', 'video_description']
youtuber_video_info_df = pd.DataFrame(youtuber_video_list_df, columns=column_list)
youtuber_video_info_df.head(3)


# In[5]:


video_info_script = "return window['ytInitialData']['contents']['twoColumnWatchNextResults']                     ['results']['results']['contents'][1]['videoSecondaryInfoRenderer']"
date_script = "{}['dateText']['simpleText']".format(video_info_script)
description_script = "{}['description']['runs']".format(video_info_script)


# 1. Date : 영상과 스트리밍 구분
#     - 영상 - "게시일: 2017. 10. 31."
#     - 스트리밍 - "실시간 스트리밍 시작일: 2017. 10. 31."
# 2. Description
#     - Description이 없는 경우
#         - 스트리밍
#         - 작성하지 않음
#     - Description내에 link가 포함된 경우(줄여서 포함되는 경우도 종종 있음)
#     
#     
# - ~~비공개/삭제 동영상 확인~~  
#     - ~~동영상을 볼 수 없습니다.(Content Warning)~~
#     - ~~동영상이 사용자에 의해 삭제되었습니다.(Removed by the user)~~
# - ~~페이지 언어 변경~~
# - ~~Description 5글자 미만 확인(1글자 or 2글자)~~
# - ~~Description에 link가 포함된 경우(\<a href)~~
# 

# In[50]:


driver = webdriver.Firefox()


# In[52]:


date_list = []
description_list = []

for i, row in youtuber_video_info_df.iterrows():
    driver.get(row['video_address'])
    time.sleep(3)
    
    date_info_list = driver.execute_script(date_script).split(': ')
    date_info = date_info_list[0]
    date = date_info_list[1].replace(". ", "/").replace(".", "")
    
    description = ""
    try:        
        description_text_list = driver.execute_script(description_script)
        for text in description_text_list:
            description += text['text']
    except:
        pass
        
    date_list.append(date)
    description_list.append(description)


# In[ ]:


driver.quit()


# In[71]:


from IPython.display import clear_output

check_description = youtuber_video_info_df['video_description'].values
for description in check_description:
    clear_output()
    print(description)


# In[57]:


youtuber_video_info_df['video_updated'] = date_list
youtuber_video_info_df['video_description'] = description_list
youtuber_video_info_df.to_csv(youtuber_video_info_path, encoding="utf-8", index=False)
youtuber_video_info_df.head(5)

