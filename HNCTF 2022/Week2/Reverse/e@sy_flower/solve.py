s = 'c~scvdzKCEoDEZ[^roDICUMC'
ans = []

for i in s:
    ans.append(chr(ord(i) ^ 0x30))

for i in range(len(ans) // 2):
    tmp = ans[2 * i + 1]
    ans[2 * i + 1] = ans[2 * i]
    ans[2 * i] = tmp

print(''.join(ans))
