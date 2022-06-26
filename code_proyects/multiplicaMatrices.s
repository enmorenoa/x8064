.data

	msgPeticion1:   .string "Introduzca los elementos de la primera matriz\n"
	msgPeticion2:   .string "Introduzca los elementos de la segunda matriz\n"
	msgFila:	.string "Fila %d:\n"
	formatNum:	.string "%d"
	formatElem:	.string "%d  "
	saltoLinea:	.string "\n"
	m1:		.space 36
	m2:		.space 36
	mResult:	.space 36
	f:		.int 0
	c:		.int 0
	msgResultado:	.string "La matriz resultante es:\n"


.text

        .global main



LeerMatriz:			# %ebx = dirección de comienzo de la matriz	
				# %ecx = número de filas y columnas de la matriz
	push %eax
	push %ecx
	push %edx
	push %esi
	push %edi


	mov $0, %esi
	mov $0, %edi
  BLeerFilas:
	push %ecx


	push %ecx
	push %edi
	pushl $msgFila
	call printf
	add $8, %esp
	pop %ecx	

    BLeerColumnas:
	    push %ecx
	    leal (%ebx, %esi, 4), %eax
	    pushl %eax
	    pushl $formatNum
	    call scanf
	    add $8, %esp
	    pop %ecx
	    inc %esi
	    loop BLeerColumnas
	inc %edi
	pop %ecx
	cmp %ecx, %edi
	jl BLeerFilas

	pop %edi
	pop %esi
	pop %edx
	pop %ecx
	pop %eax
	ret



ImprimirMatriz:			# %ebx = dirección de comienzo de la matriz
				# %ecx = número de filas y columnas de la matriz
	push %eax
	push %ecx
	push %edx
	push %esi
	push %edi

	mov $0, %esi
	mov $0, %edi
  BImprimirFilas:
	push %ecx

	push %ecx
	push %edi
	pushl $msgFila
	call printf
	add $8, %esp
	pop %ecx

    BImprimirColumnas:
	    push %ecx
	    pushl (%ebx, %esi, 4)
	    pushl $formatElem
	    call printf
	    add $8, %esp
	    pop %ecx
	    inc %esi
	    loop BImprimirColumnas

	pushl $saltoLinea
	call printf
	add $4, %esp

	inc %edi
	pop %ecx
	cmp %ecx, %edi
	jl BImprimirFilas

	pop %edi
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

	pushl $msgPeticion1
	call printf
	add $4, %esp

	mov $3, %ecx
	leal m1, %ebx
	call LeerMatriz

	pushl $msgPeticion2
	call printf
	add $4, %esp

	mov $3, %ecx
	leal m2, %ebx
	call LeerMatriz

	mov $0, %ebx
	movl $0, f
  BMultiplicaFilas:
	movl $0, c
    BMultiplicaColumnas:
	    movl $0, mResult(, %ebx, 4)
	    mov f, %esi
	    imul $3, %esi
	    mov c, %edi
	    mov $3, %ecx
	 BCalculaElemento:
		mov m1(, %esi, 4), %eax
		imul m2(, %edi, 4), %eax
		add %eax, mResult(, %ebx, 4)
		inc %esi
		add $3, %edi
		loop BCalculaElemento
	    incl %ebx
	    incl c
	    cmp $3, c
	    jl BMultiplicaColumnas
	incl f
	cmp $3, f
	jl BMultiplicaFilas


	pushl $msgResultado
	call printf
	add $4, %esp

	mov $3, %ecx
	leal mResult, %ebx
	call ImprimirMatriz



	pop %esi
	pop %edx
	pop %ecx
	pop %ebx
	pop %eax
	ret
	
