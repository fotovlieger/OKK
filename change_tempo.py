#!/usr/bin/env python3
"""Scale the tempo of a MIDI file. Usage: change_tempo.py in.mid out.mid FACTOR

FACTOR > 1 is faster, < 1 is slower. Tempo meta events are scaled, so any
tempo changes inside the file are preserved.
"""
import sys
from pathlib import Path


def read_varlen(b, i):
    v = 0
    while True:
        c = b[i]
        i += 1
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            return v, i


def write_varlen(v):
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.append(0x80 | (v & 0x7F))
        v >>= 7
    return bytes(reversed(out))


def parse_track(chunk):
    events, i, status = [], 0, None
    while i < len(chunk):
        delta, i = read_varlen(chunk, i)
        b = chunk[i]
        if b == 0xFF:
            mtype = chunk[i + 1]
            i += 2
            n, i = read_varlen(chunk, i)
            events.append((delta, "meta", mtype, chunk[i:i + n]))
            i += n
            status = None
        elif b in (0xF0, 0xF7):
            i += 1
            n, i = read_varlen(chunk, i)
            events.append((delta, "sysex", b, chunk[i:i + n]))
            i += n
            status = None
        else:
            if b & 0x80:
                status = b
                i += 1
            nd = 1 if (status >> 4) in (0xC, 0xD) else 2
            events.append((delta, "chan", status, chunk[i:i + nd]))
            i += nd
    return events


def build_track(events):
    out = bytearray()
    for delta, kind, a, body in events:
        out += write_varlen(delta)
        if kind == "meta":
            out += bytes([0xFF, a]) + write_varlen(len(body)) + body
        elif kind == "sysex":
            out += bytes([a]) + write_varlen(len(body)) + body
        else:
            out += bytes([a]) + body
    return bytes(out)


def change_tempo(data, factor):
    if factor <= 0:
        raise ValueError("factor must be positive")

    hlen = int.from_bytes(data[4:8], "big")
    header = data[:8 + hlen]
    pos = 8 + hlen
    tracks, found = [], False

    while pos < len(data):
        assert data[pos:pos + 4] == b"MTrk", "not a MIDI track chunk"
        length = int.from_bytes(data[pos + 4:pos + 8], "big")
        chunk = data[pos + 8:pos + 8 + length]
        pos += 8 + length
        events = []
        for delta, kind, a, body in parse_track(chunk):
            if kind == "meta" and a == 0x51 and len(body) == 3:
                found = True
                tempo = min(0xFFFFFF, max(1, round(int.from_bytes(body, "big") / factor)))
                body = tempo.to_bytes(3, "big")
            events.append((delta, kind, a, body))
        tracks.append(events)

    if not found:
        tempo = min(0xFFFFFF, round(500000 / factor))
        tracks[0].insert(0, (0, "meta", 0x51, tempo.to_bytes(3, "big")))

    out = bytearray(header)
    for events in tracks:
        track = build_track(events)
        out += b"MTrk" + len(track).to_bytes(4, "big") + track
    return bytes(out)


def selftest():
    track = (b"\x00\xff\x51\x03\x07\xa1\x20"          # tempo 500000 (120 BPM)
             b"\x00\x90\x3c\x64\x83\x60\x80\x3c\x00")  # note on/off
    smf = (b"MThd" + (6).to_bytes(4, "big") + (0).to_bytes(2, "big")
           + (1).to_bytes(2, "big") + (480).to_bytes(2, "big")
           + b"MTrk" + len(track).to_bytes(4, "big") + track)
    out = change_tempo(smf, 2.0)
    assert b"\x03\xd0\x90" in out and b"\x83\x60" in out

    no_tempo = b"\x00\x90\x3c\x64\x83\x60\x80\x3c\x00"
    smf = (b"MThd" + (6).to_bytes(4, "big") + (0).to_bytes(2, "big")
           + (1).to_bytes(2, "big") + (480).to_bytes(2, "big")
           + b"MTrk" + len(no_tempo).to_bytes(4, "big") + no_tempo)
    out = change_tempo(smf, 2.0)
    assert b"\xff\x51\x03\x03\xd0\x90" in out
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
    elif len(sys.argv) != 4:
        sys.exit(__doc__)
    else:
        src, dst, factor = sys.argv[1], sys.argv[2], float(sys.argv[3])
        Path(dst).write_bytes(change_tempo(Path(src).read_bytes(), factor))
        print(f"Wrote {dst} (tempo x{factor})")
