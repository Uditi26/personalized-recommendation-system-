import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque
import time

#function to clean data
def clean_text(author):
    result = str(author).lower()
    return(result.replace(' ',''))

#function for BFS
def recommend_books(pd,books,user_preferences):
    max_recommendations=5
    recommended_books = []
    input_book = input('Enter book title\n')
    visited_genres = set(user_preferences)
    queue = deque(user_preferences)
    recommendations = pd.DataFrame(df.nlargest(11,input_book)['Book-Title'])
    recommendations = recommendations[recommendations['Book-Title']!=input_book]
    while queue and len(recommended_books) < max_recommendations:
        current_genre = queue.popleft()

        for book, genres in books.items():
            if book not in recommended_books and current_genre in genres:
                recommended_books.append(book)

                # Add unvisited genres to the queue
                for genre in genres:
                    if genre not in visited_genres:
                        visited_genres.add(genre)
                        queue.append(genre)

    return recommendations

df = pd.read_csv('BX-Books.csv',on_bad_lines='skip',encoding='latin-1',sep=';',low_memory=False)
# df.info()

#removing duplicates
df.duplicated(subset='Book-Title').sum()
df = df.drop_duplicates(subset='Book-Title')
df.duplicated(subset='Book-Title').sum()

#random sampling to avoid memory errors
sample_size = 15000
df = df.sample(n=sample_size, replace=False, random_state=490)
df = df.reset_index()
df = df.drop('index',axis=1)
# df.head()

#cleaning data
df['Book-Author'] = df['Book-Author'].apply(clean_text)
#converting to lower case
df['Book-Title'] = df['Book-Title'].str.lower()
df['Publisher'] = df['Publisher'].str.lower()
# combine all strings:
df2 = df.drop(['ISBN','Image-URL-S','Image-URL-M','Image-URL-L','Year-Of-Publication'],axis=1)
df2['data'] = df2[df2.columns[1:]].apply(
    lambda x: ' '.join(x.dropna().astype(str)),
    axis=1)
# print(df2['data'].head())


#vectorising the database
#that is converting it to adjanccency matrix
vectorizer = CountVectorizer()
vectorized = vectorizer.fit_transform(df2['data'])
similarities = cosine_similarity(vectorized)
# print(similarities)

#map back to database
df = pd.DataFrame(similarities, columns=df['Book-Title'], index=df['Book-Title']).reset_index()

#print the recommendation based on bfs
start=time.time()
recommendations=recommend_books(pd,df,df2)
print(recommendations)
end=time.time()

#getting time complexity
run_time=end-start
print("\n")
print("Time complexity= ")
print(run_time)



