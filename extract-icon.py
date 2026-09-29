#!/usr/bin/env python3
"""Extract the existing 512px PNG from Cue's ICNS without image dependencies."""
import struct
import sys
from pathlib import Path


def extract_icon(data: bytes) -> bytes:
    if len(data) < 8 or data[:4] != b"icns":
        raise ValueError("Not an ICNS icon")
    if struct.unpack_from(">I", data, 4)[0] != len(data):
        raise ValueError("Invalid ICNS length")
    offset = 8
    while offset < len(data):
        if len(data) - offset < 8:
            raise ValueError("Truncated ICNS entry")
        kind, length = struct.unpack_from(">4sI", data, offset)
        if length < 8 or offset + length > len(data):
            raise ValueError("Invalid ICNS entry length")
        payload = data[offset + 8:offset + length]
        if kind == b"ic09" and payload.startswith(b"\x89PNG\r\n\x1a\n"):
            if len(payload) < 24 or struct.unpack_from(">II", payload, 16) != (512, 512):
                raise ValueError("Expected a 512px PNG")
            return payload
        offset += length
    raise ValueError("No 512px PNG in ICNS")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: extract-icon.py INPUT.icns OUTPUT.png")
    Path(sys.argv[2]).write_bytes(extract_icon(Path(sys.argv[1]).read_bytes()))
