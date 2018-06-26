#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
python版本：python3
依赖库：requests html2text
"""


import requests
import time
import os
import re
import html2text
import csdn_sdk


class Download_csdn_article(object):
    """
    下载csdn文章
    """
    def __init__(self):
        """
        err_file_name: 错误输出文件名。下载失败的文章编号和文章标题，输出到该文件中
        article_dir: 下载成功的文章放到该目录
        csdn: Csdn sdk类
        article_list: 文章信息列表。[{'id': 'xxxx', 'title': 'xxxx'...}, {...}, ...]
        """
        time_stamp = int(time.time())
        self.err_file_name = 'file_err{}.txt'.format(time_stamp)
        self.article_dir = 'articles{}'.format(time_stamp)
        os.path.exists(self.article_dir) or os.mkdir(self.article_dir)
        self.csdn = csdn_sdk.Csdn()
        self.csdn.get_oauth2()
        self.article_list = []

    def print_user_info(self):
        res_user_getinfo = self.csdn.user_getinfo()
        res_blog_getinfo = self.csdn.blog_getinfo()
        print('================================')
        print('||  用户名：{}'.format(res_user_getinfo['username']))
        print('||  昵称：{}'.format(res_user_getinfo['nickname']))
        print('||  博客标题：{}'.format(res_blog_getinfo['title']))
        print('||  博客副标题：{}'.format(res_blog_getinfo['subtitle']))
        print('================================')

    def _get_article_list(self):
        print('开始获取每页文章编号')
        page = 1
        while True:
            res_blog_getarticlelist = self.csdn.blog_getarticlelist(page=page)
            if 'list' not in res_blog_getarticlelist:
                break
            print('正在获取第 {page} 页文章编号'.format(page=page))
            self.article_list += res_blog_getarticlelist['list']
            page += 1
        print('共{}篇文章'.format(len(self.article_list)))

    def _handle_art_content(self, art_content, art_file_name_pre):
        """
        替换文章内容中的img链接，改为{% asset_img slug [title] %}格式
        下载文章中的图片
        """
        img_src_list = re.findall(r'!\[.*\]\(([^\n?]*).*\)', art_content)
        art_content = re.sub(
            r'!\[(?P<desc>.*)\]\([^\n?]*/(?P<img_name>[^\n?]*).*\)',
            lambda matched: '{} {} {} {} {}'.format(
                '{%',
                'asset_img',
                matched.group('img_name'),
                '[{}]'.format(matched.group('desc')) if matched.group('desc') else '',
                '%}'),
            art_content)
        img_path = '{}/{}'.format(self.article_dir, art_file_name_pre)
        os.path.exists(img_path) or os.mkdir(img_path)
        for img_src in img_src_list:
            print('下载图片 {}'.format(img_src))
            self._download_img(img_src, img_path)
        return art_content

    def _download_img(self, img_src, img_path):
        """
        把图片下载到指定路径
        """
        img_name = re.search(r'.*/(.*)', img_src).group(1)
        res = requests.get(url=img_src)
        f = open('{}/{}'.format(img_path, img_name), 'wb')
        f.write(res.content)
        f.close()

    def _get_art_content_md(self, art_id, art_file_name_pre):
        """
        获取markdown格式的文章内容
        替换img标签 并 下载图片
        在文章的开始增加用于hexo的Front-matter
        """
        print('\n\n\n\n获取文章 {} 详细信息'.format(art_id))
        res_blog_getarticle = self.csdn.blog_getarticle(num=art_id)
        if 'markdowncontent' in res_blog_getarticle and res_blog_getarticle['markdowncontent']:
            art_content = res_blog_getarticle['markdowncontent']
        elif 'content' in res_blog_getarticle and res_blog_getarticle['content']:
            art_content = html2text.html2text(res_blog_getarticle['content'])
        else:
            print('获取失败，需自行下载。')
            return None
        art_content = self._handle_art_content(art_content, art_file_name_pre)
        art_content = self._add_hexo_front_matter(
            art_content,
            res_blog_getarticle['title'],
            res_blog_getarticle['create'],
            res_blog_getarticle['tags'],
            res_blog_getarticle['categories'])
        return art_content

    def _add_hexo_front_matter(self, art_content, title, create, tags, categories):
        print('文章中添加Front-matter。title：{}|create：{}|tags：{}|categories：{}|'.format(
            title, create, tags, categories))
        art_title = re.sub(r'[:\t]+', ' ', title).lstrip().rstrip()
        art_date = create.replace('-', '/')
        art_tags = '[{}]'.format(tags)
        art_categories = '[{}]'.format(categories)
        art_content = 'title: {}\ndate: {}\ntags: {}\ncategories: {}\n---\n{}'.format(
            art_title, art_date, art_tags, art_categories, art_content)
        return art_content

    def download_article(self):
        self._get_article_list()
        file_err = open(self.err_file_name, 'w', encoding="utf-8")
        for article in self.article_list:
            # 文章的文件名前缀/保存文章中图片的目录名
            art_file_name_pre = re.sub(r'[/\\:*?"<>|\t]+', ' ', article['title']).lstrip().rstrip()
            # 获取文章内容
            art_content = self._get_art_content_md(article['id'], art_file_name_pre)
            if not art_content:
                file_err.write('文章编号：{}，文章标题：{}\n'.format(article['id'], article['title']))
                continue
            print('保存文章 {}.md'.format(art_file_name_pre))
            file_art = open('{}/{}.md'.format(self.article_dir, art_file_name_pre), 'w', encoding="utf-8")
            file_art.write(art_content)
            file_art.close()
        file_err.close()

if __name__ == '__main__':
    down_csdn_art = Download_csdn_article()
    down_csdn_art.print_user_info()
    down_csdn_art.download_article()




