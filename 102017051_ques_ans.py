import wikipedia
import re
import nltk.data
import string
from nltk.corpus import wordnet
import sys
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


wh_ques = ["who", "where", "what", "when"]
helping_verbs = ['is', 'are', 'has', 'have', 'has been', 'have been', 'has had', "do", 
                'was', 'were', 'had', 'had been', 'had had', "did",
                'will', 'shall', 'can', 'will have', 'shall have', 'can have',
                'would', 'should', 'could', 'would have', 'should have', 'could have', 'would have been', 'should have been', 'could have been']


logfile = open(sys.argv[1],"a+")

def get_ans(user_ques):
    
    logfile.write('%s\n\n' %user_ques)
    re_1 = re.compile(r'('+"|".join(wh_ques)+') ('+"|".join(helping_verbs)+') (.*)\?', re.IGNORECASE)
    m = re_1.match(user_ques)
    
    if(m is None):
        return
    wh = m.group(1)
    hv = m.group(2)
    obj = m.group(3)
    
    if(wh.lower() != "when"):
        tagged_data = nltk.pos_tag(nltk.word_tokenize(obj))
        logfile.write(str(tagged_data))
        noun = " ".join([word_tag[0] for word_tag in tagged_data if word_tag[1]=="NNP"])
        verbs = [word_tag[0] for word_tag in tagged_data if word_tag[1]=="VBD"]
        if(len(verbs) == 1):
            verb = verbs[0]
            syns = [l.name() for syn in wordnet.synsets(verb) for l in syn.lemmas()]
        else:
            verb = ""
        if(verb != ""):
            search_res = wikipedia.search(noun)
            logfile.write(str('%s\n\n' %search_res))
            
        else:
            search_res = wikipedia.search(obj)
            logfile.write(str('%s\n\n' %search_res)) 
        findings = []

        for res in search_res:
            content = wikipedia.page(res).content
            sentences = tokenizer.tokenize(content)
            
            if(verb != ""):
                for sent in sentences:
                    if(re.search('('+verb+'|'+"|".join(syns)+')', sent, re.IGNORECASE) is not None):
                        if(re.search(noun, sent, re.IGNORECASE) is not None):
                            findings.append(sent)
                        else:
                            findings.append(sent)
                            logfile.write(str('%s\n\n' %findings))
                if(len(findings) == 0):
                    return "Not found."
                else:
                    find = findings[0]
                    logfile.write(str('%s\n\n' %find))
                    return noun+" "+hv+" "+ find[find.index(verb):]
            else:
                for sent in sentences:
                    if(re.search(noun, sent, re.IGNORECASE) is not None):
                        if(re.search(" "+hv+" ", sent, re.IGNORECASE) is not None):
                            findings.append(sent)
                            logfile.write(str('%s\n\n' %findings))

                if(len(findings) == 0):
                    return "Not found"
                find = findings[0]
                logfile.write(str('%s\n\n' %find))
                return obj+" "+ find[find.index(hv+" "):]
    else:
        arr = obj.split()
        name = " ".join(arr[:-1])
        y = arr[-1]
        syns = [l.name() for syn in wordnet.synsets(y) for l in syn.lemmas()]
        search_res = wikipedia.search(name)
        logfile.write(str('%s\n' %search_res))
        findings = []
        
        for res in search_res:
            content = wikipedia.page(res).content
            sentences = tokenizer.tokenize(content)
            for sent in sentences:
                if(re.search(name, sent, re.IGNORECASE) is not None):
                    if(re.search('('+y+'|'+"|".join(syns)+')', sent, re.IGNORECASE) is not None):
                        if(re.search(" on ", sent, re.IGNORECASE) is not None):
                            findings.append(sent)
                            logfile.write(str('%s\n\n' %findings))
        if(len(findings) == 0):
            return "Not found."
        find = findings[0]
        logfile.write(str('%s\n\n' %find))
        sobj = re.search(r'\d{4}', find, re.IGNORECASE)
        year = sobj.group()
        return name+" "+hv+" "+y+" "+find[find.index("on"):find.index(year)+4]


# In[ ]:


print("Hi,this is a Q/A Project ")
while True:
    
    user_ques = input()
    if(user_ques == 'exit'):
        print("End")
        logfile.write('%s\n\n' %"End")
        break
    else:
        try:
            ans = get_ans(user_ques)
            print(ans)
            logfile.write('%s\n\n' %ans)
            
        except Exception as e:
            print(str(e))
            print("Not Found")
            logfile.write('%s\n\n' %"Not Found.")