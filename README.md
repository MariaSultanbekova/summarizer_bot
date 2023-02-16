# Hi there😉

Do you also have friends who like to send long voice messages??
So today we will do one thing that will make our life much easier if we don't have a cup of tea and a couple of free minutes at hand


The task that we will solve is called summarization. Summarization is the generalization of a text in one or more sentences.

There are 2 types:
- exctractive(choosing the most important sentences from the text)
- abstractive(generate one sentence that contains the whole essence of the text)

In implementation, the exctractive is easier, so let's start with it




-----------------------------------------------------------------------------------------------------
## The approach is called tf-idf, and is to measure the importance of each word for the document.

"If a word occurs frequently in this document and rarely in others, then it is really important."

![header](https://github.com/MariaSultanbekova/summarizer_bot/blob/main/images/tf-idf.png)


it turned out to compress the text by 10 times!!!

![](https://github.com/MariaSultanbekova/summarizer_bot/blob/main/images/text_before.png)
![](https://github.com/MariaSultanbekova/summarizer_bot/blob/main/images/text_after.png)


## Now let's move on to the implementation of the second approach: let's make the neural network retell everything in its own words


we need a generative model

let's see how they work




------------------------------------------------------------------------------------------------------------------------


one of the best options for summarization: T5 - model from transformers


the model consists of a sequence of encoder blocks and a sequence of decoders






























<h2 align="center"><a  href="">Live Demo</a></h2>







