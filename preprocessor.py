import pandas as pd
import re

def preprocess(data):
    # Regular expression pattern to match date and message
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[AP]M\s*-\s*'

    # Extract dates using re.findall
    dates = re.findall(pattern, data)

    # Extract messages using re.split, remove the first empty string
    messages = re.split(pattern, data)[1:]

    # Remove any leading or trailing whitespace from messages
    messages = [message.strip() for message in messages]

    # Create a DataFrame
    df = pd.DataFrame({'date': dates, 'message': messages})
    df['date'] = df['date'].str.replace(' - ', '')
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p')
    # seperate username and message

    users = []
    messages_list = []

    for messages in df['message']:
        entry = re.split('([\w\W]+?):\s', messages)
        if entry[1:]:
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df.drop(columns=['message'], inplace=True)
    df['message'] = messages_list

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period
    return df


