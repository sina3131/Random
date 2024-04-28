

import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random

import json
with open('/Users/sina/Python/Django/web-framework-project_v1-paul-sina-hyomi/django-boilerplate-main/boilerplate/core/inten.json'
) as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []


for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])
        
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)


#tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("/Users/sina/Python/Django/web-framework-project_v1-paul-sina-hyomi/django-boilerplate-main/boilerplate/core/model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("/Users/sina/Python/Django/web-framework-project_v1-paul-sina-hyomi/django-boilerplate-main/boilerplate/core/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


# def get_response(inp):
#     results = model.predict([bag_of_words(inp, words)])
#     results_index = numpy.argmax(results)
#     tag = labels[results_index]


#     for tg in data["intents"]:
#         if tg['tag'] == tag:
#             responses = tg['responses']

#     # return random.choice(responses)

    

def get_response(inp):
    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    try:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        return str(random.choice(responses))

    except Exception as e:
        print(e)
        return "Sorry, I didn't understand that."









# import nltk
# nltk.download('punkt')
# from nltk.stem.lancaster import LancasterStemmer
# stemmer = LancasterStemmer()

# import numpy as np
# import tflearn
# import tensorflow as tf
# import random
# import json

# with open('intents.json') as file:
#     data = json.load(file)

# words = []
# labels = []
# docs_x = []
# docs_y = []

# # Loop through each intent in the JSON file
# for intent in data['intents']:
#     for pattern in intent['patterns']:
#         wrds = nltk.word_tokenize(pattern)
#         words.extend(wrds)
#         docs_x.append(wrds)
#         docs_y.append(intent['tag'])
    
#     # Check if the intent tag already exists in the labels list
#     if intent['tag'] not in labels:
#         labels.append(intent['tag'])

# # Stem and lowercase the words
# words = [stemmer.stem(w.lower()) for w in words if w != '?']
# words = sorted(list(set(words)))

# # Sort the labels
# labels = sorted(labels)

# training = []
# output = []

# # Create an empty array for the output
# out_empty = [0 for _ in range(len(labels))]

# # Loop through each input/output pair
# for x, doc in enumerate(docs_x):
#     bag = []

#     # Stem and lowercase each word in the input
#     wrds = [stemmer.stem(w.lower()) for w in doc]

#     # Create a bag of words with 1's for words that appear in the input
#     for w in words:
#         if w in wrds:
#             bag.append(1)
#         else:
#             bag.append(0)

#     # Create the output for the current input
#     output_row = out_empty[:]
#     if docs_y[x] in labels:
#         output_row[labels.index(docs_y[x])] = 1
#     else:
#         labels.append(docs_y[x])
#         output_row[len(labels)-1] = 1

#     # Add the bag of words and output to the training data
#     training.append(bag)
#     output.append(output_row)

# # Convert the training and output data to numpy arrays
# training = np.array(training)
# output = np.array(output)



# # Define the neural network architecture
# net = tflearn.input_data(shape=[None, len(training[0])])
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
# net = tflearn.regression(net)

# # Define the model and try to load it from disk
# model = tflearn.DNN(net)

# try:
#     model.load("C:/Python/chatbot/model.tflearn")
# except:
#     model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
#     model.save("C:/Python/chatbot/model.tflearn")

# # model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
# # model.save('model.tflearn')


# # Define a function to generate a bag-of-words representation of an input sentence
# def bag_of_words(sentence, words):
#     bag = np.zeros(len(words))
#     stemmed_sentence = [stemmer.stem(w.lower()) for w in nltk.word_tokenize(sentence) if w.isalpha()]
    
#     for i, w in enumerate(words):
#         if w in stemmed_sentence:
#             bag[i] = 1
            
#     return bag

# # Define a function to generate a response to an input sentence
# def get_response(sentence):
#     # Use the trained model to predict the tag of the input sentence
#     results = model.predict([bag_of_words(sentence, words)])
#     tag_index = np.argmax(results)
#     tag = labels[tag_index]
    
#     # Select a random response from the set of responses for the predicted tag
#     responses = [intent['response'] for intent in data['intents'] if intent['tag'] == tag]
#     response = random.choice(responses)
    
#     return response


# import nltk
# import numpy as np
# import tflearn
# import tensorflow as tf
# import random
# import json
# import pickle
# from nltk.stem.lancaster import LancasterStemmer

# stemmer = LancasterStemmer()

# # load the saved model
# # model = tflearn.DNN.load("C:/Python/chatbot/model.tflearn")
# # model = tflearn.DNN.load('model.tflearn')


# # load the intents file
# with open("intents.json") as file:
#     data = json.load(file)

# # # load the trained data
# # with open("data.pickle", "rb") as f:
# #     words, labels, training, output = pickle.load(f)

# # create a chat interface
# def chat():
#     print("Start talking with the bot (type 'quit' to exit)")

#     # keep chatting until the user types 'quit'
#     while True:
#         # get user input
#         user_input = input("You: ")

#         # check if user wants to quit
#         if user_input.lower() == "quit":
#             break

#         # pre-process user input
#         user_input = nltk.word_tokenize(user_input)
#         user_input = [stemmer.stem(word.lower()) for word in user_input]

#         # create a bag of words
#         bag = [0] * len(words)
#         for word in user_input:
#             for i, w in enumerate(words):
#                 if w == word:
#                     bag[i] = 1

#         # generate the model's prediction
#         results = model.predict([bag])[0]
#         results_index = np.argmax(results)
#         tag = labels[results_index]

#         # if the model's confidence is low, respond with "I'm not sure"
#         if results[results_index] < 0.7:
#             print("Bot: I'm not sure what you mean. Can you be more specific?")
#         else:
#             # select a random response from the tag's list of responses
#             for intent in data["intents"]:
#                 if intent["tag"] == tag:
#                     responses = intent["responses"]
#             response = random.choice(responses)
#             print("Bot: " + response)

# # start the chat interface
# chat()
