# 我的bear blog

我很欣赏bear blog的简约，但它很多功能需要付费，于是我就在Gemini的指导下自己做了一个类似的。

## 项目结构

```
my-blog/
├── .github/              # 存放 GitHub Actions 自动化工作流
│   └── workflows/
│       └── deploy.yml
├── .gitignore            # Git 忽略文件配置
├── build.py              # 核心构建脚本
├── content/              # 网站原始内容
│   ├── pages/            # 存放独立页面 (如首页, 专题页)
│   └── posts/            # 存放博客文章
├── static/               # 存放 CSS, 图片等静态资源
└── templates/            # 存放 Jinja2 HTML 模板
```


## 本地开发流程

1.  **设置环境 (仅需一次)**
    ```bash
    # 创建并激活 Conda 环境
    conda create --name myblog python=3.10
    conda activate myblog

    # 安装依赖
    pip install jinja2
    ```

2.  **内容创作**
    -   在 `content/pages/` 中创建或修改独立页面。
    -   在 `content/posts/` 中创建或修改博客文章。

3.  **构建和预览**
    ```bash
    # 运行脚本生成网站到 public 目录
    python build.py

    # (推荐) 使用 VS Code 的 Live Server 插件右键打开 public/index.html 进行预览
    ```

## 网站部署

本网站通过 **GitHub Actions** 实现自动化部署。

当任何改动被推送到 `main` 分支后，GitHub Actions 会自动被触发。它将完成所有的构建和部署工作，并将最终的网站成品推送到 `gh-pages` 分支。网站会在几分钟后自动更新。

你唯一需要做的就是将源码推送到 `main` 分支。