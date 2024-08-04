import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader('choose a file')

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    bytes_data = bytes_data.decode('utf-8')
    data = preprocessor.preprocess(bytes_data)
    # st.dataframe(data)

    # fetch unique user

    user_list  = data['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button('show analysis'):
        num_messages,words,media_messages,links = helper.fetch_stats(selected_user,data)
        st.title('Top Statistics')

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(media_messages)
        with col4:
            st.header('Links')
            st.title(links)

        # timelines

        # monthly time line
        st.title('Monthly Timeline')
        time_line = helper.monthly_timeline(selected_user,data)
        fig, axes = plt.subplots()
        axes.plot(time_line['time'], time_line['message'],color='green')
        plt.xticks(rotation='vertical')
        # fig.autofmt_xdate()
        st.pyplot(fig)

        # daily time line
        st.title('Daily Timeline')
        dailytime_line = helper.daily_timeline(selected_user, data)
        fig, axes = plt.subplots()
        axes.plot(dailytime_line['only_date'], dailytime_line['message'], color='green')
        plt.xticks(rotation='vertical')
        # fig.autofmt_xdate()
        st.pyplot(fig)

        # activity map

        st.title('activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most busy Weeks')
            busy_day = helper.weekly_activity_map(selected_user,data)
            fix,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values,color='black')
            st.pyplot(fix)
        with col2:
            st.header('Most busy Months')
            busy_day = helper.monthly_activity_map(selected_user,data)
            fix,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values,color='orange')
            st.pyplot(fix)

        st.title('Weekly Heat Map')
        activity = helper.activity_heat_map(selected_user,data)
        fig,ax = plt.subplots()
        ax  = sns.heatmap(activity)
        st.pyplot(fig)


        # find the most busiest user in the group
        if selected_user == 'Overall':
            st.title('most busy users')
            users, new_df = helper.fetch_most_busy_users(data)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(users.index, users.values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # word cloud generator

        st.title('Most used words in the chat')
        wc = helper.create_word_Cloud(selected_user,data)
        fig,ax = plt.subplots()
        ax.imshow(wc)
        st.pyplot(fig)

        # most comman words
        st.title('Most Common Words')
        common_words = helper.most_common_words(selected_user,data)
        fig,axes = plt.subplots()
        axes.barh(common_words[0],common_words[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # fetch emojis

        col1,col2 = st.columns(2)

        df = helper.find_emojis(selected_user, data)
        with col1:
            st.title('Emoji Analysis')
            st.dataframe(df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(df[1].head(),labels=df[0].head(),autopct="%0.2f")
            st.pyplot(fig)




        a=1
