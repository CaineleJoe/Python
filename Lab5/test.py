result = [t for t in sorted([(288, 399), (583, 192), (926, 697), (306, 254), (942, 730), (521, 680), (52, 602), (627, 647), (963, 607), (319, 138), (640, 701), (653, 966), (304, 764), (294, 65), (50, 597), (225, 254), (541, 847), (379, 273), (31, 36), (368, 993), (385, 243), (880, 241), (755, 451), (420, 554), (753, 927), (550, 142), (46, 168), (118, 156), (709, 217), (644, 606)], reverse=True, key=lambda x: x[0])[:10] if (t[1] & 3) == 3]
print(result)


word=[(1,1,1,0,0,1,0,0,0,1,0,1,1,1,1,1,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,1),
      (1,0,0,1,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1),
      (1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1),
      (1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1),
      (1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1),
      (1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1),
      (1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1)]
final=""
for lists in word:
    y=""
    for i in lists:
      if i==0:
       y=y+" "
      else: y=y+"#"
    final=final+y+"\n"
print(final)


def pwer(n,p):
    count=0
    result=1
    while(count<p):
        result=result*n
        count=count+1
    return result%10
print(pwer(5,2))

text="Praslea a invins si cel de al treilea zmeu si eliberase si pe fata de imparat cea mai mica"
words=text.split()
sorted_words=sorted(words, key=lambda x: (len(x), x))
for word in sorted_words:
    print(word)
