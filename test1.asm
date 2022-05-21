.data 			      		
	buf: .word 
.text 				
switch1:
	lw	$t1,0xC70($28) # $t1=mode
	srl	$t1,$t1,21
	beq	$t1,$zero,case000
	j switch2
	
case000:lw	$t2,0xC70($28) # $t2,a
	sll	$t2,$t2,16
	srl	$t2,$t2,16
	sw	$t2,0xC64($28) # 0xC64 store 8-bit
	add	$t3,$zero,16   # $t3 upnum
	add	$t4,$zero,0    # $t4 lownum
	
loop1:	sub	$t3,$t3,1
	add	$t5,$zero,1    # $t5 number1
	sllv	$t5,$t5,$t3
	and	$t6,$t2,$t5
	beq	$t3,$zero,is1001
	beq	$t6,$zero,loop1
loop2:	beq	$t3,$t4,is1001
	add	$t7,$t4,1
	beq	$t3,$t7,is1001
	add	$t5,$zero,1    # $t5 number1
	sllv	$t5,$t5,$t3
	and	$t5,$t2,$t5
	srlv	$t5,$t5,$t3
	sub	$t3,$t3,1
	add	$t6,$zero,1    # $t6 number2
	sllv	$t6,$t6,$t4
	and	$t6,$t2,$t6
	srlv	$t6,$t6,$t4
	add	$t4,$t4,1
	bne	$t6,$t5,not1001
	j loop2
	
is1001:	add	$t7,$zero,1
	sw	$t7,0xC60($28)
	j switch1
	
not1001:sw	$zero,0xC60($28)
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

case001:lw	$t3,0xC70($28) # control input 
	srl	$t3,$t3,16
	addi	$t4,$zero,1
	and	$t3,$t4,$t3	
	bne	$t3,1,switch1
wait1:	lw	$t3,0xC70($28)
	srl	$t3,$t3,16
	addi	$t4,$zero,1
	and	$t3,$t4,$t3	
	bne	$t3,0,wait1
wait2:	lw	$t3,0xC70($28)
	srl	$t3,$t3,16
	addi	$t4,$zero,1
	and	$t3,$t4,$t3	
	lw	$t1,0xC70($28)
	sll	$t2,$t2,16
	srl	$t2,$t2,16
	sw	$t1,0xC64($28)
	bne	$t3,1,wait2
wait3:	lw	$t3,0xC70($28)
	srl	$t3,$t3,16
	addi	$t4,$zero,1
	and	$t3,$t4,$t3	
	bne	$t3,0,wait3
wait4:	lw	$t3,0xC70($28)
	srl	$t3,$t3,16
	addi	$t4,$zero,1
	and	$t3,$t4,$t3	
	lw	$t2,0xC70($28)
	sll	$t2,$t2,16
	srl	$t2,$t2,16
	sw	$t1,0xC64($28)
	beq	$t3,1,wait4
	j	switch1

case010:and	$t3,$t1,$t2
	sw	$t3,0xC64($28)
	j 	switch1
	
case011:or	$t3,$t1,$t2
	sw	$t3,0xC64($28)
	j	switch1
	
case100:xor	$t3,$t1,$t2
	sw	$t3,0xC64($28)
	j	switch1
	
case101:sllv	$t3,$t1,$t2
	sw	$t3,0xC64($28)
	j	switch1
	
case110:srlv	$t3,$t1,$t2
	sw	$t3,0xC64($28)
	j	switch1
	
case111:sll	$t3,$t1,16
	sra	$t3,$t3,16
	srav	$t3,$t3,$t2
	sw	$t3,0xC64($28)
	j	switch1
