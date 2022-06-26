.globl main

main:
    push %rbp
    #num1
    mov $1,%rax
    mov $1,%rdi
    leaq msg1(%rip),%rsi
    mov $33,%rdx
    syscall
    mov $60,%rax
    mov $0,%rdi
    mov  $0, %eax       # clear AL (zero FP args in XMM registers)
    leaq f1(%rip), %rdi  # load format string
    leaq x1(%rip), %rsi  # set storage to address of x
    call scanf

    pop %rbp
    ret 

.data

msg1:	.string "Introduzca un numero por teclado\n"
f1:  .string "%d"         # could be in .rodata instead
x1:  .long 0
