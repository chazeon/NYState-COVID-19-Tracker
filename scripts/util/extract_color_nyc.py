import subprocess
from PIL import Image
from io import BytesIO
import json

def render_pdf(fname, draw="mutool draw"):
    opts = ["-o", "-", "-r", "216"]
    ret = subprocess.run(
        [*draw.split(), *opts, fname],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if len(ret.stderr): raise RuntimeError(ret.stderr.decode())
    return ret.stdout


def get_bitmap_handler(bitmap, normalize=(2376, 3024)):
    image = Image.open(BytesIO(bitmap))
    pixels = image.load()
    transform = lambda x, y: (x * image.size[0] / normalize[0], y * image.size[1] / normalize[1])
    def handler(x, y):
        x, y = transform(x, y)
        return pixels[round(x), round(y)]
    return handler


def extract_pdf_colors(fname, wpd_info):

    bitmap = render_pdf(fname)

    with open(wpd_info) as fp:
        data = json.load(fp)["datasetColl"]

    handler = get_bitmap_handler(bitmap)

    for i, dataset in enumerate(data):
        for j, point in enumerate(dataset["data"]):
            yield (100 * i + j + 1, handler(*point["value"]))
 

def extract_pdf_data(fname, wpd_info="data/test_map_coords.json"):
    data = dict(extract_pdf_colors(fname, wpd_info))
    color_map = dict((c, v) for v, c in data.items() if v < 100)
    for k in data.keys():
        if k < 100: continue
        yield k, color_map[data[k]]
