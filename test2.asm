.data 0x0000
	data0: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	data1: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	data2: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	data3: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

.text 0x0000
ReadTestCase:
	add 	$8, $25, $0 # 8=readtestcase number
	add 	$26, $8, $0
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, ReadTestCase
wait0:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait0
	
	srl 	$8, $8, 21
	addi 	$9, $0, 0
	beq 	$8, $9, Case0
	addi 	$9, $9, 1
	beq		$8, $9, Case1
	addi 	$9, $9, 1
	beq 	$8, $9, Case2
	addi 	$9, $9, 1
	beq 	$8, $9, Case3
	addi 	$9, $9, 1
	beq 	$8, $9, Case4
	addi 	$9, $9, 1
	beq 	$8, $9, Case5
	addi 	$9, $9, 1
	beq 	$8, $9, Case6
	addi 	$9, $9, 1
	beq 	$8, $9, Case7
	j 		ReadTestCase
	

Case0:
	addi 	$26, $0, 10
	add 	$28, $25, $0 #4=number
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Case0
wait1:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait1

	andi 	$28, $28, 0xff
	addi 	$27, $28, -1 #2=number-1
	
	add 	$5, $0, $0 # current id of data read in

Read01: # read data of the array
	add 	$16, $25, $0 # data read in
	addi 	$26, $5, 1
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Read01
wait2:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait2
	
	sll 	$6, $5, 2
	andi	$16, $16, 0xff
	sw 		$16, data0($6)
	
	addi 	$5, $5, 1
	beq 	$5, $28, ReadTestCase
	j 		Read01
	
	
Case1: 
	add $5, $0, $0
Loop10:
	sll $6, $5, 2
	lw $7, data0($6)
	sw $7, data1($6)
	addi $5, $5, 1
	bne $28, $5, Loop10
	
	add $5, $0, $0
	# bubble sort
Loop11: # 
	add $6, $0, $0
	Loop12: #
		sll $7, $6, 2
		lw $16, data1($7)
		addi $19, $6, 1
		sll $19, $19, 2
		lw $17, data1($19)
		sltu $18, $17, $16
		beq $18, $0, Swap1 # 
		sw $16, data1($19)	
		sw $17, data1($7)
	Swap1:
		addi $6, $6, 1
		bne $6, $27, Loop12
	addi $5, $5, 1 
	bne $5, $28, Loop11
	
	j ReadTestCase
	

Case2:  #
	add $5, $0, $0
Loop20:
	sll $6, $5, 2
	lw $7, data1($6)
	andi $16, $7, 128 # get the sign bit
	srl $16, $16, 7
	beq $16, $0, Store20 # if it's positive
	andi $7, $7, 127
	sub $7, $0, $7 # turn it to complementary code
	
Store20:
	sw $7, data2($6)
	addi $5, $5, 1
	bne $28, $5, Loop20
	j ReadTestCase
	
	
Case3: # 
	add $5, $0, $0
Loop30:
	sll $6, $5, 2
	lw $7, data2($6)
	sw $7, data3($6)
	addi $5, $5, 1
	bne $28, $5, Loop30
	
	add $5, $0, $0
	# bubble sort
Loop31: # 
	add $6, $0, $0
	Loop32: # 
		sll $7, $6, 2
		lw $16, data3($7)
		addi $19, $6, 1
		sll $19, $19, 2
		lw $17, data3($19)
		slt $18, $17, $16 # 
		beq $18, $0, Swap3 # 
		sw $16, data3($19)
		sw $17, data3($7)	
	Swap3:
		addi $6, $6, 1
		bne $6, $27, Loop32
	addi $5, $5, 1 
	bne $5, $28, Loop31
	
	j ReadTestCase


Case4:
	add 	$8, $25, $0
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Case4
wait3:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait3
	
	andi	$8, $8, 0xff
	addi	$9, $0, 3
	beq		$9, $8, Case43

	lw	 	$16, data1($0)
	addi 	$5, $28, -1
	sll 	$5, $5, 2
	lw 		$17, data1($5)
	j 		Out40
Case43:
	lw 		$16, data3($0)
	addi 	$5, $28, -1
	sll 	$5, $5, 2
	lw 		$17, data3($5)
Out40:
	sub 	$18, $17, $16
	sll 	$30, $25, 11
	srl		$30, $30, 31
	add 	$26, $0, $18
	beq 	$30, $0, Out40
wait4:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait4
	j 		ReadTestCase
	

Case5:
	add 	$8, $8, $0
Read50:
	add 	$8, $25, $0 # id of dataset
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Read50
wait5:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait5

Read51:
	add 	$9, $25, $0 # id of data
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Read51
wait6:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait6
	
	andi	$8, $8, 0xff
	andi	$9, $9, 0xff
	sll 	$9, $9, 2
	addi 	$16, $0, 3
	beq 	$8, $16, Case53
Case51:
	lw 		$16, data1($9)
	andi 	$16, $16, 0xff
	add 	$26, $16, $0
	sll 	$30, $25, 11
	srl		$30, $30, 31
	beq 	$30, $0, Case51
wait7:
	addi 	$26, $26, 0xf
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait7
	j 		ReadTestCase
	
Case53:
	lw 		$16, data3($9)
	andi 	$26, $16, 0xff
	sll 	$30, $25, 11

	srl		$30, $30, 31
	beq 	$30, $0, Case53
wait8:
	addi 	$26, $26, 0xf
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait8
	j 		ReadTestCase
	
Case6:	
	add 	$17, $25, $0 # 17=id of dataset
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Case6
wait9:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait9
	andi 	$17, $17, 0xff
Read62:
	add 	$18, $25, $0 # 18=id
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Read62
wait10:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait10
	andi	$18, $18, 0xff

	sll		$18,$18,2
	addi 	$19,$0,2
	beq 	$17,$19,Case62
	addi 	$19,$0,3
	beq 	$17,$19,Case63
Case61:	lw 	$20,data1($18)
	add		$21, $0, $0
	j 		Branch0
Case62:	lw 	$20, data2($18)
	j 		Out60
Case63:	lw 	$20, data3($18)
Out60:	add	$21, $20, $0  # $20=original data, $21=symbol bit
	srl		$21, $21,8
	beq		$21, $0,Branch0
	addi	$21, $0,1
	sub		$20, $0,$20
Branch0:sll	$21, $21, 8
	addi	$22, $0,126
Loop6:	addi	$22, $22,1
	srl		$20, $20,1
	bne		$20, $0, Loop6
	sll		$21, $21, 8
	or 		$22, $22, $21
Out61:
	add		$26, $22, $0
	sll 	$30, $25, 11
	srl		$30, $30, 31
	beq 	$30, $0, Out61
wait11:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait11
	j 		ReadTestCase
	
Case7:
	add 	$1, $25, $0 #1=id
	sll 	$30, $25, 11
	srl		$30, $30, 31
	beq		$30, $0, Case7
wait12:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait12

	andi	$1, $1, 0xff
	sll 	$1, $1, 2
	lw		$27, data0($1)
	add		$20, $27, $0
	andi  	$27, $27, 0xff
	 
	add	$21, $20,$0  # $20=original data, $21=symbol bit
	srl		$21, $21,8
	beq		$21, $0,Branch1
	addi	$21, $0,1
	sub		$20, $0,$20
Branch1:sll	$21, $21, 8
	addi	$22, $0,126
Loop70:	addi	$22, $22,1
	srl		$20, $20,1
	bne		$20, $0, Loop70
	sll		$21, $21, 8
	or 		$22, $22, $21 # float representation

Loop71:
	addi 	$3, $0, 1
	sll 	$3, $3, 25
	add		$28, $0, $0
Loop711:
	add 	$26, $27, $0
	addi	$28, $28, 1
	bne		$28, $3, Loop711
	add 	$28, $0, $0
Loop712:
	add 	$26, $22, $0
	addi 	$28, $28, 1
	bne		$28, $3, Loop712
	j 		Loop71
