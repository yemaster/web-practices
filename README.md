# web-practices

CTF web 新手从零练习题库的源代码（包括题目附件和 Dockerfile）。

**在线训练平台**：[https://ctf.abstrax.cn](https://ctf.abstrax.cn)。另外，每个专题都放置了具体的训练链接，如果出 404 啥的就说明题目下架了，反正源码都在了，自己本地训练也是很方便的。

每道题目有一个文件夹，文件夹的构成如下：

- source: 存放 题目的源代码，包括 docker 的构建脚本
- archive.zip: 存放附件题的附件
- solution: 存放题目题解

部分题目因为题目描述不清等原因在之后可能会更新，另外之后可能会补充题目的题解。

## 目录

这里只放题目的名称，具体题目信息请点入具体的题目文件夹中的 `README.md` 来进行查看。

### Web0-基础环境搭建

在线练习：[Web0-基础环境搭建](https://ctf.u5tc.cn/games/4)

- [跑个 Shell 看看](./web0/shell)
- [跑个 PHP 看看](./web0/php)
- [跑个 Python 看看](./web0/python)
- [跑个 JavaScript 看看](./web0/js)
- [跑个 Docker 看看](./web0/docker)

### Web1-敏感信息泄露

- gedit备份文件泄露
- vim备份文件泄露
- 网站备份文件泄露
- .git目录泄露
- 敏感文件泄露综合练习

### Web2-简单 js 脚本编写和 F12 调试

- 取石子游戏
- js小测
- 我什么都可以交代的
- 口算天天练
- 测测need手速
- 真的什么东西都能发吗（题目描述不清）

### Web3-Python,PHP与Linux命令基础

### Web4-PHP文件包含

- 什么都不防
- 我就是个记事的
- 没有了她，我也要拿到flag
- 我都没输出，你是怎么知道的
- php out!!!
- yema is best（未通过测试）

### Web5-PHP文件上传

- 传传need马
- 传传need马2
- 传传need马3
- 传传need马4
- 传传need马5（未通过测试）
- 传传need马6（未通过测试）
- 传传need马7
- 传传need马8

### Web6-PHP反序列化

- 初识反序列化
- 初识POP链
- wakeup
- destruct
- 没有O
- 不是yema，是yemama
- yema out！！！
- yema，找到你啦
- 引用传值
- [强网S8]Platform（未通过测试）
