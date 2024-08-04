from  urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

# pip install urlextract
# pip install emoji
extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch words
    words = []
    for loop in df['message']:
        words.extend(loop.split())

    # fetch  media message

    media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # fetch links
    links = []
    for link in df['message']:
        links.extend(extract.find_urls(link))

    return df.shape[0], len(words),media_messages,len(links)

def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()

    df = round(df[df['user']!='group_notification']['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','count':'percent'})
    return  x , df

def create_word_Cloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    f = open('stop_hinglish.txt')
    stop_words = f.read()

    temp = df[df['user']!='group_notification']
    temp = temp[temp['message']!='<Media omitted>']

    # def remove_stop_words(message):
    #     words = []
    #     for messagesss in message:
    #         for word in messagesss.lower().split():
    #             if word not in stop_words:
    #                 words.append(word)
    #     return ' '.join(words)

    # temp['message'] = temp['message'].apply(remove_stop_words)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    df_wc = wc.generate(temp['message'].str.cat(sep =''))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user']!='group_notification']
    temp = temp[temp['message']!='<Media omitted>']

    words = []
    f = open('stop_hinglish.txt')
    stop_words = f.read()
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    df = pd.DataFrame(Counter(words).most_common(20))
    return df


def find_emojis(selected_user , df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Initialize list to store emojis
    emojis = []

    # Access the emoji data dictionary
    emoji_data = emoji.EMOJI_DATA if hasattr(emoji, 'EMOJI_DATA') else emoji.UNICODE_EMOJI_ENGLISH

    # Iterate through each message in the DataFrame
    for message in df['message']:
        # Extract emojis from the message
        emojis.extend([c for c in message if c in emoji_data])

    return pd.DataFrame(Counter(emojis).most_common(len(emojis)))

def monthly_timeline(selected_user,df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-"+str(timeline["year"][i]))
    timeline['time']  = time
    return timeline

def daily_timeline(selected_user,df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity_map(selected_user,df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return  df['day_name'].value_counts()


def monthly_activity_map(selected_user,df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return  df['month'].value_counts()

def activity_heat_map(selected_user,df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_map = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_map

#
