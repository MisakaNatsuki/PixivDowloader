import json
import requests
import zipfile
import _thread
import time

headers_str = """accept: image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cache-control: no-cache
pragma: no-cache
referer: https://www.pixiv.net/
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: image
sec-fetch-mode: no-cors
sec-fetch-site: cross-site
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"""

headers = {}

for i in headers_str.split("\n"):
    i = i.split(": ")
    headers[i[0]] = i[1]

process = int(input("StartNum:"))

def download():
    global process
    global zf
    global content
    while process < len(content):
        i = content[process]
        index = process
        process += 1
        while True:
            try:
                data = requests.get(i["small"],headers=headers)
                zf.writestr(i["id"]+"."+i["small"].split(".")[-1],data.content)
                time.sleep(0.1)
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
        print(i["id"], index)

if __name__ == "__main__":
    with open("result" + input("resultID:") + ".json") as fp:
        content = json.load(fp)
    zf = zipfile.ZipFile("download" + input("id:") + ".zip","w",compression=zipfile.ZIP_DEFLATED,compresslevel=6)
    index = 0
    for i in range(int(input("process:"))):
        _thread.start_new_thread(download, ())
    download()
    zf.close()
