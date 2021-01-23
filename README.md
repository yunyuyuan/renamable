## Renamable

> 一个简约的批量重命名工具

* Python3.9
* PyQt5
* pyinstaller

## 使用

* 下载[renamable.rar](https://wws.lanzous.com/iKJRekntrdc)。解压缩后，直接运行`renamable.exe`
* clone项目->`python main.py`
* clone项目->`pyinstaller -D -w -i=assets/icon.ico -n renamable main.py`

## ✨Tips
需要会写正则表达式。如果你不会写，请看[教程](https://www.runoob.com/regexp/regexp-tutorial.html)。

如果你会写，其实renamable就是调用了python `re`模块的`sub`函数，例如：

`C:\users\xxx\desktop\[xx字幕组]-进击的巨人S04-1080p-E01.mp4`；`C:\users\xxx\desktop\[xx字幕组]-进击的巨人S04-1080p-E02.mp4`；`C:\users\xxx\desktop\[xx字幕组]-进击的巨人S04-1080p-E03.mp4`

等等文件想要转化成

`C:\users\xxx\desktop\01.mp4`；`C:\users\xxx\desktop\02.mp4`；`C:\users\xxx\desktop\03.mp4`。


那么输入这样写：`^\[xx字幕组\]-进击的巨人S04-1080p-E(\d+)\.mp4$`，输出这样写：`\1.mp4`
