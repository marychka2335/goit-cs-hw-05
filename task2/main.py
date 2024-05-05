import string
import asyncio
from collections import defaultdict, Counter
from matplotlib import pyplot as plt
import httpx

#Getting data from url
async def get_text(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None


# Delete punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

#Return tuple
async def map_text(word) -> tuple:
    return word, 1

#Gather tuple word in list
async def transform_in_listed_tuple(words) -> list:
    return [await map_text(word) for word in words]

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


async def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Main 
async def map_reduce(text):
    text = await get_text(url)
    if text:
        # Delete punct
        text = remove_punctuation(text)
        words = text.split()

        # Mapping
        mapped_values = await transform_in_listed_tuple(words)

        # Shuffle
        shuffled_values = shuffle_function(mapped_values)

        # Reduction
        reduced_values = await asyncio.gather(*[reduce_function(key_values) for key_values in shuffled_values])

        return dict(reduced_values)
    else:
        return None

#To set settings of pyplot
def visual_result(result):
    top_10 = Counter(result).most_common(10)
    top_10.reverse()
    labels, values = zip(*top_10)
    plt.figure(figsize=(10, 5))
    plt.barh(labels, values, color='#84cbeb')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 Most Frequent Words')
    plt.show()

# To start use - > python<version> main.py
if __name__ == '__main__':
    url = "https://www.gutenberg.net.au/ebooks06/0602541.txt" # <--- Add url here
    # Execute MapReduce
    result = asyncio.run(map_reduce(url))

    #print("Results:", result) < - to get in CLI
    visual_result(result)