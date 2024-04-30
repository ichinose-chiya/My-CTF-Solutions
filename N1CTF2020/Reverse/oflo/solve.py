s = "5-\x11\x1AI}\x11\x14+;>=<_"
b = "Linux version "
ans = ""

for i in range(14):
    ans += chr(ord(s[i]) ^ (ord(b[i]) + 2))
print(ans)
