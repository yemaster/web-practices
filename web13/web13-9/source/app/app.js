const express = require('express');
const app = express();
const ejs = require('ejs');

// 处理根路径请求
app.get('/', (req, res) => {
    const input = req.query.name || 'guest';
    const html = `<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>web13-9</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
        }

        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        button {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }

        #greeting {
            margin-top: 20px;
            font-size: 18px;
            color: #333;
        }
    </style>
</head>

<body>
    <h1>web13-9</h1>
    <div class="container">
        <form action="/" method="get">
            <label for="name">Enter Your Name:</label>
            <input type="text" id="name" name="name" placeholder="Your Name">
            <button type="submit">Submit</button>
        </form>
        <div id="greeting">
            Hello, ${input}
        </div>
    </div>
</body>

</html>`;
    const template = ejs.render(html, { name: input });
    res.send(template);
});

// 启动服务器
const port = 8000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});