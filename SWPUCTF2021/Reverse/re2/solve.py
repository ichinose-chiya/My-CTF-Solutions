s = 'ylqq]aycqyp{'
ans = ''
for i in s:
    c = ord(i)
    c += 2
    if (c <= 96 or c >= 98) and (c <= 64 or c > 66):
        ans += chr(c)
    else:
        ans += chr(c -2 - 24)
print(ans)
