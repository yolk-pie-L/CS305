#25��, $t9�Ĵ���������������ݣ�$k0�Ĵ�����Ϊ���,$fp��Ϊȷ��
.data
	data0: .space 40
	data1: .space 40
	data2: .space 40
	data3: .space 40

.text
	
	addi $t1, $zero, 0
	
	# �����������
ReadTestCase:
	add 	$t0, $t9, $zero # $t0=�����������
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, ReadTestCase
wait0:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait0
	
	# �ж����ĸ���������
	beq $t0, $t1, Case0
	addi $t1, $t1, 1
	beq $t0, $t1, Case1
	addi $t1, $t1, 1
	beq $t0, $t1, Case2
	addi $t1, $t1, 1
	beq $t0, $t1, Case3
	addi $t1, $t1, 1
	beq $t0, $t1, Case4
	addi $t1, $t1, 1
	beq $t0, $t1, Case5
	addi $t1, $t1, 1
	beq $t0, $t1, Case6
	addi $t1, $t1, 1
	beq $t0, $t1, Case7
	j ReadTestCase
	

# ��������0	
Case0: #�����м�������
	add 	$a0, $t9, $zero # $a0=���ݸ���
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, Case0
wait1:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait1
	subi 	$v0, $a0, 1
	
	add $a1, $zero, $zero # ��ǰ��¼�˼���
Loop0:
Read01: # ���������е�����
	add $s0, $t9, $zero # $s0=�洢������
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq $fp, $zero, Read01
wait2:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait2
	
	sll $a2, $a1, 2
	sw $s0, data0($a2)
	
	addi $a1, $a1, 1
	bne $a1, $a0, Loop0
	j ReadTestCase
	
	
Case1: # ��������1
	add $a1, $zero, $zero
Loop10:
	sll $a2, $a1, 2
	lw $a3, data0($a2)
	sw $a3, data1($a2)
	addi $a1, $a1, 1
	bne $a0, $a1, Loop10
	
	add $a1, $zero, $zero
	# bubble sort
Loop11: # $a1�������ѭ����$a2�����ڲ�ѭ��
	add $a2, $zero, $zero
	Loop12: # $a3��ŵ�һ�����ݵĵ�ַ��$s3��ŵڶ������ݵĵ�ַ
		sll $a3, $a2, 2
		lw $s0, data1($a3)
		addi $s3, $a2, 1
		sll $s3, $s3, 2
		lw $s1, data1($s3)
		sltu $s2, $s1, $s0
		beq $s2, $zero, Swap1 # ���$s0С��$s1�������ѭ�������򽻻�
		sw $s0, data1($s3)	
		sw $s1, data1($a3)
	Swap1:
		addi $a2, $a2, 1
		bne $a2, $v0, Loop12
	addi $a1, $a1, 1 
	bne $a1, $a0, Loop11
	
	j ReadTestCase
	

Case2:  # ��������2
	add $a1, $zero, $zero
Loop20:
	sll $a2, $a1, 2
	lw $a3, data1($a2)
	andi $s0, $a3, 256
	srl $s0, $s0, 7
	beq $s0, $zero, Store20
	andi $a3, $a3, 255
	sub $a3, $zero, $a3
	
Store20:
	sw $a3, data2($a2)
	addi $a1, $a1, 1
	bne $a0, $a1, Loop10
	j ReadTestCase
	
	
Case3: # ��������3
	add $a1, $zero, $zero
Loop30:
	sll $a2, $a1, 2
	lw $a3, data2($a2)
	sw $a3, data3($a2)
	addi $a1, $a1, 1
	bne $a0, $a1, Loop10
	
	add $a1, $zero, $zero
	# bubble sort
Loop31: # $a1�������ѭ����$a2�����ڲ�ѭ��
	add $a2, $zero, $zero
	Loop32: # $a3��ŵ�һ�����ݵĵ�ַ��$s3��ŵڶ������ݵĵ�ַ
		sll $a3, $a2, 2
		lw $s0, data1($a3)
		addi $s3, $a2, 1
		sll $s3, $s3, 2
		lw $s1, data1($s3)
		slt $s2, $s1, $s0 # ���s1��s0С��s2��Ϊ1����ת������ѭ��
		beq $s2, $zero, Swap3 # ���$s0С��$s1�������ѭ�������򽻻�
		sw $s0, data1($s3)
		sw $s1, data1($a3)	
	Swap3:
		addi $a2, $a2, 1
		bne $a2, $v0, Loop12
	addi $a1, $a1, 1 
	bne $a1, $a0, Loop11
	
	j ReadTestCase


Case4:
	add 	$t0, $t9, $zero
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, Case4
wait3:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait3
	
	addi $t1, $zero, 3
	beq $t1, $t0, Case43
	# ���ݼ�1
	lw $s0, data1
	sub $a1, $a0, 1
	sll $a1, $a1, 2
	lw $s1, data1($a1)
	j Out40
Case43:
	lw $s0, data3
	sub $a1, $a0, 1
	sll $a1, $a1, 2
	lw $s1, data3($a1)
Out40:
	sub $s2, $s1, $s0
	add $k0, $zero, $s2
	beq $fp, $zero, Out40
wait4:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait4
	j ReadTestCase
	

Case5:
Read50:
	add $t0, $t9, $zero # �ĸ����ݼ�
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq $fp, $zero, Read50
wait5:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait5
Read51:
	add $t1, $t9, $zero # �ڼ���Ԫ��
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq $fp, $zero, Read51
wait6:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait6
	
	addi $s0, $zero, 3
	beq $t0, $s0, Case53
Case51:
	lw $s0, data1($t1)
	add $k0, $s0, $zero
	beq $fp, $zero, Case51
wait7:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait7
	j ReadTestCase
	
Case53:
	lw $s0, data3($t1)
	add $k0, $s0, $zero
	beq $fp, $zero, Case53
wait8:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait8
	j ReadTestCase
	
	
Case6:	
	add 	$s1, $t9, $zero # ���ݼ�
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, Case6
wait9:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait9
Read62:
	add 	$s2, $t9, $zero # s2=index
	sll 	$fp, $t9, 3
	srl 	$fp, $fp, 23
	beq 	$fp, $zero, Read62
wait10:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait10
	
	sll	$s2,$s2,2
	addi 	$s3,$zero,2
	beq 	$s1,$s3,Case62
	addi 	$s3,$zero,3
	beq 	$s1,$s3,Case63
Case61:	lw 	$s4,data1($s2)
	add	$s5, $zero, $zero
	j 	Branch0
Case62:	lw 	$s4,data2($s2)
	j 	Out60
Case63:	lw 	$s4,data3($s2)
Out60:	add	$s5,$s4,$zero  # $s4=original data, $s5=symbol bit
	srl	$s5,$s5,7
	beq	$s5,$zero,Branch0
	addi	$s5,$zero,1
	sub	$s4,$zero,$s4
Branch0:sll	$s5, $s5, 8
	addi	$s6,$zero,126
Loop6:	addi	$s6,$s6,1
	srl	$s4,$s4,1
	bne	$s4,$zero,Loop6
	# ������λ��ָ��λ����һ��register���棬Ϊ��λ8~0��8Ϊ����λ
	or 	$s6, $s6, $s5
Out61:
	add	$k0, $s6, $zero
	beq 	$fp, $zero, Out61
wait11:
	sll 	$fp, $t9, 3
	srl	$fp, $fp, 23
	bne	$fp, $zero, wait11
	j 	ReadTestCase
	
Case7:
	

