from moviepy import VideoFileClip, ImageClip, clips_array
from PIL import Image, ImageDraw, ImageFont
import numpy as np

img_path = "More_demos/ycb20/BGR.png"
vid_path = "More_demos/ycb20/pybullet_video.avi"
out_path = "More_demos/ycb20/stacked.mp4"

TITLE_H = 96          # 标题栏高度（明显加高）
LINE_H = 6            # 分割线高度
PAD_X = 24            # 标题左边距
FONT_SIZE = 48        # 字体明显变大

def load_font(size):
    """
    优先使用更好看的粗体无衬线字体
    """
    font_candidates = [
        "DejaVuSans-Bold.ttf",
        "DejaVuSans.ttf",
        "Arial.ttf"
    ]
    for f in font_candidates:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            pass
    return ImageFont.load_default()

def make_title_bar(width: int, text: str, height: int = TITLE_H) -> np.ndarray:
    img = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = load_font(FONT_SIZE)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_h = bbox[3] - bbox[1]
    y = (height - text_h) // 2

    draw.text((PAD_X, y), text, font=font, fill=(255, 255, 255))
    return np.array(img)

def add_title_bar_to_clip(clip, title: str):
    w, h = clip.size
    bar = make_title_bar(w, title, TITLE_H)

    def f(get_frame, t):
        frame = get_frame(t)
        return np.vstack([bar, frame])

    return (
        clip
        .transform(f, apply_to="mask")
        .with_memoize((w, h + TITLE_H))
    )

def make_divider_clip(width: int, duration: float, height: int = LINE_H):
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    arr[:] = (255, 255, 255)   # 白色分割线
    return ImageClip(arr).with_duration(duration)

# 读视频
video = VideoFileClip(vid_path)

# 图片 → 静止视频 → 同宽
img = ImageClip(img_path).with_duration(video.duration)
img = img.resized(width=video.w)

# 加标题栏（文案按你的要求）
img_labeled = add_title_bar_to_clip(img, "Input Image")
video_labeled = add_title_bar_to_clip(video, "Simulation of Reconstructed Scene")

# 分割线
divider = make_divider_clip(video.w, video.duration, LINE_H)

# 竖向拼接
stacked = clips_array([
    [img_labeled],
    [divider],
    [video_labeled]
])

# 导出
stacked.write_videofile(
    out_path,
    fps=video.fps,
    codec="libx264",
    audio=False,
    preset="medium"
)
