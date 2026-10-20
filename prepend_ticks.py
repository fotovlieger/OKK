#!/usr/bin/env python3
"""Prepend a 6-click count-in to a Standard MIDI File.

Two long ticks two beats apart, then four short ticks one beat apart, on GM
percussion (channel 10): side stick for all ticks. All ticks are quarter
notes at the same volume.

Usage:
    python3 prepend_ticks.py INPUT.mid [OUTPUT.mid]

Default output is INPUT-ticks.mid. Standard library only.
"""

import struct
import sys
from pathlib import Path

# Count-in definition. Change these if you want another feel.
N_LONG, N_SHORT = 2, 4
LONG_GAP, SHORT_GAP = 2, 1       # beats between ticks
CHANNEL = 9                      # 0-based: MIDI channel 10, GM percussion
LONG_NOTE, SHORT_NOTE = 37, 37   # side stick
LONG_VEL, SHORT_VEL = 60,60


def read_vlq(data, pos):
    value = 0
    while True:
        if pos >= len(data):
            raise ValueError("truncated variable-length quantity")
        b = data[pos]
        pos += 1
        value = (value << 7) | (b & 0x7F)
        if not b & 0x80:
            return value, pos


def encode_vlq(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(out))


def parse_track(chunk):
    pos = tick = 0
    running = None
    events = []
    while pos < len(chunk):
        delta, pos = read_vlq(chunk, pos)
        tick += delta
        if pos >= len(chunk):
            raise ValueError("truncated event")
        b = chunk[pos]
        if b == 0xFF:                       # meta
            mtype = chunk[pos + 1]
            length, p = read_vlq(chunk, pos + 2)
            end = p + length
            if end > len(chunk):
                raise ValueError("truncated meta event")
            events.append((tick, len(events), chunk[pos:end]))
            pos = end
        elif b in (0xF0, 0xF7):             # sysex
            length, p = read_vlq(chunk, pos + 1)
            end = p + length
            if end > len(chunk):
                raise ValueError("truncated sysex event")
            events.append((tick, len(events), chunk[pos:end]))
            pos = end
        else:
            if b & 0x80:                    # explicit status byte
                status = b
                running = status
                pos += 1
            else:                           # running status
                if running is None:
                    raise ValueError("running status without status byte")
                status = running
            high = status & 0xF0
            n_data = 1 if high in (0xC0, 0xD0) else 2
            end = pos + n_data
            if end > len(chunk):
                raise ValueError("truncated channel event")
            events.append((tick, len(events), bytes([status]) + chunk[pos:end]))
            pos = end
    return events


def parse_smf(path):
    data = Path(path).read_bytes()
    if data[:4] != b"MThd":
        raise ValueError(f"{path}: not a Standard MIDI File")
    header_len = int.from_bytes(data[4:8], "big")
    fmt, ntrks, division = struct.unpack(">HHH", data[8:14])
    extra = data[14:8 + header_len]
    if division & 0x8000:
        raise ValueError(f"{path}: SMPTE timing is not supported")
    pos = 8 + header_len
    tracks = []
    for _ in range(ntrks):
        if data[pos:pos + 4] != b"MTrk":
            raise ValueError(f"{path}: missing track chunk")
        track_len = int.from_bytes(data[pos + 4:pos + 8], "big")
        chunk = data[pos + 8:pos + 8 + track_len]
        tracks.append(parse_track(chunk))
        pos += 8 + track_len
    return fmt, division, extra, tracks


def note(status, pitch, velocity):
    return bytes([status, pitch, velocity])


def build_output(fmt, division, extra, tracks):
    beat = division
    long_gap = LONG_GAP * beat
    short_gap = SHORT_GAP * beat
    shift = N_LONG * long_gap + N_SHORT * short_gap

    # Keep the piece's initial tempo for the count-in. The original tempo
    # event also moves with the music, so no other tempo change is needed.
    tempo = None
    for track in tracks:
        for tick, _, ev in track:
            if len(ev) == 6 and ev[0:2] == b"\xFF\x51":
                if tempo is None or tick < tempo[0]:
                    tempo = (tick, ev)

    click_dur = beat                # quarter note
    clicks = []
    seq = 0
    if tempo:
        clicks.append((0, seq, tempo[1]))
        seq += 1
    for i in range(N_LONG):
        t = i * long_gap
        clicks.append((t, seq, note(0x90 | CHANNEL, LONG_NOTE, LONG_VEL)))
        clicks.append((t + click_dur, seq + 1, note(0x80 | CHANNEL, LONG_NOTE, 0)))
        seq += 2
    short_start = N_LONG * long_gap
    for i in range(N_SHORT):
        t = short_start + i * short_gap
        clicks.append((t, seq, note(0x90 | CHANNEL, SHORT_NOTE, SHORT_VEL)))
        clicks.append((t + click_dur, seq + 1, note(0x80 | CHANNEL, SHORT_NOTE, 0)))
        seq += 2

    out_tracks = []
    added = len(clicks)
    for index, track in enumerate(tracks):
        shifted = [(tick + shift, 100000 + order, ev)
                   for tick, order, ev in track]
        if index == 0:
            shifted += clicks
        if not any(ev[0:2] == b"\xFF\x2F" for _, _, ev in shifted):
            end = max((t for t, _, _ in shifted), default=0)
            shifted.append((end, 999999, b"\xFF\x2F\x00"))
            added += 1
        shifted.sort(key=lambda item: (item[0], item[1]))
        out_tracks.append(shifted)
    return out_tracks, shift, tempo, added


def encode_track(events):
    out = bytearray()
    last_tick = 0
    for tick, _, ev in events:
        out += encode_vlq(tick - last_tick)
        out += ev
        last_tick = tick
    return bytes(out)


def write_smf(path, fmt, division, extra, tracks):
    out = bytearray(b"MThd")
    out += (6 + len(extra)).to_bytes(4, "big")
    out += struct.pack(">HHH", fmt, len(tracks), division)
    out += extra
    for track in tracks:
        chunk = encode_track(track)
        out += b"MTrk" + len(chunk).to_bytes(4, "big") + chunk
    Path(path).write_bytes(out)


def verify(path, division, original_count, added_count, expected_ons):
    fmt, div, _, tracks = parse_smf(path)
    if div != division:
        raise AssertionError("division changed")
    total = sum(len(t) for t in tracks)
    if total != original_count + added_count:
        raise AssertionError("event count changed")
    for track in tracks:
        if track[-1][2][0:2] != b"\xFF\x2F":
            raise AssertionError("track does not end with End of Track")
    count_in = (N_LONG * LONG_GAP + N_SHORT * SHORT_GAP) * division
    found = [(tick, ev[1]) for tick, _, ev in tracks[0]
             if tick < count_in and ev[0] == (0x90 | CHANNEL) and ev[2] > 0
             and ev[1] in (LONG_NOTE, SHORT_NOTE)]
    if sorted(found) != sorted(expected_ons):
        raise AssertionError(f"count-in notes wrong: {found}")


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__.strip())
        return 2
    src = Path(argv[1])
    dst = Path(argv[2]) if len(argv) == 3 else src.with_name(src.stem + "-ticks.mid")

    fmt, division, extra, tracks = parse_smf(src)
    out_tracks, shift, tempo, added = build_output(fmt, division, extra, tracks)
    write_smf(dst, fmt, division, extra, out_tracks)

    beat = division
    expected = []
    for i in range(N_LONG):
        expected.append((i * LONG_GAP * beat, LONG_NOTE))
    short_start = N_LONG * LONG_GAP * beat
    for i in range(N_SHORT):
        expected.append((short_start + i * SHORT_GAP * beat, SHORT_NOTE))
    verify(dst, division, sum(len(t) for t in tracks), added, expected)

    tempo_us = 500000
    if tempo:
        tempo_us = int.from_bytes(tempo[1][3:6], "big")
    seconds = shift * tempo_us / 1e6 / beat
    print(f"{src} -> {dst}")
    print(f"format {fmt}, {division} ticks/beat, "
          f"{60000000 / tempo_us:.1f} BPM")
    print(f"count-in: {N_LONG} long + {N_SHORT} short ticks, "
          f"{shift} ticks ({seconds:.2f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
