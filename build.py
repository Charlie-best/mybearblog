import os
import shutil
from jinja2 import Environment, FileSystemLoader

# --- 配置 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_POSTS_DIR = os.path.join(BASE_DIR, 'content/posts')
CONTENT_PAGES_DIR = os.path.join(BASE_DIR, 'content/pages')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

def parse_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    parts = file_content.split('---', 2)
    if len(parts) < 3: return None
        
    metadata_str, body_html = parts[1], parts[2].strip()
    
    content_data = {}
    for line in metadata_str.strip().split('\n'):
        key, value = line.split(':', 1)
        content_data[key.strip()] = value.strip()
    
    content_data['content'] = body_html
    return content_data

def main():
    print("开始构建网站...")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    os.makedirs(os.path.join(PUBLIC_DIR, 'posts'))

    # --- 1. 自动处理所有独立页面 (index.html, topics.html, etc.) ---
    page_template = env.get_template('page.html')
    for filename in os.listdir(CONTENT_PAGES_DIR):
        if filename.endswith('.html'):
            filepath = os.path.join(CONTENT_PAGES_DIR, filename)
            page_data = parse_content(filepath)
            if not page_data: continue

            rendered_html = page_template.render(title=page_data['title'], page=page_data)
            output_filepath = os.path.join(PUBLIC_DIR, filename)
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(rendered_html)

    # --- 2. 处理所有博客文章 ---
    all_posts = []
    # ... (这部分代码和之前完全一样，无需改动) ...
    for filename in os.listdir(CONTENT_POSTS_DIR):
        if filename.endswith('.html'):
            filepath = os.path.join(CONTENT_POSTS_DIR, filename)
            post = parse_content(filepath)
            if not post: continue
            
            post['slug'] = os.path.splitext(filename)[0]
            all_posts.append(post)

            post_template = env.get_template('post.html')
            rendered_html = post_template.render(title=post['title'], post=post)
            
            output_filepath = os.path.join(PUBLIC_DIR, 'posts', f"{post['slug']}.html")
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
    
    # --- 3. 生成博客列表页 (blog.html) ---
    all_posts.sort(key=lambda p: p.get('date', ''), reverse=True)
    blog_template = env.get_template('blog.html')
    blog_html = blog_template.render(title="Blog", posts=all_posts)
    with open(os.path.join(PUBLIC_DIR, 'blog.html'), 'w', encoding='utf-8') as f:
        f.write(blog_html)

    # --- 4. 复制静态文件 ---
    shutil.copytree(STATIC_DIR, os.path.join(PUBLIC_DIR, 'static'))

    print(f"网站构建成功！")

if __name__ == "__main__":
    main()