.data

	msgPeticion:    .string "Introduzca 10 números\n"
	formatNum:	.string "%d"
	formatElem:	.string "%d\n"
	vectorS:	.space 40
	vectorD:	.space 40
	nD:		.int 0
	msgResultado:	.string "El vector resultante es:\n"

.text

        .global main



LeerVector:		# %ebx = dirección de comienzo del vector	%ecx = número de elementos del vector
	push %eax
	push %ecx
	push %edx
	push %esi

	mov $0, %esi
  BLeer:
	push %ecx
	leal (%ebx, %esi, 4), %eax
	pushl %eax
	pushl $formatNum
	call scanf
	add $8, %esp
	inc %esi
	pop %ecx
	loop BLeer

	pop %esi
	pop %edx
	pop %ecx
	pop %eax
	ret



ImprimirVector:		# %ebx = dirección de comienzo del vector     %ecx = número de elementos del vector
	push %eax
	push %ecx
	push %edx
	push %esi

	mov $0, %esi
  BImprimir:
	push %ecx
	pushl (%ebx, %esi, 4)
	pushl $formatElem
	call printf
	add $8, %esp
	inc %esi
	pop %ecx
	loop BImprimir

	pop %esi
	pop %edx
	pop %ecx
	pop %eax
	ret



main:
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi

	pushl $msgPeticion
	call printf
	add $4, %esp

	mov $10, %ecx
	leal vectorS, %ebx
	call LeerVector

	
	mov $0, %ebx
	mov $0, %esi
	mov $2, %ecx
    CopiaPares:
	mov vectorS(,%ebx,4), %eax
	cltd
	idivl %ecx
	cmp $0, %edx
	jne SigCopiaPares
	mov vectorS(,%ebx,4), %eax
	mov %eax, vectorD(,%esi, 4)
	inc %esi
    SigCopiaPares:
	inc %ebx
	cmp $10, %ebx
	jl CopiaPares
	mov %esi, nD

	pushl $msgResultado
	call printf
	add $4, %esp

	mov nD, %ecx
	leal vectorD, %ebx
	call ImprimirVector

	pop %esi	
	pop %edx
	pop %ecx
	pop %ebx
	pop %eax
	ret
	
