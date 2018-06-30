#!/usr/bin/env python3

import re 

result = open('result.txt', 'w')

dict_FOPB = {
	'0' : 'Filter outer pbit ',
	'8' : 'Do not filter on outer pbit',
	'14' : 'default filter when no other two-tag rule applies',
	'15' : 'not a double-tag rule'	
}

dict_FOVID = {
	'0' :  'Filter outer VID value ',
	'4096' : 'Do not filter on the outer VID'
}

dict_FIPB = {
    '0': 'Filter inner pbit ',  
	'8': 'Do not filter on inner pbit',
    '14': 'default filter when no other one-tag rule applies',
    '15': 'This entry is a no-tag rule'
}

dict_FIVID = {
	'0' :   'Filter inner VID value ',
	'4096' : 'Do not filter on the inner VID'
}

dict_FEType = {
	'00': 'do not filter on Ethertype',
	'01': 'filter IPoE frames',
	'02': 'filter PPPoE frames',
	'03': 'filter ARP frames'
}

dict_RTag = {
	'00':  '',
	'01': 'remove 1 tag',
	'02': 'remove 2 tags',
	'03': 'Discard the frame'
}


dict_TOPB = {
	'0': 'add an outer tag, insert this pbit in the outer vlan tag ',
	'8': 'add an outer tag, copy from the inner pbit',
	'9': 'add an outer tag, copy from the outer pbit',
	'10': 'add an outer tag, derive pbit from DSCP to pbit mapping',
	'15': 'do not add outer tag'
}

dict_TOVID ={
	'0': 'Use this value as outer VLAN tag ',
	'4096': 'copy the outer VID from inner VID',
	'4097': 'copy the outer VID from outer VID'
}

dict_TIPB = {
	'0': 'add an inner tag, insert this pbit in the inner vlan tag ',
	'8': 'add an inner tag, copy from the inner pbit',
	'9': 'add an inner tag, copy from the outer pbit',
	'10': 'add an inner tag, derive pbit from DSCP to pbit mapping',
	'15': 'do not add inner tag'	
}

dict_TIVID = {
	'0': 'Use this value as inner VLAN tag ',
	'4096': 'copy the inner VID from inner VID',
	'4097': 'copy the inner VID from outer VID'
}


rules_file = input("filter file:")
rules = open(rules_file, 'r')
rule_table = rules.readlines()
rules.close()

for line in rule_table:
	filters = (' '.join(line.split())).split(' ')
	print('rule %s:' % (filters[0][0:-1]))
	result.write('rule %s:\n' % (filters[0][0:-1]))
	print(filters[1:-3], '\n')
	
	#result.write(str(filters[1:-1]) + '\n')
	FOPB   = filters[1].replace('0', '', 1)
	#result.write(dict_FOPB['0' if int(FOPB) < 8 else FOPB] + FOPB if int(FOPB) < 8 else '' + '\n')
	
	#FOVID  = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filters[2])
	FOVID  = '0' if filters[2].lstrip('0')=='' else filters[2].lstrip('0')
	#result.write(dict_FOVID['0' if int(FOVID) < 4095 else FOVID] + FOVID if int(FOVID) < 4095 else '' + '\n')
	
	FIPB   = filters[4].replace('0', '', 1)
	result.write(dict_FIPB['0' if int(FIPB) < 8 else FIPB]       + FIPB if int(FIPB) < 8 else ' ' + '\n')
	
	#FIVID  = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filters[5])
	FIVID  = '0' if filters[5].lstrip('0')=='' else filters[5].lstrip('0')
	result.write(dict_FIVID['0' if int(FIVID) < 4095 else FIVID] + FIVID if int(FIVID) < 4095 else ' ' + '\n')
	
	FEType = filters[7]
	RTag   = filters[8]
	'''
	result.write(dict_FOPB['0' if int(FOPB) < 8 else FOPB] + FOPB if int(FOPB) < 8 else '' + '\n' + 
		         dict_FOVID['0' if int(FOVID) < 4095 else FOVID] + FOVID if int(FOVID) < 4095 else '' + '\n' +
				 dict_FIPB['0' if int(FIPB) < 8 else FIPB]       + FIPB if int(FIPB) < 8 else '' + '\n' +
				 dict_FIVID['0' if int(FIVID) < 4095 else FIVID] + FIVID if int(FIVID) < 4095 else '' + '\n')
	result.write('\n')
	'''
	
	print('filter')
	print(dict_FOPB['0' if int(FOPB) < 8 else FOPB], FOPB if int(FOPB) < 8 else '')
	print(dict_FOVID['0' if int(FOVID) < 4095 else FOVID], FOVID if int(FOVID) < 4095 else '')
	print(dict_FIPB['0' if int(FIPB) < 8 else FIPB], FIPB if int(FIPB) < 8 else '')
	print(dict_FIVID['0' if int(FIVID) < 4095 else FIVID], FIVID if int(FIVID) < 4095 else '')
	print(dict_FEType[FEType])
	print(dict_RTag[RTag])
	
	#result.write('\n')


rule_file = input("treatment file:")
rules = open(rule_file, 'r')
rule_table = rules.readlines()
rules.close()


for line in rule_table:
	treatments = (' '.join(line.split())).split(' ')
	print('rule %s:' % (treatments[0][0:-1]))
	print(treatments[1:-1], '\n')
	TOPB   = treatments[1].replace('0', '', 1)
	#FOVID  = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", treatments[2])
	TOVID  = '0' if treatments[2].lstrip('0')=='' else treatments[2].lstrip('0')
	TIPB   = treatments[4].replace('0', '', 1)
	
	#FIVID  = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", treatments[5])
	TIVID  = '0' if treatments[5].lstrip('0')=='' else treatments[5].lstrip('0')
	

	print('treatment')
	print(dict_TOPB['0' if int(TOPB) < 8 else TOPB], TOPB if int(TOPB) < 8 else '')
	print(dict_TOVID['0' if int(TOVID) < 4095 else TOVID], TOVID if int(TOVID) < 4095 else '')
	print(dict_TIPB['0' if int(TIPB) < 8 else TIPB], TIPB if int(TIPB) < 8 else '')
	print(dict_TIVID['0' if int(TIVID) < 4095 else TIVID], TIVID if int(TIVID) < 4095 else '')
	
	print('\n')