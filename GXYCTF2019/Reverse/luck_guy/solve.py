import binascii

f1 = 'GXY{do_not_'
f2 = [i for i in (binascii.unhexlify('7F666F6067756369')[::-1])]

while True:
    again = False
    for i in f2:
        if i < 32 or i >126:
            again = True
            break

    if not again:
        break

    for i in range(8):
        if i %2 == 1:
            f2[i] -= 2
        else:
            f2[i] -= 1

print(f1 + ''.join([chr(i) for i in f2]))
