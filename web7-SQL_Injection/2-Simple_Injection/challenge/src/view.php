<?php 
include "connect.php";
$id = $_GET['id'] ?? "1";
$sql = "SELECT * FROM users WHERE id=\"$id\"";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    $user = mysqli_fetch_assoc($result);
} else {
    die("用户不存在!");
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户详情 - 开发者信息</title>
    <style>
        /* 基础样式重置（复用原页面风格） */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        body {
            background-color: #f0f2f5;
            color: #1d2129;
            padding: 2rem;
            line-height: 1.6;
        }

        .page-container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            margin-bottom: 2rem;
            text-align: center;
        }

        .header h1 {
            color: #165dff;
            font-weight: 600;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .header p {
            color: #666;
            font-size: 1rem;
        }

        /* 详情页核心样式 */
        .user-detail-container {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            padding: 2rem;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 2rem;
        }

        .user-detail-container:hover {
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }

        /* 左侧头像与基础信息区 */
        .avatar-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1rem;
            border-right: 1px solid #f0f2f5;
        }

        .avatar-large {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background-color: #e8f3ff;
            color: #165dff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
        }

        .avatar-large:hover {
            transform: scale(1.05);
        }

        .basic-info {
            text-align: center;
            width: 100%;
        }

        .basic-info .username-large {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1d2129;
            margin-bottom: 0.3rem;
        }

        .basic-info .user-id {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px dashed #f0f2f5;
        }

        .join-date {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #4e5969;
            font-size: 0.95rem;
        }

        .join-date svg {
            width: 16px;
            height: 16px;
            fill: #165dff;
        }

        /* 右侧详细信息区 */
        .detail-info-section {
            padding: 1rem 0;
        }

        .info-group {
            margin-bottom: 2rem;
        }

        .info-title {
            color: #4e5969;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            padding-left: 0.5rem;
            border-left: 3px solid #165dff;
        }

        .info-item {
            display: flex;
            margin-bottom: 1rem;
            align-items: flex-start;
        }

        .info-label {
            width: 120px;
            color: #666;
            font-weight: 500;
        }

        .info-content {
            flex: 1;
            color: #1d2129;
        }

        /* 技能标签样式 */
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin-top: 0.5rem;
        }

        .skill-tag {
            background-color: #e8f3ff;
            color: #165dff;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            transition: background-color 0.2s ease;
        }

        .skill-tag:hover {
            background-color: #d1eaff;
        }

        /* 返回列表按钮 */
        .back-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #165dff;
            text-decoration: none;
            font-weight: 500;
            padding: 0.6rem 1.2rem;
            border: 1px solid #165dff;
            border-radius: 8px;
            margin-top: 1rem;
            transition: all 0.2s ease;
        }

        .back-btn:hover {
            background-color: #165dff;
            color: #fff;
        }

        .back-btn svg {
            width: 16px;
            height: 16px;
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }

            .header h1 {
                font-size: 1.6rem;
            }

            .user-detail-container {
                grid-template-columns: 1fr;
                padding: 1.5rem;
                gap: 1.5rem;
            }

            .avatar-section {
                border-right: none;
                border-bottom: 1px solid #f0f2f5;
                padding-bottom: 1.5rem;
            }

            .info-item {
                flex-direction: column;
            }

            .info-label {
                margin-bottom: 0.3rem;
                width: auto;
            }
        }

        @media (max-width: 480px) {
            .avatar-large {
                width: 100px;
                height: 100px;
                font-size: 2rem;
            }

            .basic-info .username-large {
                font-size: 1.2rem;
            }

            .info-group {
                margin-bottom: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="page-container">
        <!-- 页面头部 -->
        <div class="header">
            <h1>用户详情</h1>
            <p>查看开发者的详细信息与专业能力</p>
        </div>

        <!-- 详情内容容器 -->
        <div class="user-detail-container">
            <!-- 左侧：头像与基础信息 -->
            <div class="avatar-section">
                <div class="avatar-large">AL</div>
                <div class="basic-info">
                    <div class="username-large"><?=$user["username"];?></div>
                    <div class="user-id">用户ID: <?=$id;?></div>
                </div>
                <a href="/" class="back-btn">
                    <svg viewBox="0 0 24 24">
                        <path fill="currentColor" d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
                    </svg>
                    返回列表
                </a>
            </div>

            <!-- 右侧：详细信息 -->
            <div class="detail-info-section">
                <!-- 座右铭与简介 -->
                <div class="info-group">
                    <h3 class="info-title">个人简介</h3>
                    <div class="info-item">
                        <span class="info-label">座右铭：</span>
                        <span class="info-content"><?=$user["motto"];?></span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">自我描述：</span>
                        <span class="info-content"><?=$user["info"];?></span>
                    </div>
                </div>

                <!-- 专业信息 -->
                <div class="info-group">
                    <h3 class="info-title">专业能力</h3>
                    <div class="info-item">
                        <span class="info-label">擅长技能：</span>
                        <div class="info-content">
                            <div class="skills-container">
                                <span class="skill-tag">吹牛</span>
                                <span class="skill-tag">装逼</span>
                                <span class="skill-tag">强大的SQL技能</span>
                            </div>
                        </div>
                    </div>
                    <div class="info-item">
                        <span class="info-label">认证资质：</span>
                        <span class="info-content">第一吹牛 SQL 大师</span>
                    </div>
                </div>

                <!-- 联系信息 -->
                <div class="info-group">
                    <h3 class="info-title">联系与作品</h3>
                    <div class="info-item">
                        <span class="info-label">邮箱：</span>
                        <span class="info-content">真正的大师不需要邮箱</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">GitHub：</span>
                        <span class="info-content">真正的大师不需要 Github</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">代表作品：</span>
                        <span class="info-content">真正的大师不需要代表作品</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>