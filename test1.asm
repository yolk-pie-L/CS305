.data 0x0000
	buf: .word 0x0000
.text 0x0000
Read0:
	add 	$9, $25, $0 # $9=testcase
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Read0
	
waitRead0:
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	bne		$30, $0, waitRead0

	srl 	$9, $9, 21

Switch:
	add 	$8, $0, $0 # $8=compare test case
	beq		$9, $8, Case0
	addi	$8, $8, 1
	beq 	$9, $8, Case1
	addi	$8, $8, 1
	beq		$9, $8, Case2
	addi	$8, $8, 1
	beq 	$9, $8, Case3
	addi	$8, $8, 1
	beq		$9, $8, Case4
	addi 	$8, $8, 1
	beq 	$9, $8, Case5
	addi 	$8, $8, 1
	beq		$9, $8, Case6
	addi 	$8, $8, 1
	beq		$9, $8, Case7
	j 		Read0
	
Case0:
	add		$10, $25, $0 # a
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Case0

Wait0:
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	bne		$30, $0, Wait0
	
	andi	$10, $10, 0xffff
	addi 	$1, $0, 2
	beq 	$10, $1, not1001

	sll		$10, $10, 16
	srl		$10, $10, 16
	addi	$11, $0, 16   # $11 upnum
	add		$12, $0, $0    # $12 lownum
	
loop1:	addi	$11, $11,-1
	addi	$13, $0, 1    # $13 number1
	sllv	$13, $13, $11
	and		$14, $10, $13
	beq		$11, $0, is1001
	beq		$14, $0, loop1
loop2:	beq	$11, $12, is1001
	addi	$t7, $12, 1
	beq		$11, $t7, is1001
	addi	$13, $0, 1    # $13 number1
	sllv	$13, $13, $11
	and		$13, $10, $13
	srlv	$13, $13, $11
	addi	$11, $11, -1
	addi	$14, $0, 1    # $14 number2
	sllv	$14, $14, $12
	and	 	$14, $10, $14
	srlv	$14, $14, $12
	addi	$12, $12, 1
	bne		$14, $13, not1001
	j loop2

is1001:	addi	$t7, $0, 1 # t7, sign bit
	sll 	$t7, $t7, 23
	add		$26, $10, $t7 #the highest bit is sign bit
	sll		$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, is1001
wait1:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait1
	j 	Read0
	
not1001:
	add		$26, $10, $0
	sll		$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, not1001
wait2:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait2
	j 		Read0



Case1:
	add 	$11, $25, $0 # 11=a
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Case1
wait3:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait3
	
	andi	$11, $11, 0xffff
Outa:
	add		$26, $11, $0
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Outa
wait4:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait4
	
Inb:
	add 	$12, $25, $0 # 12=b
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Inb
wait5:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait5
	
	andi 	$12, $12, 0xffff
Outb:
	add		$26, $12, $0
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Outb
wait6:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait6
	j  		Read0


Case2:and	$26, $11, $12
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Case2
wait7:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait7
	j 	Read0
	
Case3:or	$26, $11, $12
	sll 	$30, $25, 11
	srl 	$30, $30, 31
	beq 	$30, $0, Case3
wait8:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait8
	j 	Read0
	
Case4:xor	$26, $11, $12
	sll 	$30, $25, 11
	srl		$30, $30, 31
	beq 	$30, $0, Case4
wait9:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait9
	j 	Read0
	
Case5:sllv	$26, $11, $12
	sll 	$30, $25, 11
	srl		$30, $30, 31
	beq 	$30, $0, Case5
wait10:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait10
	j 		Read0
	
Case6:srlv	$26,$11,$12
	sll 	$30, $25, 11
	srl		$30, $30, 31
	beq 	$30, $0, Case6

wait11:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait11
	j 		Read0
	

Case7:sll	$11, $11, 16
	sra		$11, $11, 16
	srav	$3, $11, $12
	andi $26, $3, 0xffff
	sll 	$30, $25, 11
	srl		$30, $30, 31
	beq 	$30, $0, Case7

wait12:
	sll 	$30, $25, 11
	srl		$30, $30, 31
	bne		$30, $0, wait12
	j 	Read0
