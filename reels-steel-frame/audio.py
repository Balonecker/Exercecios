"""Gera a trilha (impactos sintetizados + base grave) a partir de hits.json."""
import json, sys, wave
import numpy as np
SR = 44100
info = json.load(open(sys.argv[1])); out = sys.argv[2]
dur = info["dur"]; n = int(SR * dur)
t = np.arange(n) / SR
mix = np.zeros(n)
rng = np.random.default_rng(3)

def add(start, sig):
    i = int(start * SR); j = min(n, i + len(sig))
    if i < n: mix[i:j] += sig[: j - i]

def clank(freqs, decay, amp, length=1.2):
    tt = np.arange(int(SR * length)) / SR
    s = sum(np.sin(2 * np.pi * f * tt) / (k + 1) for k, f in enumerate(freqs))
    return amp * s * np.exp(-tt * decay)

def thud(f0, decay, amp, noise=0.3, length=0.5):
    tt = np.arange(int(SR * length)) / SR
    s = np.sin(2 * np.pi * f0 * tt * (1 - 0.4 * tt)) + noise * rng.standard_normal(len(tt)) * np.exp(-tt * 40)
    return amp * s * np.exp(-tt * decay)

for k, (time, kind) in enumerate(info["hits"]):
    if kind == "steel":
        base = 820 + 60 * (k % 4)
        add(time, clank([base, base * 2.76, base * 5.4, base * 1.5], 7, 0.22))
    elif kind == "osb":
        add(time, thud(110, 14, 0.5, 0.6))
    elif kind == "tile":
        add(time, thud(190 + 15 * (k % 3), 26, 0.28, 0.9, 0.3))
    else:
        add(time, clank([660, 990, 1320], 4, 0.22, 2.0))

# "whoosh" das quedas
for time, _ in info["hits"]:
    L = int(SR * 0.6); w = rng.standard_normal(L) * np.hanning(L) * 0.035
    add(time - 0.65, np.convolve(w, np.ones(30) / 30, mode="same"))

# base: pad suave em acorde maior, com acorde final mais brilhante
pad = sum(np.sin(2 * np.pi * f * t) for f in (110, 138.6, 164.8, 220)) * 0.025
pad *= np.clip(t / 1.5, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
mix += pad
end = max(h[0] for h in info["hits"]) + 0.6
add(end, clank([523.3, 659.3, 784, 1046.5], 1.6, 0.12, 3.5))

mix /= max(1e-9, np.abs(mix).max()) / 0.85
data = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
