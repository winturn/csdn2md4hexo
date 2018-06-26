# csdn2md4hexo

以markdown格式下载csdn博客文章，转换为hexo博客所需的文章格式。<br>
并将文章中用到的图片下载到本地，<br>
文章中用到图片的地方由 `![图片描述](http://www.图片链接.com/图片.jpg)` 改为 `{% asset_img slug [title] %}` 格式<br>
在文章的开始添加Front-matter<br>

# 使用方法

## 在csdn开放平台创建新应用，并获取App Key 和 App Secret
链接：`http://open.csdn.net/apps/createapp`<br>

## 更新配置文件
修改conf.py文件，填写从csdn开放平台获取到的App Key 和 App Secret<br>
填写博主用户名和密码<br>

## 运行脚本
```
python main.py
```

## 输出
下载的文章，保存到当前目录的`./articles`目录下，文件名为`文章标题.md`。<br>
文章中依赖的图片，保存到`./articles/文章标题`目录下。<br>
下载失败的文章标题，保存到当前目录的`./file_err.txt`文件中。<br>

## 将文章放到hexo博客中
假如<br>
  hexo博客路径：/home/hexo/blog<br>
  执行该脚本的路径：/home/hexo<br>
cp /home/hexo/articles/* /home/hexo/blog/source/_posts<br>

## 注
如果你的文章中包含的代码类似`{% url http://www.baidu.com %}`，需要自行用`raw`标签包含起来。<br>
```
{% raw %}
{% url http://www.baidu.com %}
{% endraw %}
```

