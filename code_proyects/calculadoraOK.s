.data

	msgOperacion:	.string "Introduzca la operación (+,-,*,s para salir)\n"
	oper:	.byte 0
	msgPeticion:    .string "Introduzca dos números\n"
	msgNum1:        .string "Primer número: "
	msgNum2:        .string "Segundo número: "
	formatNum:	.string "%d"
	msgResultado:  .string "El resultado de la operación es %d\n"
	num1: .int 0
	num2: .int 0
	msgNOperaciones: .string "El número de operaciones realizadas es %d\n"

.text

        .global main

leerOperandos:
	push %eax
	push %ecx
	push %edx

	pushl $msgPeticion
	call printf
	add $4, %esp

	pushl $msgNum1
	call printf
	add $4, %esp
	
	pushl $num1
	pushl $formatNum
	call scanf
	add $8, %esp

	pushl $msgNum2
	call printf
	add $4, %esp

	pushl $num2
	pushl $formatNum
	call scanf
	add $8, %esp

	pop %edx
	pop %ecx
	pop %eax
	ret

mostrarResultado:
	push %eax
	push %ecx
	push %edx

	pushl %eax
	pushl $msgResultado
	call printf
	add $8, %esp

	pop %edx
	pop %ecx
	pop %eax
	ret

main:

	push %eax
	push %ecx

	mov $0, %ecx

    iniMain:
	push %ecx
	pushl $msgOperacion
	call printf
	add $4, %esp
	pop %ecx

    pedirOtraOper:
	push %ecx
	call getchar
	pop %ecx
	mov %al, oper

	cmpb $'s', oper
	je finMain

	cmpb $'+', oper
	je operacionValida

	cmpb $'-', oper
	je operacionValida

	cmpb $'*', oper
	jne pedirOtraOper

    operacionValida:

	inc %ecx

	call leerOperandos

	cmpb $'+', oper
	jne operResta

	mov num1, %eax
	add num2, %eax
	jmp finOperacion

    operResta:
	cmpb $'-', oper
	jne operMultip

	mov num1, %eax
	sub num2, %eax
	jmp finOperacion

    operMultip:
	mov num1, %eax
	imul num2, %eax

    finOperacion:
	call mostrarResultado

	jmp iniMain

    finMain:

	push %ecx
	pushl $msgNOperaciones
	call printf
	add $8, %esp

	pop %ecx
	pop %eax
	ret
