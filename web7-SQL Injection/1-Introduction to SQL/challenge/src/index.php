<?php 
if (isset($_GET["sql"])) {
    $sql = $_GET["sql"];
    header('Content-Type: application/json');
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        echo json_encode(mysqli_fetch_all($result, MYSQLI_ASSOC));
    } else {
        echo json_encode([]);
    }
    die();
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户列表</title>
    <style>
        /* 基础样式重置 */
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
            line-height: 1.5;
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

        .user-list-container {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .user-list-container:hover {
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }

        .user-table {
            width: 100%;
            border-collapse: collapse;
        }

        .table-header {
            background-color: #f7f8fa;
        }

        .user-table th,
        .user-table td {
            padding: 1rem 1.5rem;
            text-align: left;
        }

        .user-table th {
            color: #4e5969;
            font-weight: 600;
            font-size: 0.95rem;
            position: relative;
        }

        .user-table th::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 1px;
            background-color: #f0f2f5;
        }

        .user-table tbody tr {
            transition: background-color 0.2s ease;
        }

        .user-table tbody tr:hover {
            background-color: #f7f8fa;
        }

        .user-table tbody tr:not(:last-child) {
            border-bottom: 1px solid #f0f2f5;
        }

        /* 列样式 */
        .id-column {
            width: 10%;
            color: #165dff;
            font-weight: 500;
        }

        .username-column {
            width: 20%;
        }

        .info-column {
            width: 70%;
            color: #666;
        }

        /* 用户名和头像样式 */
        .user-info {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: #e8f3ff;
            color: #165dff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9rem;
            transition: transform 0.2s ease;
        }

        .user-table tbody tr:hover .avatar {
            transform: scale(1.05);
        }

        .username {
            font-weight: 500;
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }

            .header h1 {
                font-size: 1.6rem;
            }

            .user-table th,
            .user-table td {
                padding: 0.8rem 1rem;
            }

            .id-column {
                width: 15%;
            }

            .username-column {
                width: 25%;
            }

            .info-column {
                width: 60%;
                font-size: 0.9rem;
            }
        }

        @media (max-width: 480px) {
            .info-column {
                display: none;
            }

            .id-column {
                width: 20%;
            }

            .username-column {
                width: 80%;
            }
        }
    </style>
</head>
<body>
    <div class="page-container">
        <div class="header">
            <h1>开发者列表</h1>
            <p>看看我们强大的 SQL 开发者</p>
        </div>
        
        <div class="user-list-container">
            <table class="user-table">
                <thead class="table-header">
                    <tr>
                        <th class="id-column">ID</th>
                        <th class="username-column">用户名</th>
                        <th class="info-column">信息</th>
                    </tr>
                </thead>
                <tbody id="user-table-body">
                </tbody>
            </table>
        </div>
    </div>
    <script>
        fetch('index.php?sql=SELECT%20*%20FROM%20users')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('user-table-body');
                data.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.id}</td>
                        <td>
                            <div class="user-info">
                                <div class="avatar">${user.username.charAt(0).toUpperCase() + user.username.charAt(1).toUpperCase()}</div>
                                <span class="username">${user.username}</span>
                            </div>
                        </td>
                        <td class="info-column">${user.motto}</td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching user data:', error));
    </script>
</body>
</html>
