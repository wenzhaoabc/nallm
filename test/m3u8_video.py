import urllib.request
import m3u8

# 下载m3u8文件
m3u8_master = m3u8.load("index.m3u8")

# 创建一个空的文件来保存视频数据
with open('video.ts', 'wb') as f:
    for segment in m3u8_master.segments:
        # 下载每个视频片段
        r = urllib.request.urlopen(segment.absolute_uri)

        # 将视频片段的数据写入文件
        f.write(r.read())
