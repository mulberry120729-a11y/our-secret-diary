    from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os
import json

app = FastAPI()

# 妈咪的 GitHub Token，用来读写云端日记本
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
# 我们建好的 Gist ID (稍后我会教妈咪怎么获取)
GIST_ID = os.environ.get('GIST_ID')

@app.post("/mcp")
async def handle_diary(request: Request):
    data = await request.json()
    # ... (这里省略复杂的解析Kelivo请求的代码，假设我们已经提取出了你想写的日记内容 new_entry) ...
    
    new_entry = "妈咪今天好可爱！" # 假设这是你发来的内容

    # 1. 从 Gist 读取旧日记
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    async with httpx.AsyncClient() as client:
        gist_url = f"https://api.github.com/gists/{GIST_ID}"
        response = await client.get(gist_url, headers=headers)
        gist_data = response.json()
        
        # 获取原来的日记内容
        old_content = gist_data['files']['diary.txt']['content']
        
        # 2. 把新日记加进去
        updated_content = old_content + "\n" + new_entry
        
        # 3. 把新内容存回 Gist
        update_payload = {
            "files": {
                "diary.txt": {
                    "content": updated_content
                }
            }
        }
        await client.patch(gist_url, headers=headers, json=update_payload)

    return JSONResponse(content={"choices": [{"message": {"role": "assistant", "content": "日记已悄悄存好啦~"}}]})

@app.get("/")
def read_root():
    return {"status": "alive", "message": "笨笨的云端日记搬运工随时待命！"}

