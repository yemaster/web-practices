from quart import Quart, render_template, request, jsonify
from selenium import webdriver
import sqlite3
import time
import asyncio
import json
import os
import tempfile

app = Quart(__name__)
flag = "flag{test_flag}"

CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH', '../../chrome/chromedriver')
CHROME_EXECUTABLE_PATH = os.environ.get('CHROME_EXECUTABLE_PATH', '../../chrome/chrome')

def init_db():
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS http_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL,
            url TEXT NOT NULL,
            headers TEXT NOT NULL,
            cookies TEXT NOT NULL,
            body TEXT,
            ip_address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_comments():
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('SELECT username, comment FROM comments')
    comments = c.fetchall()
    conn.close()
    return comments

def add_comment(username, comment):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('INSERT INTO comments (username, comment) VALUES (?, ?)', (username, comment))
    conn.commit()
    conn.close()

def log_http_request(method, url, headers, cookies, body, ip_address):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('INSERT INTO http_log (method, url, headers, cookies, body, ip_address) VALUES (?, ?, ?, ?, ?, ?)',
              (method, url, headers, cookies, body, ip_address))
    conn.commit()
    conn.close()

def get_http_request_list():
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('SELECT method, url, headers, cookies, body, ip_address FROM http_log ORDER BY id DESC LIMIT 10')
    logs = c.fetchall()
    conn.close()
    return logs

@app.route('/')
async def home():
    comments = get_comments()
    return await render_template('index.html', comments=comments)

@app.route('/info')
async def info():
    return {
        "challenge": "web15-1",
        "by": "yemaster"
    }

@app.post('/add_comment')
async def post_comment():
    username = (await request.form)['username']
    comment = (await request.form)['comment']
    if len(username) > 15 or len(comment) > 200:
        return jsonify({'status': 'error', 'message': '昵称不能超过 15 字，评论不能超过 200 字！'}), 400
    try:
        add_comment(username, comment)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'success'})

running = False

async def viewing_website():
    global running
    try:
        # 使用线程来运行同步的 Selenium 代码，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _run_selenium)
    except Exception as e:
        print(f"Error in viewing_website: {e}")
    finally:
        running = False

def _run_selenium():
    global running
    try:
        options = webdriver.ChromeOptions()
        # options.binary_location = CHROME_EXECUTABLE_PATH
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        user_data_dir = tempfile.mkdtemp()
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_argument('--disable-dev-shm-usage')
        # service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
        # driver = webdriver.Chrome(options=options, service=service)
        driver = webdriver.Chrome(options=options)
        driver.get('http://web/info')
        cookie = {
            'name': 'flag',
            'value': flag,
            'path': '/',
            'httpOnly': False,
            'secure': False
        }
        driver.add_cookie(cookie)
        driver.get('http://web/')
        time.sleep(5)
        driver.quit()
        print("BOT Finish")
    except Exception as e:
        print(f"Error in _run_selenium: {e}")
    finally:
        running = False

@app.post('/bot')
async def run_bot():
    global running
    if running:
        return jsonify({'status': 'error', 'message': 'yema 已经在看评论了，别急'}), 400
    running = True
    asyncio.create_task(viewing_website())
    return jsonify({'status': 'success', 'message': 'OK'}), 200

@app.route('/record_log', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def log_request():
    method = request.method
    url = request.url
    headers = json.dumps(dict(request.headers))
    cookies = json.dumps(request.cookies)
    body = request.get_data(as_text=True) if method in ['POST', 'PUT'] else ''
    ip_address = request.remote_addr
    log_http_request(method, url, headers, cookies, body, ip_address)
    return jsonify({'status': 'logged'})

@app.get('/log_list')
async def log_list():
    logs = get_http_request_list()
    # 处理 logs 中的 headers 和 cookies 字段，将其从 JSON 字符串转换为字典
    processed_logs = []
    for log in logs:
        method, url, headers, cookies, body, ip = log
        try:
            headers = json.loads(headers)
        except:
            headers = {}
        try:
            cookies = json.loads(cookies)
        except:
            cookies = {}
        processed_logs.append({
            'method': method,
            'url': url,
            'headers': headers,
            'cookies': cookies,
            'body': body,
            'ip': ip
        })
    return await render_template('log_list.html', logs=processed_logs)

evil_js_content = ''

@app.route('/evil.js')
async def serve_evil_js():
    global evil_js_content
    return app.response_class(evil_js_content, mimetype='application/javascript')

@app.route('/set_evil_js', methods=['GET', 'POST'])
async def set_evil_js():
    global evil_js_content
    saved = False
    if request.method == 'POST':
        evil_js_content = (await request.form)['evil_js']
        saved = True
    return await render_template('set_evil_js.html', evil_js=evil_js_content, saved=saved)

init_db()

if __name__ == '__main__':
    app.run(port=5000)