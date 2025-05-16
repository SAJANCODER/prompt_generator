import spacy

nlp=spacy.load("en_core_web_lg")
doc1=nlp("dog")
doc2=nlp("cat")

print("Similarity:",doc1.similarity(doc2))