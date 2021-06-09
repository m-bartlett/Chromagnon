#!/usr/bin/python3
from io import BytesIO
import os
import pathlib
import struct

tab_file = sorted(
                    list(
                        pathlib.Path(f"~/.config/vivaldi/Default/Sessions/")
                        .expanduser()
                        .glob("Tabs*")
                    ),
                    key=lambda p: p.stat().st_mtime
                )[-1]

SNSS_MAGIC = 0x53534E53

tabs=set()
with tab_file.open('rb') as f:
    f.seek(0, os.SEEK_END)
    end = f.tell()
    f.seek(0, os.SEEK_SET)
    magic = struct.unpack('i', f.read(4))[0]
    if magic != SNSS_MAGIC:
        raise Exception("Invalid file header!")
    version = struct.unpack('i', f.read(4))[0]

    while (end - f.tell()) > 0:
        commandSize = struct.unpack('H', f.read(2))[0]
        if commandSize == 0:
            raise Exception("Corrupted File!")

        command_enum = struct.unpack('B', f.read(1))[0]
        content = BytesIO(f.read(commandSize - 1))
        if command_enum == 1:
            payloadSize = struct.unpack("I", content.read(4))[0]
            tabId = struct.unpack("I", content.read(4))[0]
            index = struct.unpack("I", content.read(4))[0]
            url_length = struct.unpack("I", content.read(4))[0]
            url = content.read(url_length).decode('utf-8', 'ignore')
            tabs.add(url)

print('\n'.join(sorted(tabs)))