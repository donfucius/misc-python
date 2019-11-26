import sys
import os
import zlib

size_cfg = 0x50

fname = sys.argv[1]
with open(fname, 'rb') as bin_file:
    buf = bin_file.read()
    pos_cfg_zipped_data = 0
    pos_cfg = 0
    while pos_cfg < len(buf):
        pos_cfg_zipped_data += size_cfg
        if buf[pos_cfg_zipped_data : pos_cfg_zipped_data + 2] != b'\x78\x9c':
            pos_cfg += 1
            pos_cfg_zipped_data = pos_cfg
            continue
        cfg = buf[pos_cfg : pos_cfg_zipped_data]
        size_unzip = int.from_bytes(cfg[0xC : 0xC + 4], sys.byteorder)
        if pos_cfg + size_unzip > len(buf):
            exit(-1)
        name = cfg[0x14 : 0x14 + 0x20].decode('windows-1252')
        size_all = size_unzip + int.from_bytes(cfg[0x38 : 0x38 + 4], sys.byteorder)
        if not os.path.exists(name):
            zfile = buf[pos_cfg_zipped_data : pos_cfg_zipped_data + size_unzip]
            head, tail = os.path.split(fname)
            with open(os.path.join(os.path.dirname(fname), '.'.join((tail, name))), 'wb') as fw:
                try:
                    fw.write(zlib.decompress(zfile))
                except:
                    pass
            pos_cfg += size_cfg + size_all
            pos_cfg_zipped_data = pos_cfg
