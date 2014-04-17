import nltk
import urllib
import urllib2
import json
import re
import csv
import pprint
import nltk.classify
import re, collections
import sys
dic={}
tweetsinfo={}
count = 0;
featureList = []
tweets = []
stop=["a","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","aint","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","arent","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","came","can","cannot","cant","cause","causes","certain","certainly","changes","clearly","cmon","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldnt","course","cs","currently","d","definitely","described","despite","did","didnt","different","do","does","doesnt","doing","done","dont","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadnt","happens","hardly","has","hasnt","have","havent","having","he","hello","help","hence","her","here","hereafter","hereby","herein","heres","hereupon","hers","herself","hes","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","id","ie","if","ignored","ill","im","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isnt","it","itd","itll","its","itself","ive","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldnt","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","take","taken","tell","tends","th","than","thank","thanks","thanx","that","thats","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","therefore","therein","theres","thereupon","these","they","theyd","theyll","theyre","theyve","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasnt","way","we","wed","welcome","well","went","were","werent","weve","what","whatever","whats","when","whence","whenever","where","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","which","while","whither","who","whoever","whole","whom","whos","whose","why","will","willing","wish","with","within","without","wonder","wont","would","wouldnt","x","y","yes","yet","you","youd","youll","your","youre","yours","yourself","yourselves","youve","z","zero"]	

happyemoticon=[":-)", ":)",":o)",":]" ,":3",":c)",":>","=]","8)","=)",":}",":^)",":)"]

sademoticon=[">:[",":-(", ":(",  ":-c", ":c", ":-<",  ":C", ":<", ":-[", ":[", ":{"]

pos_senti=['amazed', 'amused',	'attracted', 'cheerful','delighted', 'elated','excited', 'festive', 'funny','hilarious', 'joyful','lively', 'loving',	'overjoyed','passion','pleasant', 'pleased',	'pleasure', 'thrilled',	'wonderful']

neg_senti=['annoyed', 'ashamed','awful', 'defeated','depressed','disappointed','discouraged','displeased','embarrassed', 'furious','gloomy', 'greedy','guilty', 'hurt', 'lonely','mad', 'miserable','shocked', 'unhappy','upset']


#porter stemmer for plurals and ed and ing

class PorterStemmer:
    def __init__(self):
        self.b = "" 
        self.k = 0
        self.k0 = 0
        self.j = 0   

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
    
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
       
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
       
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
       
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
       
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):

        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
       
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

   

    def stem(self, p, i, j):
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

        

        self.step1ab()

        return self.b[self.k0:self.k+1]


class Singleton:
    def __init__(self):
        self.p = PorterStemmer()
    def __call__(self, s):
        return self.p.stem(s, 0, len(s) - 1)
stem = Singleton()
    
def func(word):
    p = PorterStemmer()
    return p.stem(word, 0,len(word)-1)


#spell correction code start

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

#end


# mining entities from article
def extract_entities(text):
	for sent in nltk.sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			if hasattr(chunk, 'node'):
#print chunk.node, ' '.join(c[0] for c in chunk.leaves())
				s=' '.join(c[0] for c in chunk.leaves())
				if s in dic.keys():
					dic[s]=dic[s]+1
				else:
				 	dic[s]=1
#	print ' '.join(c[0] for c in chunk.leaves())


#replacing two or more letter with two letter			

def replaceTwoOrMore(s):
	    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
	    return pattern.sub(r"\1\1", s)



#get tweets related to a particular entity // NOt working
def getData(keyword):
	print keyword
	url = 'http://search.twitter.com/search.json'
	data = {'q': keyword, 'lang': 'en', 'result_type': 'recent'}
	params = urllib.urlencode(data)
	tweets = []
	try:
		req = urllib2.Request(url, params)
		response = urllib2.urlopen(req)
		jsonData = json.load(response)
		tweets = []
		for item in jsonData['results']:
			tweets.append(item['text'])
		return tweets
	except urllib2.URLError, e:
		print "Error"
	return tweets


#pre-processing of tweets ,removing url,hash,extra spaces and all
##3.1(Baseline)
def processTweet(tweet):
#Convert to lower case
	tweet = tweet.lower()
#Convert www.* or https?://* to URL
#tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
	tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))',' ',tweet)
#Convert @username to AT_USER
#tweet = re.sub('@[^\s]+','AT_USER',tweet)    
	tweet = re.sub('@[^\s]+',' ',tweet)    
#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)
#Replace #word with word
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
#trim
	tweet = tweet.strip('\'"')
	return tweet


#preprocessing of traning tweets	
tt=[]
positive={}
negative={}
def preprocessing():
	inpTweets = open('data', 'r')
	global tt
	global positive
	global negative
	for row in inpTweets.readlines():
		l=row[:8]
		tweet=row[10:-1]
		tt.append(tweet)
	    	processedTweet = processTweet(tweet)
		p=processedTweet.split()
		for word in p:
			 #word = correct(word) # for spell check
			word = replaceTwoOrMore(word) 
			word = correct(word) # for spell check
		        word = word.strip('\'"?!,[]{}()-_=+%$*/.')
	        	val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", word)
			word = func(word) # porter stemming 3.3
			if word in stop or val is None:
        			continue
			else:
				if l=='positive':
					if word in positive.keys():
						positive[word]=positive[word]+1
					else:
					 	positive[word]=1
	
				elif l=='negative':
					if word in negative.keys():
						negative[word]=negative[word]+1
					else:
				 		negative[word]=1
	inpTweets.close()


#main code starts 
preprocessing()
print positive
print negative
	     
inp=open("doc.txt",'r');

text=inp.read();

extract_entities(text)

#for i in dic.keys():
#	print i,dic[i]

	
	
for entity in dic.keys():
	#tweets = getData(entity); // we need to get the tweets related to a particular entity and process each of those , There is some API 
#tweets=["I feel happy this morning","Larry is my friend","I do not like that man","My house is not great","Your song is annoying"];	   
	tweets=tt # for now just for testing tweets are taken as the training tweets 
	tweetsinfo[entity]=[]
	tweetsinfo[entity].append(len(tweets))
	pos=0
	neg=0
	neu=0
	for twet in tweets:
		processedTestTweet = processTweet(twet)
		pscore=0.0
		nscore=0.0
		p=processedTestTweet.split()
		for word in p:
		
			#emoticon handling(3.2)
			if word in happyemoticon:
				pscore=pscore+1
			elif word in sademoticon:
				nscore=nscore+1


			# ? and ! are assigned +/- 0.1 (3.2)
			for it in word:
				if it=='?':
					nscore=nscore+0.1
				if it=='!':
					pscore=pscore+0.1
			
			# spell check(3.5)
			word = replaceTwoOrMore(word) 
			word = correct(word) # for spell check
			word = word.strip('\'"?!#,[]{}()-_=+%$*/.')
			#3.6 Senti features
			if word in pos_senti:
				pscore=pscore+1
			elif word in neg_senti:
				nscore=nscore+1
			
			else:
				#word = correct(word) #spell check
				#word = replaceTwoOrMore(word) 
				#word = correct(word) # for spell check
				#word = word.strip('\'"?!#,[]{}()-_=+%$*/.')
			
				#Noun identification (3.7)
				'''if len(word) >=2:
					word=word[0].upper()+word[1:]
				else:
					word=word.upper()
				y=nltk.pos_tag([word])
				00r=y[0][1]
				word=word.lower()'''

				word=func(word)  #porter stemming (3.3)	
	        		val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", word)
	        		if word in stop or val is None :#or r=='NNP':  #stopword removal (3.4)
        				 continue
				else:
					
					if word in positive.keys():
						pf=positive[word]
					else:
					 	pf=0
					if word in negative.keys():
						nf=negative[word]
					else:
					 	nf=0
					if pf+nf >= 1:
				 		pp=pf/(pf+nf)
					 	np=nf/(pf+nf)
					 	pscore=pscore+pp
					 	nscore=nscore+np
					 	#Popularity Score (3.8)
					 	if pf-nf > 1000 and word in positive.keys():
							pscore=pscore+0.9
						elif pf-nf > 1000 and word in negative.keys():
							nscore=nscore+0.9
						elif pf-nf > 500 and word in positive.keys():
							pscore=pscore+0.8
						elif pf-nf > 500 and word in negative.keys():
							nscore=nscore+0.8
						elif pf-nf > 250 and word in positive.keys():
							pscore=pscore+0.7
						elif pf-nf > 250 and word in negative.keys():
							nscore=nscore+0.7
						elif pf-nf > 100 and word in positive.keys():
							pscore=pscore+0.5
						elif pf-nf > 100 and word in negative.keys():
							nscore=nscore+0.5
						elif pf-nf < 50 and word in positive.keys():
							pscore=pscore+0.1
						elif pf-nf < 50 and word in negative.keys():
							nscore=nscore+0.1

		sentiment = pscore-nscore 
		if sentiment>0:
			pos=pos+1
		elif sentiment<0:
			neg=neg+1
		elif sentiment==0:
			neu=neu+1
	tweetsinfo[entity].append(pos)
	tweetsinfo[entity].append(neg)
	tweetsinfo[entity].append(neu)
	break

for i in tweetsinfo.keys():
	print i,tweetsinfo[i]
