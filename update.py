import requests
from Crypto.Cipher import AES


def get_json_str(content: str) -> str:
    assert(content[:4] == '2423')
    content = bytes.fromhex(content)
    pad = lambda x: x + b'0' * (16 - len(x))
    key = pad(content[content.find(b'$#')+2:content.find(b'#$')])
    data = content[content.find(b'#$')+2:-13]
    iv = pad(content[-13:])
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    return aes.decrypt(data).decode('utf8')


res = requests.get('https://download.kstore.space/download/2863/01.txt')
res.encoding = 'utf-8'
res = get_json_str(res.text)
lines = res.splitlines(keepends=True)
for i, line in enumerate(lines):
    if line.startswith('"lives"'):
        lines[i] = '"lives":[{"name":"直播","type":0,"url":"https://cdn.jsdelivr.net/gh/Reflyer823/tvbox-config@master/live.txt"}],\n//' + line
        break
with open('main.json', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(lines)
