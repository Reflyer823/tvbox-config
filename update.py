import requests
from Crypto.Cipher import AES


CONFIG_URL = 'https://download.kstore.space/download/2863/01.txt'
LIVE_URL = 'https://download.kstore.space/download/2863/live.txt'
CUSTOM_LIVE_URL = 'https://cdn.jsdelivr.net/gh/Reflyer823/tvbox-config@master/live.txt'


def get_json_str(content: str) -> str:
    assert(content[:4] == '2423')
    content = bytes.fromhex(content)
    pad = lambda x: x + b'0' * (16 - len(x))
    key = pad(content[content.find(b'$#')+2:content.find(b'#$')])
    data = content[content.find(b'#$')+2:-13]
    iv = pad(content[-13:])
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    text = aes.decrypt(data).decode('utf8')
    return text[:text.rfind('}')+1]    # 不知道为什么文件末尾会有奇怪的字符


res = requests.get(CONFIG_URL)
res.encoding = 'utf-8'
res = get_json_str(res.text)
lines = res.splitlines(keepends=True)
for i, line in enumerate(lines):
    if line.startswith('"lives"') and LIVE_URL in line:
        lines[i] = line.replace(LIVE_URL, CUSTOM_LIVE_URL) + '//' + line
        break
with open('main.json', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(lines)


res = requests.get(LIVE_URL)
res.encoding = 'utf-8'
live_str = res.text
with open('custom_live.txt', 'r', encoding='utf-8') as f:
    live_str = f.read() + live_str
with open('live.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(live_str)
