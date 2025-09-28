#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, render_template_string
from json import loads, dumps
from python_jwt import generate_jwt, verify_jwt, process_jwt
from jwcrypto import jwk
from datetime import timedelta
import base64
import os
import subprocess
import hashlib


app = Flask(__name__)
app.config['SECRET_KEY'] = hashlib.md5(os.urandom(24)).hexdigest()


jwt_key = jwk.JWK.generate(kty='RSA', size=2048)

users={}

users['guest'] = {
    'password': 'guest',
    'role': 'guest',
    'name': 'guest',
    'department': 'guest'
}


tobacco_companies = [
    {
        'id': 1,
        'name': '测试集团1',
        'license': 'CS2025001',
        'status': '正常',
        'location': '北京市朝阳区',
        'products': ['牙膏', '牙刷', '洗发水']
    },
    {
        'id': 2, 
        'name': '测试集团2',
        'license': 'CS2025002',
        'status': '正常',
        'location': '山东省济南市',
        'products': ['把子肉', '四喜丸子']
    },
    {
        'id': 3,
        'name': '测试集团3',
        'license': 'CS2025003', 
        'status': '待审核',
        'location': '湖南省长沙市',
        'products': ['奶茶', '辣椒炒肉拌面']
    }
]

def base64url_decode(inp):
    
    padding = 4 - len(inp) % 4
    if padding:
        inp += '=' * padding
    return base64.urlsafe_b64decode(inp)

def base64url_encode(inp):
    
    return base64.urlsafe_b64encode(inp).decode('ascii').rstrip('=')

@app.route('/')
def index():
    
    return 'index.html'

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        
        if username in users and users[username]['password'] == password:
            user_info = users[username].copy()
            user_info['username'] = username
            
            
            payload = {
                'username': username,
                'role': user_info['role'],
                'name': user_info['name'],
                'department': user_info['department']
            }
            
            token = generate_jwt(payload, jwt_key, 'PS256', timedelta(hours=2))
            
            return jsonify({
                'success': True,
                'token': token,
                'user': user_info
            })
        else:
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401
    
    return 'login.html'

@app.route('/dashboard')
def dashboard():
    
    return 'dashboard.html'

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'valid': False, 'message': '未提供token'}), 400
        
        try:
            header, payload = verify_jwt(token, jwt_key, ['PS256'])
            return jsonify({
                'valid': True,
                'payload': payload
            })
        except Exception as e:
            return jsonify({
                'valid': False, 
                'message': f'Token验证失败: {str(e)}'
            }), 401
            
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': f'请求处理失败: {str(e)}'
        }), 500

@app.route('/api/companies')
def get_companies():
    
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': '未提供认证token'}), 401
            
        token = auth_header[len('Bearer '):]
        
        
        try:
            header, payload = verify_jwt(token, jwt_key, ['PS256'])
            
            
            if payload.get('role') in ['inspector', 'manager', 'admin']:
                return jsonify({
                    'success': True,
                    'companies': tobacco_companies,
                    'user_role': payload.get('role')
                })
            else:
                return jsonify({'error': '权限不足'}), 403
                
        except Exception as e:
            return jsonify({'error': f'Token验证失败: {str(e)}'}), 401
            
    except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 500

@app.route('/api/report/generate', methods=['POST'])
def generate_report():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': '未提供认证token'}), 401
            
        token = auth_header[len('Bearer '):]
        
        
        try:
            header, payload = verify_jwt(token, jwt_key, ['PS256'])
            
            
            if payload.get('role') not in ['manager', 'admin']:
                return jsonify({
                    'error': '权限不足，只有经理和管理员可以生成报告',
                    'current_role': payload.get('role', 'unknown')
                }), 403
            
            data = request.get_json()
            company_id = data.get('company_id')
            report_template = data.get('template', '')
            custom_title = data.get('title', '企业监管报告')
            
            # 查找企业信息
            company = None
            for comp in tobacco_companies:
                if comp['id'] == company_id:
                    company = comp
                    break
            
            if not company:
                return jsonify({'error': '未找到指定企业'}), 404
            
            # 获取用户信息
            user_name = payload.get('name', '未知用户')
            user_dept = payload.get('department', '未知部门')


            if "{{" in report_template:
                return jsonify({'error': 'bad template'}), 400

            if report_template:
                
                template_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{custom_title}</title>
    <style>
        body {{ font-family: SimSun, serif; margin: 40px; }}
        .header {{ text-align: center; border-bottom: 2px solid #8B4513; padding-bottom: 20px; }}
        .content {{ margin-top: 30px; }}
        .signature {{ margin-top: 50px; text-align: right; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{custom_title}</h1>
        <p>企业监管报告</p>
    </div>
    
    <div class="content">
        <h2>企业基本信息</h2>
        <p><strong>企业名称：</strong>{company['name']}</p>
        <p><strong>许可证号：</strong>{company['license']}</p>
        <p><strong>运营状态：</strong>{company['status']}</p>
        <p><strong>所在地区：</strong>{company['location']}</p>
        <p><strong>主要产品：</strong>{', '.join(company['products'])}</p>
        
        <h2>自定义报告内容</h2>
        <div>
            {report_template}
        </div>
        
        <div class="signature">
            <p>报告生成人：{user_name}</p>
            <p>所属部门：{user_dept}</p>
            <p>生成时间：{{{{ "现在的时间" }}}}</p>
        </div>
    </div>
</body>
</html>
                """
                
                
                try:
                    rendered_html = render_template_string(template_content)
                    return jsonify({
                        'success': True,
                        'report_html': rendered_html,
                        'message': '报告生成成功'
                    })
                except Exception as e:
                    return jsonify({
                        'error': f'模板渲染失败: {str(e)}',
                        'hint': '检查模板语法是否正确'
                    }), 400
            else:
                
                default_template = f"""
                <h3>监管结论</h3>
                <p>经过全面检查，{company['name']} 企业运营状况良好，符合国家相关规定。</p>
                <p>建议继续保持规范经营，定期接受监管部门检查。</p>
                """
                
                template_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{custom_title}</title>
    <style>
        body {{ font-family: SimSun, serif; margin: 40px; }}
        .header {{ text-align: center; border-bottom: 2px solid #8B4513; padding-bottom: 20px; }}
        .content {{ margin-top: 30px; }}
        .signature {{ margin-top: 50px; text-align: right; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{custom_title}</h1>
        <p>企业监管报告</p>
    </div>
    
    <div class="content">
        <h2>企业基本信息</h2>
        <p><strong>企业名称：</strong>{company['name']}</p>
        <p><strong>许可证号：</strong>{company['license']}</p>
        <p><strong>运营状态：</strong>{company['status']}</p>
        <p><strong>所在地区：</strong>{company['location']}</p>
        <p><strong>主要产品：</strong>{', '.join(company['products'])}</p>
        
        {default_template}
        
        <div class="signature">
            <p>报告生成人：{user_name}</p>
            <p>所属部门：{user_dept}</p>
        </div>
    </div>
</body>
</html>
                """
                
                return jsonify({
                    'success': True,
                    'report_html': template_content,
                    'message': '默认报告生成成功'
                })
                
        except Exception as e:
            return jsonify({'error': f'Token验证失败: {str(e)}'}), 401
            
    except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)