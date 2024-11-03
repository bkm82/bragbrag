My implementation of a rag agent

Name: bragbrag

In my friends group, when someone is talking about something awesome they did we often light heartedly respond with "brag brag"
So when I (Bray) wanted to make a RAG agent to learn about LLM models, brag brag was born

This project was used as a learning exersise, and as i belive the best way to learn is to break things, it might be broken my some of my schenanigan s. My objective of this project is to create an RAG agent that utilizes a llama model.

I want to have the following flow
- Ask a question
- Retrevie relevant documents
- Create a grader agent that determines if the documents are releveant to the original question, dropping any documents that are not
- Generate a response to the original question using the relevent documen ts as reference material
-create a grader agent that determines if the answer is supported by the relevent material, if not, regenerate
-create a grader agent that determines if the original question was answerd, if not regenerate
- return the response.







![Tests](https://github.com/bkm82/pyflowvc/actions/workflows/tests.yml/badge.svg)
