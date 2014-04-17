f=open("tweets.csv",'r')
neg=0
pos=0
f1=open("data",'w')
c=0
n=50
for i in f.readlines():
	l=i[:8]
	if pos >= n and neg>=n:
		break
	if l=='positive' and pos < n:
			pos=pos+1
			f1.write(i)
			c=c+1
	if l=='negative' and neg < n:
			neg=neg+1
			f1.write(i)
			c=c+1
f1.close()
print c
print pos+neg
