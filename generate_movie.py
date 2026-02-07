from moviepy import VideoFileClip, ImageClip, clips_array

img_path = "More_demos/ycb1/BGR.png"
vid_path = "More_demos/ycb1/pybullet_video.avi"
out_path = "More_demos/ycb1/stacked.mp4"

video = VideoFileClip(vid_path)

# 图片做成一个“静止视频”，长度与原视频一致
img = (ImageClip(img_path)
       .with_duration(video.duration))

# 统一宽度：把图片缩放到视频同宽（避免拼接时报尺寸不一致）
img = img.resized(width=video.w)

# 竖向拼接：两行一列
stacked = clips_array([[img],
                       [video]])

# 导出 mp4
stacked.write_videofile(
    out_path,
    fps=video.fps,
    codec="libx264",
    audio=False,          # 你这个模拟视频一般没音频；有需要再改 True
    preset="medium"
)
