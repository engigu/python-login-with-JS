import execjs

with open('./enpwd.js', 'r',encoding='utf-8') as f:
    content = f.read()

js_e = execjs.get()
cm = execjs.compile(content)
result = cm.call('ensnpwd','admin1234')
print(result)