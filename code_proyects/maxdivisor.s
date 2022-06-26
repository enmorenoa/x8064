.data

msgPeticion:    .string "Introduzca un número\n"
msgError:	.string "El número tiene que ser mayor que 0\n"
formatNum:	.string "%d"
msgResultado:	.string "El máximo divisor de %d es %d\n"
num:		.int 0
maxdivisor:	.int 0

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
	mov %ebx, maxdivisor
    BMaxDivisor:
	cmpl $1, maxdivisor
	je ImpResultado
        sub $1, maxdivisor
	mov num, %eax
	mov $0, %edx
	divl maxdivisor
	cmp $0, %edx
	je ImpResultado
	jmp BMaxDivisor

    ImpResultado:
	pushl maxdivisor
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
	
