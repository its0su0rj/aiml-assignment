
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Loading FILE
log_file_path = "HealthApp_2k.log"






column_names = ["timestamp", "module", "user_id", "action", "value1", "value2", "value3"]

# Reading log file and extracting
data = []

with open(log_file_path, "r") as file:
    for line in file:
        parts = line.strip().split('|')
        if len(parts) >= len(column_names):
            data.append(parts[:len(column_names)])
        else:
            data.append(parts + [''] * (len(column_names) - len(parts)))

# Creating a DataFrame
df = pd.DataFrame(data, columns=column_names)


df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d-%H:%M:%S:%f')


df['user_id'] = df['user_id'].astype('int64')
df[['value1', 'value2', 'value3']] = df[['value1', 'value2', 'value3']].apply(pd.to_numeric, errors='coerce')

# Printing basic info
print("Basic Information about the Data:")
print(df.info())

# Printing few rows of the Data
print("\nFirst Few Rows of the Data:")
print(df.head())

# Checking for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Printing uniq. val.
unique_actions = df['action'].unique()
print("Unique Actions:")
print(unique_actions)


#  workout action based on different patterns
workout_logs = df[df['action'].str.contains('onStandStepChanged|onExtend|calculateCaloriesWithCache|calculateAltitudeWithCache', case=False, na=False)]

# first few rows of workout logs
print("Workout Logs:")
print(workout_logs.head())


workout_logs = df[df['action'].str.contains('Step|Workout|Exercise', case=False, regex=True)]

#  first few rows of workout logs
print("\nWorkout Logs:")
print(workout_logs.head())


#daily step count
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d-%H:%M:%S:%f')

df['date'] = df['timestamp'].dt.date


daily_step_count = df.groupby('date')['value1'].sum().reset_index()


print("\nDaily Step Count:")
print(daily_step_count)



#plotting graph


workout_logs['timestamp'] = pd.to_datetime(workout_logs['timestamp'])


# graph Daily Step Count
plt.figure(figsize=(10, 6))
sns.barplot(x='date', y='value1', data=daily_step_count)
plt.title('Daily Step Count')
plt.xlabel('Date')
plt.ylabel('Step Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



active_times = pd.DataFrame({
    'start_time': ['2022-01-01 08:00:00', '2022-01-02 12:30:00', '2022-01-03 18:45:00'],
    'end_time': ['2022-01-01 10:30:00', '2022-01-02 14:45:00', '2022-01-03 21:15:00'],
    'duration': [150, 195, 150]
})


active_times['start_time'] = pd.to_datetime(active_times['start_time'])
active_times['end_time'] = pd.to_datetime(active_times['end_time'])


active_times['day_of_week'] = active_times['start_time'].dt.day_name()
active_times['hour'] = active_times['start_time'].dt.hour

# Heatmap graph
plt.figure(figsize=(10, 6))
heatmap_data = active_times.pivot_table(index='day_of_week', columns='hour', values='duration', aggfunc='sum')
sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='.0f')
plt.title('Active Times Heatmap')
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.tight_layout()
plt.show()
