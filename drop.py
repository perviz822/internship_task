import pandas as pd
import json
'''
df =  pd.read_csv('final10.csv')

df['Company name'] = df['Company name'].replace(['', None], 'unknown')
df.to_csv('final11.csv')


'''

array = []



array.append({
'mobile' :67,
"desktop":21

})
array.append({
'mobile':78,
'desktop':67

})

print(type(array))
print(type(array[0]))

'''
with open("newfile.json" ,"w") as jsonfile:
    json.dump(array,jsonfile,indent=3)


'''
