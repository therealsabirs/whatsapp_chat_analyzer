import re
import pandas as pd

def preprocess(data):
    # Define a regex pattern to find timestamps in the format '[dd/mm/yy, HH:MM:SS] '
    pattern = r'\[\d{2}\/\d{2}\/\d{2}, \d{2}:\d{2}:\d{2}\]\s'
    
    # Split the data based on the pattern to isolate messages
    messages = re.split(pattern, data)[1:]
    # Find all timestamps
    dates = re.findall(pattern, data)

    # Create a DataFrame with messages and their corresponding dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Convert the message_date column to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='[%d/%m/%y, %H:%M:%S] ')
    
    # Rename the message_date column to date
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    users = []
    messages = []
    for message in df['user_message']:
        # Split each message to separate user name and message content
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # If user name is present
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            # If the message is a group notification
            users.append('group_notification')
            messages.append(entry[0])

    # Add user and message columns to the DataFrame
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    # Extract various date and time components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    # Create a period column to represent hour ranges
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour+1}")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df
