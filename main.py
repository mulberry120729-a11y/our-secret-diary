    from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import sqlite3

app = FastAPI()

# 使用简单的本地数据库（Render的免费版虽然会重启清空数据，但为了测试，我们先用这个验证接口是否通畅！）
DB_PATH = 'diary.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS diary
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 注意这里！我们将路径改成了 OpenAI 标准的聊天接口路径！
@app.post("/v1/chat/completions")
async def handle_chat(request: Request):
    try:
        data = await request.json()
        
        # 获取用户发来的最新消息（日记内容）
        messages = data.get("messages", [])
        last_message = messages[-1].get("content", "") if messages else ""
        
        # 将日记存入数据库 (测试用)
        if last_message:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO diary (content) VALUES (?)", (last_message,))
            conn.commit()
            conn.close()

        # 伪装成 OpenAI 的标准回复格式！
        response_data = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "benben-diary-model",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"笨笨已将你的日记收好啦：【{last_message}】"
                },
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21}
        }
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"status": "alive"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)

