import os
import pandas as pd
import numpy as np
from collections import Counter


def count_words_fast(text):
    text = text.lower()
    skips = [".", ",", ";", ":", "'", '"', "\n", "!", "?", "(", ")"]
    for ch in skips:
        text = text.replace(ch, "")
    word_counts = Counter(text.split(" "))
    return word_counts

def word_stats(word_counts):
    num_unique = len(word_counts)
    counts = word_counts.values()
    return (num_unique, counts)

hamlets = pd.read_csv("hamlets.csv", index_col=(1))
language, text = hamlets.iloc[0]
counted_text = count_words_fast(text)
data = pd.DataFrame(columns=('word','count', "length", "frequency"))


row_num = 1
for word in counted_text:
    count = counted_text[word]
    if count > 10:
        frequency = "frequent"
    elif 1 < count <= 10:
        frequency = "infrequent"
    elif count == 1:
        frequency = "unique"
    data.loc[row_num] = word, count,len(word),frequency
    row_num += 1

sub_data = pd.DataFrame(columns=("language","frequency","mean_word_length","num_words"))

i = 1
for word in counted_text:
    count = counted_text[word]
    if count > 10:
        frequency = "frequent"
        sum = 0
        for j in data.length[data.frequency == "frequent"]:
            sum += j

        mean_word_length = sum / len(data[data.frequency == "frequent"])
        num_words = len(data[data.frequency == "frequent"])
    elif 1 < count <= 10:
        frequency = "infrequent"
        sum = 0
        for j in data.length[data.frequency == "infrequent"]:
            sum += j

        mean_word_length = sum / len(data[data.frequency == "infrequent"])
        num_words = len(data[data.frequency == "infrequent"])
    elif count == 1:
        frequency = "unique"
        sum = 0
        for j in data.length[data.frequency == "unique"]:
            sum += j

        mean_word_length = sum / len(data[data.frequency == "unique"])
        num_words = len(data[data.frequency == "unique"])
    
    sub_data.loc[i] = language, frequency,mean_word_length,num_words
    i += 1

def summarize_text(language, text):
    counted_text = count_words_fast(text)

    data = pd.DataFrame({
        "word": list(counted_text.keys()),
        "count": list(counted_text.values())
    })
    
    data.loc[data["count"] > 10,  "frequency"] = "frequent"
    data.loc[data["count"] <= 10, "frequency"] = "infrequent"
    data.loc[data["count"] == 1,  "frequency"] = "unique"
    
    data["length"] = data["word"].apply(len)
    
    sub_data = pd.DataFrame({
        "language": language,
        "frequency": ["frequent","infrequent","unique"],
        "mean_word_length": data.groupby(by = "frequency")["length"].mean(),
        "num_words": data.groupby(by = "frequency").size()
    })
    
    return sub_data
grouped_data = pd.DataFrame(columns= ("language","frequency","mean_word_length","num_words"))
for i in range(len(hamlets)):
    language, text = hamlets.iloc[i]
    if language == 1:
        language = "English"
        sub_data = summarize_text(language, text)
        grouped_data = grouped_data.append(sub_data)
    elif language == 2:
        language = "German"
        sub_data = summarize_text(language, text)
        grouped_data = grouped_data.append(sub_data)
    elif language == 3:
        language = "Portuguese"
        sub_data = summarize_text(language, text)
        grouped_data = grouped_data.append(sub_data)

colors = {"Portuguese": "green", "English": "blue", "German": "red"}
markers = {"frequent": "o","infrequent": "s", "unique": "^"}
import matplotlib.pyplot as plt
for i in range(grouped_data.shape[0]):
    row = grouped_data.iloc[i]
    plt.plot(row.mean_word_length, row.num_words,
        marker=markers[row.frequency],
        color = colors[row.language],
        markersize = 10
    )

color_legend = []
marker_legend = []
for color in colors:
    color_legend.append(
        plt.plot([], [],
        color=colors[color],
        marker="o",
        label = color, markersize = 10, linestyle="None")
    )
for marker in markers:
    marker_legend.append(
        plt.plot([], [],
        color="k",
        marker=markers[marker],
        label = marker, markersize = 10, linestyle="None")
    )
plt.legend(numpoints=1, loc = "upper left")

plt.xlabel("Mean Word Length")
plt.ylabel("Number of Words")

plt.show()
plt.savefig("hw3-2")















