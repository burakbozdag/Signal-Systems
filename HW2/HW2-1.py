# Burak Bozdag
# 150170110

from scipy import signal

print("x = ")
x = [int(i) for i in input().split()] # Entering numbers with spaces
print("h = ")
h = [int(i) for i in input().split()] # Entering numbers with spaces
x = x[:5]
h = h[:5]
if len(x) > len(h):
    for i in range(0, (len(x) - len(h))):
        h.append(0)
elif len(x) < len(h):
    for i in range(0, (len(h) - len(x))):
        x.append(0)

print("y = ")
print(signal.convolve(x, h))
