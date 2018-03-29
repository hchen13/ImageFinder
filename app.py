import argparse
import os
from datetime import datetime
from io import BytesIO

import numpy as np
import requests
from PIL import Image
from matplotlib import pyplot as plt
from selenium import webdriver

BAIDU_IMAGE = 'http://image.baidu.com/'
FLAGS = None


def init_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')

    return webdriver.Chrome(options=options)


browser = init_driver(True)


def search(keyword, limit=10):
    print("Searching the web for images of `{}`...".format(keyword))
    browser.get(BAIDU_IMAGE)
    browser.find_element_by_css_selector("#kw").send_keys(keyword)  # find input element and insert kw
    browser.find_element_by_css_selector("#homeSearchForm > span.s_search").click()  # click search
    images = browser.find_elements_by_css_selector('img.main_img.img-hover')
    current_len = len(images)
    tick = datetime.now()
    while len(images) < limit:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        images = browser.find_elements_by_css_selector('img.main_img.img-hover')
        tock = datetime.now()
        if current_len == len(images):
            elapsed = tock - tick
            if elapsed.total_seconds() > 5:
                break
        else:
            tick = datetime.now()
        current_len = len(images)
    print("Found {} images in total".format(min(limit, len(images))))
    return images[:limit]


def load_image(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        # "Cookie": "device_id=bdb99c41f693c372a30387f3b564733a; s=em1b7ydxvp; __utma=1.208621711.1507526003.1507526003.1507526003.1; __utmz=1.1507526003.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_a_token=bd10649447b05a985dfe102ce646520af55111cd; xqat=bd10649447b05a985dfe102ce646520af55111cd; xq_r_token=0ce0fb904ca069a26120631b8d5043e8c8fd1ba4; xq_token_expire=Fri%20Nov%2003%202017%2013%3A42%3A37%20GMT%2B0800%20(CST); xq_is_login=1; u=5984336726; bid=81b5763c50d6ae9b80baefd6038e282e_j8jr3py1; aliyungf_tc=AQAAAGhbWmq9zgwAChuWtiFPY+q7q3YD; Hm_lvt_1db88642e346389874251b5a1eded6e3=1507776474,1507883182,1508154298,1508316742; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1508321713"
    }
    try:
        response = requests.get(url, headers=headers)
    except ConnectionError as e:
        print("网络连接错误, 加载图片失败\n")
        return None
    if response.status_code != 200:
        print("请求图片失败: status code {}".format(response.status_code))
    raw = response.content
    image = Image.open(BytesIO(raw))
    return image


def extract_image(element):
    image_url = element.get_attribute('src')
    return load_image(image_url)


def save_image(image, dest, filename):
    path = os.path.join(dest, filename)
    image.save(path, 'jpeg')


def main():
    results = search(FLAGS.keyword, FLAGS.limit)
    images = map(extract_image, results)
    dest_dir = os.path.join(FLAGS.dir, FLAGS.keyword)
    ensure_dir_exists(dest_dir)
    print("Saving images..")
    for i, img in enumerate(images):
        save_image(img, dest_dir, "{}.jpg".format(i))
    print("All images saved.")


def display_image(*images, col=None):
    """
    Plot the images

    :param images: arbitrary number of ndarrays each of which represents an image
    :param title: optionally set the plot title
    :param col: optionally change the number of images shown in one row,
                default to the number of images to be displayed
    :return: None
    """
    if col is None:
        col = len(images)
    plt.figure(figsize=(8, 4.5))
    row = np.math.ceil(len(images) / col)
    for i, image in enumerate(images):
        plt.subplot(row, col, i + 1)
        plt.imshow(image, cmap='gray')
    plt.show()


def ensure_dir_exists(path):
    if not os.path.exists(path):
        print("Create directory {} to store the images".format(path))
        os.makedirs(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir',
        type=str,
        default='./',
        help='Root directory where a folder named after the keyword will be created, which will contain all the downloaded images'
    )
    parser.add_argument(
        '--keyword',
        type=str,
        default='',
        help="The keyword for searching the web"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help='The maximum number of images to be downloaded'
    )
    FLAGS, unparsed = parser.parse_known_args()
    main()
    browser.close()