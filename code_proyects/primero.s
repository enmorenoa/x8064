.data

msg:    .ascii "Hola mundo!\n"

.text

        .global main

main:
	push %eax
	push %ebx
	push %ecx
	push %edx

	mov $4, %eax	
	mov $1, %ebx
	mov $msg, %ecx 
	mov $12, %edx
	int $0x80

	pop %edx
	pop %ecx
	pop %ebx
	pop %eax
	ret
	
