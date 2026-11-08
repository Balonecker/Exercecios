"""Trilha da queda: rangido/tremor, assobio da queda e impacto pesado."""
import json, sys, wave
import numpy as np
SR = 44100
info = json.load(open(sys.argv[1])); out = sys.argv[2]
dur, land = info["dur"], info["land"]
shake, drop = 1.2, 2.05
n = int(SR * dur); t = np.arange(n) / SR
rng = np.random.default_rng(7)
def lowpass(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
mix = np.zeros(n)
# tremor: ruído grave crescente + rangido metálico
m = (t >= shake) & (t < drop + 0.1)
env = np.clip((t - shake) / (drop - shake), 0, 1) ** 2 * m
mix += lowpass(rng.standard_normal(n), 120) * env * 3.0
mix += np.sin(2 * np.pi * (180 + 40 * np.sin(2 * np.pi * 3 * t)) * t) * env * 0.05
# assobio da queda (ruído filtrado subindo)
m = (t >= drop) & (t < land)
u = np.clip((t - drop) / (land - drop), 0, 1)
mix += lowpass(rng.standard_normal(n), 12) * (u ** 1.5) * m * 0.35
# impacto: grave forte + estalo + detritos
i = int(land * SR); L = n - i; tt = np.arange(L) / SR
boom = np.sin(2 * np.pi * 48 * tt * (1 - 0.25 * tt)) * np.exp(-tt * 4.5) * 1.0
boom += np.sin(2 * np.pi * 95 * tt) * np.exp(-tt * 9) * 0.5
crack = rng.standard_normal(L) * np.exp(-tt * 28) * 0.6
rumble = lowpass(rng.standard_normal(L), 60) * np.exp(-tt * 2.2) * 2.2
mix[i:] += boom + crack + rumble
for k in range(22):
    s = i + int(rng.uniform(0.05, 0.9) * SR); d = int(0.03 * SR)
    if s + d < n: mix[s:s + d] += rng.standard_normal(d) * np.exp(-np.arange(d) / (0.006 * SR)) * rng.uniform(.05, .18)
mix /= np.abs(mix).max() / 0.9
data = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
