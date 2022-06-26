.globl main

main:
    push %rbp
    mov $1,%rax
    mov $1,%rdi
    leaq hello(%rip),%rsi
    mov $15,%rdx
    syscall
    mov $60,%rax
    mov $0,%rdi
    pop %rbp
    ret 

.data

hello:	.string "Hello World\n"