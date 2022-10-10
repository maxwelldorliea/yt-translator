import math
import os
import time
import xml.etree.ElementTree as ElementTree
from html import unescape
from typing import Dict, Optional

from pytube import request
from pytube.helpers import safe_filename, target_directory

class Caption:

    def __init__(self, caption_track: Dict):

        self.url = caption_track.get("baseUrl")

        name_dict = caption_track['name']
        if 'simpleText' in name_dict:
            self.name = name_dict['simpleText']
        else:
            for el in name_dict['runs']:
                if 'text' in el:
                    self.name = el['text']

        self.code = caption_track["vssId"]

        self.code = self.code.strip('.')

    @property
    def xml_captions(self) -> str:

        return request.get(self.url)

    def generate_srt_captions(self) -> str:

        return self.xml_caption_to_srt(self.xml_captions)

    @staticmethod
    def float_to_srt_time_format(d: float) -> str:

        fraction, whole = math.modf(d/1000)
        time_fmt = time.strftime("%H:%M:%S,", time.gmtime(whole))
        ms = f"{fraction:.3f}".replace("0.", "")
        return time_fmt + ms

    def xml_caption_to_srt(self, xml_captions: str) -> str:

        segments = []
        root = ElementTree.fromstring(xml_captions)
        count_line = 0
        for i, child in enumerate(list(root.findall('body/p'))):
        
            text = ''.join(child.itertext()).strip()
            if not text:
                continue
            count_line += 1
            caption = unescape(text.replace("\n", " ").replace("  ", " "),)
            try:
                duration = float(child.attrib["d"])
            except KeyError:
                duration = 0.0
            start = float(child.attrib["t"])
            end = start + duration
            try:
                end2 = float(root.findall('body/p')[i+2].attrib['t'])
            except:
                end2 = float(root.findall('body/p')[i].attrib['t']) + duration
            sequence_number = i + 1  # convert from 0-indexed to 1.
            line = "{seq}\n{start} --> {end}\n{text}\n".format(
                seq=count_line,
                start=self.float_to_srt_time_format(start),
                end=self.float_to_srt_time_format(end2),
                text=caption,
            )
            segments.append(line)

        return "\n".join(segments).strip()

    def download(
        self,
        title: str,
        srt: bool = True,
        output_path: Optional[str] = None,
        filename_prefix: Optional[str] = None,
    ) -> str:

        if title.endswith(".srt") or title.endswith(".xml"):
            filename = ".".join(title.split(".")[:-1])
        else:
            filename = title

        if filename_prefix:
            filename = f"{safe_filename(filename_prefix)}{filename}"

        filename = safe_filename(filename)

        filename += f" ({self.code})"

        if srt:
            filename += ".srt"
        else:
            filename += ".xml"

        file_path = os.path.join(target_directory(output_path), filename)

        with open(file_path, "w", encoding="utf-8") as file_handle:
            if srt:
                file_handle.write(self.generate_srt_captions())
            else:
                file_handle.write(self.xml_captions)

        return file_path

    def __repr__(self):
        return '<Caption lang="{s.name}" code="{s.code}">'.format(s=self)
