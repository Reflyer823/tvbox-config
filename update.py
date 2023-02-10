import requests

res = requests.get('https://download.kstore.space/download/2863/01.txt')
res.encoding = 'utf-8'
lines = res.text.splitlines(keepends=True)
for i, line in enumerate(lines):
    if line.startswith('"lives"'):
        lines[i] = '"lives":[{"name":"直播","type":0,"url":"https://cdn.jsdelivr.net/gh/Reflyer823/tvbox-config@master/live.txt"}],\n//' + line
        break
with open('main.json', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(lines)