.text 				
switch1:
	add 	$t1, $t9, $zero
	sll 	$fp, $t1, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, switch1
wait0:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait0
	beq	$t1, $zero,case000
	j switch2
	
case000: #先找到最高为1的位数,然后开始从两边往中间找,找的时候用and只留下要判断的那位,然后看等不等就行
	add 	$t2, $t9, $zero # t2, a
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, case000
wait:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait

	sll	$t2,$t2,16
	srl	$t2,$t2,16
	addi	$t3,$zero,16   # $t3 upnum
	add	$t4,$zero,$zero    # $t4 lownum
	
loop1:	subi	$t3,$t3,1
	addi	$t5,$zero,1    # $t5 number1
	sllv	$t5,$t5,$t3
	and	$t6,$t2,$t5
	beq	$t3,$zero,is1001
	beq	$t6,$zero,loop1
loop2:	beq	$t3,$t4,is1001
	addi	$t7,$t4,1
	beq	$t3,$t7,is1001
	addi	$t5,$zero,1    # $t5 number1
	sllv	$t5,$t5,$t3
	and	$t5,$t2,$t5
	srlv	$t5,$t5,$t3
	subi	$t3,$t3,1
	addi	$t6,$zero,1    # $t6 number2
	sllv	$t6,$t6,$t4
	and	$t6,$t2,$t6
	srlv	$t6,$t6,$t4
	addi	$t4,$t4,1
	bne	$t6,$t5,not1001
	j loop2
	
is1001:	addi	$t7, $zero, 1 # t7, sign bit
	sll 	$t7, $t7, 31
	add	$k0, $t2, $t7 #最高位作为sign bit
	sll	$fp, $t9, 3
	srl 	$fp, $fp, 21
	beq 	$fp, $zero, is1001
wait1:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait1
	j switch1
	
not1001:
	add	$k0, $t2, $zero
	sll	$fp, $t9, 3
	srl 	$fp, $fp, 21
	beq 	$fp, $zero, not1001
wait2:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait2
	j switch1
	
switch2:addi	$a0,$zero,1
	beq	$t1,$a0,case001
	addi	$a0,$a0,1
	beq	$t1,$a0,case010
	addi	$a0,$a0,1
	beq	$t1,$a0,case011
	addi	$a0,$a0,1
	beq	$t1,$a0,case100
	addi	$a0,$a0,1
	beq	$t1,$a0,case101
	addi	$a0,$a0,1
	beq	$t1,$a0,case110
	addi	$a0,$a0,1
	beq	$t1,$a0,case111
	j	switch1

case001:
	add 	$t1, $t9, $zero # t1 a
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, case001
wait3:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait3
	
Outa:
	add	$k0, $t1, $zero
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, Outa
wait4:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait4
	
Inb:
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	add 	$t2, $t9, $zero # t2 b
	beq 	$fp, $zero, Inb
wait5:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait5
Outb:
	add	$k0, $t2, $zero
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, Outb
wait6:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait6
	j  	switch1


case010:and	$t3, $t1, $t2
	add 	$k0, $t3, $zero
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, case010
wait7:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait7
	j 	switch1
	
case011:or	$t3, $t1, $t2
	add 	$k0, $t3, $zero
	beq 	$fp, $zero, case011
wait8:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait8
	j 	switch1
	
case100:xor	$t3,$t1,$t2
	add 	$k0, $t3, $zero
	beq 	$fp, $zero, case100
wait9:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait9
	j 	switch1
	
case101:sllv	$t3,$t1,$t2
	add 	$k0, $t3, $zero
	beq 	$fp, $zero, case101
wait10:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait10
	j 	switch1
	
case110:srlv	$t3,$t1,$t2
	add 	$k0, $t3, $zero
	beq 	$fp, $zero, case110
wait11:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait11
	j 	switch1
	
case111:sll	$t3,$t1,16
	sra	$t3,$t3,16
	srav	$t3,$t3,$t2
	add 	$k0, $t3, $zero
	beq 	$fp, $zero, case111
wait12:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait12
	j 	switch1
