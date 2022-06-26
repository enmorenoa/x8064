.data

msgPeticion:    .string "Introduzca un número\n"
msgError:	.string "El número tiene que ser mayor que 0\n"
formatNum:	.string "%d"
msgResultado:	.string "El factorial de %d es %d\n"
num:		.int 0
factorial:	.int 0

.text

        .global main

main:
	push %eax
	push %ebx
	push %ecx
	push %edx

	pushl $msgPeticion
	call printf
	add $4, %esp

	pushl $num
	pushl $formatNum
	call scanf
	add $8, %esp

	cmpl $0, num
	jg Continuar
	pushl $msgError
	call printf
	add $4, %esp
	jmp Fin

    Continuar:
	mov num, %ebx
	mov $1, %eax
    BFact:
	mul %ebx
	sub $1, %ebx
	cmp $1, %ebx
	jg BFact
	mov %eax, factorial

	pushl factorial
	pushl num
	pushl $msgResultado
	call printf
	add $12, %esp

    Fin:
	pop %edx
	pop %ecx
	pop %ebx
	pop %eax
	ret
	
