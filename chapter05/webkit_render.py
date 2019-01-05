#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午10:09

try:
    from PySide.QtGui import QApplication
    from Pyside.QtCore import QUrl, QEventLoop, QTimer
    from Pyside.QtWebkit import QWebview
except ImportError:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QUrl, QEventLoop, QTimer
    from PyQt4.QtWebkit import QWebView
import lxml.html
import downloader

def direct_download(url):
    download = downloader.Downloader()
    return downloader(url)

def webkit_download(url):
    app = QApplication([])
    webview = QWebView()
    webview.loadFinished.connect(app.quit)
    webview.load(url)
    app.exec_() # delay here until download finished
    return webview.page().mainFrame().toHtml()

def parse(html):
    tree = lxml.html.fromstring(html)
    print tree.cssselect('#result')[0].text_content()

def main():
    url = 'http://example.webscraping.com/dynamic'
    parse(direct_download(url))
    parse(webkit_download(url))
    return

    print len(r.html)

if __name__ == '__main__':
    main()