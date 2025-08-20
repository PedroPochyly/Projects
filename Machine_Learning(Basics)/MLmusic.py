import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv('music.csv')

X = df.drop(columns=['genre'])
y = df['genre']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) #20% of the data will be used for testing

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(predictions)

score = accuracy_score(y_test, predictions) #returns the accuracy of the model

print('Accuracy:', score)