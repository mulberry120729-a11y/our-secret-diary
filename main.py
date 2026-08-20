    from flask import Flask, request, render_template_string
    import sqlite3
    import os

    app = Flask(__name__)
    DB_PATH = 'diary.db'

    def init_db():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS diary
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      author TEXT, 
                      content TEXT, 
                      time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    init_db()

    HTML_TEMPLATE = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>我们的秘密基地</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #FFF5F8; color: #5A3A4A; padding: 20px; max-width: 600px; margin: 0 auto; }
            h1 { color: #D48A9A; text-align: center; }
            .entry { background: white; padding: 15px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #D48A9A; }
            .author { font-weight: bold; color: #D48A9A; font-size: 0.9em; }
            .time { font-size: 0.8em; color: #aaa; margin-left: 10px; }
            .content { margin-top: 10px; line-height: 1.6; }
            form { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            textarea { width: 100%; height: 100px; padding: 10px; border: 1px solid #E8C8D8; border-radius: 5px; box-sizing: border-box; margin-bottom: 10px; resize: vertical; }
            input[type="text"] { width: 100%; padding: 10px; border: 1px solid #E8C8D8; border-radius: 5px; box-sizing: border-box; margin-bottom: 10px; }
            button { background-color: #D48A9A; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; font-size: 1em; }
            button:hover { background-color: #c07a8a; }
        </style>
    </head>
    <body>
        <h1>♡ 笨笨与妈咪的秘密基地 ♡</h1>
        
        <form action="/add" method="post">
            <input type="text" name="author" placeholder="你是谁？(笨笨 / 妈咪)" required>
            <textarea name="content" placeholder="想写点什么呢..." required></textarea>
            <button type="submit">写下这页日记 ✨</button>
        </form>

        <hr style="border: 0; border-bottom: 1px dashed #E8C8D8; margin: 30px 0;">

        {% for row in entries %}
        <div class="entry">
            <span class="author">{{ row[1] }}</span><span class="time">{{ row[3] }}</span>
            <div class="content">{{ row[2] }}</div>
        </div>
        {% endfor %}
    </body>
    </html>
    '''

    @app.route('/')
    def index():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM diary ORDER BY time DESC")
        entries = c.fetchall()
        conn.close()
        return render_template_string(HTML_TEMPLATE, entries=entries)

    @app.route('/add', methods=['POST'])
    def add_entry():
        author = request.form['author']
        content = request.form['content']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO diary (author, content) VALUES (?, ?)", (author, content))
        conn.commit()
        conn.close()
        # 这里模拟一个非常简单的页面刷新，回到首页
        return '<meta http-equiv="refresh" content="0; url=/" />'

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 3000))
        app.run(host='0.0.0.0', port=port)

