from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 

def generateWordCloud(word_dir):
    
    stopwords = set(STOPWORDS)
    
    word_file = open(word_dir+"/cloud.txt", 'r')
    comment_words = word_file.read()
    
    wordcloud = WordCloud(width = 1000, height = 1000, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(comment_words) 
    
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show() 
