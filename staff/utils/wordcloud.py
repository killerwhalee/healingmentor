from django.conf import settings

from session.models import GuidedMeditation

from PIL import Image
from collections import Counter
from konlpy.tag import Hannanum
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import io, zipfile


FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumPen.ttf"
MASK = np.array(Image.open(settings.STATIC_ROOT / "images" / "staff-mask.png"))


def get_wordcloud_from_queryset(queryset, count=4):
    # Get NLP engine
    han = Hannanum()

    # Create temporary image box
    images = []

    # Get GuidedMeditation objects
    gm_first = queryset.order_by("date_created")[:count]
    gm_last = queryset.order_by("-date_created")[count:]

    # Execute wordcloud for each question
    for field in ["question_1", "question_2", "question_3", "question_4"]:
        # Get all response for given field
        first_str = " ".join(getattr(gm.question, field) for gm in gm_first)
        last_str = " ".join(getattr(gm.question, field) for gm in gm_last)

        # Count word from response
        first_cnt = Counter(
            [text for text, tag in han.pos(first_str) if tag[0] not in "ESJX"],
        )
        last_cnt = Counter(
            [text for text, tag in han.pos(last_str) if tag[0] not in "ESJX"],
        )

        # Get first 200 most common word.
        first_cnt.most_common(200)
        last_cnt.most_common(200)

        # Create image object
        first_img = get_wordcloud(first_cnt, orange_color_func)
        last_img = get_wordcloud(last_cnt, green_color_func)

        # Create image name
        first_filename = f"wordcloud_first_{field}.png"
        last_filename = f"wordcloud_last_{field}.png"

        # Append image data to images list
        images.append((first_filename, first_img))
        images.append((last_filename, last_img))

    # Create buffer for zip file
    zip_buffer = io.BytesIO()

    # Write images into zip buffer
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, image in images:
            image_buffer = io.BytesIO()
            image.save(image_buffer, format="PNG")
            zip_file.writestr(filename, image_buffer.getvalue())

    zip_buffer.seek(0)

    return zip_buffer


def orange_color_func(*args, **kwargs):
    return "hsl({:d},{:d}%, {:d}%)".format(
        np.random.randint(0, 36), 100, np.random.randint(7, 50)
    )


def green_color_func(*args, **kwargs):
    return "hsl({:d},{:d}%, {:d}%)".format(
        np.random.randint(120, 165), 100, np.random.randint(30, 40)
    )


def get_wordcloud(text, color_func):
    wordcloud = WordCloud(
        font_path=FONT_PATH,
        mask=MASK,
        background_color="white",
        height=400,
        width=400,
        max_font_size=42,
        color_func=color_func,
    ).generate_from_frequencies(dict(text))

    font_name = fm.FontProperties(fname=FONT_PATH, size=10).get_name()
    plt.rc("font", family=font_name)

    return wordcloud.to_image()
