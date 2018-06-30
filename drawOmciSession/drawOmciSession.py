#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: andy wu
date:	20180125

depends libs: pydot, graphviz
	(1) firstly, install graphviz from http://www.graphviz.org/download/
	(2) add graphviz install path to EVN PATH
	(3) install pydot
example:
	https://www.programcreek.com/python/example/5579/pydot.Dot
	http://jseabold.net/blog/2012/02/12/making-graphical-models-with-pydot/
"""
import os, re, time
import pydot


MS = []
ME = []
ID = []
INFO = []

MES = {
	"T-CONT":1,
	"PRIORITY_QUEUE_G":2,
	"EXTENDED VLAN CONFIG DATA":3,
	"MAC BRIDGE PORT CONFIGURATION DATA":4,
	"VLAN TAGGING FILTER DATA":5,
	"GEM PORT CTP":6,
	"GEM PORT IW TP":7,
	"DS VLAN EGRESS":8,
	"PRIORITY QUEUE MAPPER":9
}

ME_label = {
	"T-CONT":"tcont",
	"PRIORITY_QUEUE_G":"pqueue",
	"EXTENDED VLAN CONFIG DATA":"evlan",
	"MAC BRIDGE PORT CONFIGURATION DATA":"mbpcd",
	"PRIORITY QUEUE MAPPER":"pqmap",
	"VLAN TAGGING FILTER DATA":"vtfd",
	"GEM PORT CTP":"gemctp",
	"GEM PORT IW TP":"gemiwtp",
	"DS VLAN EGRESS":"dsve"
}

def getData(log_file):
	fp = open(log_file, 'r')
	lines = fp.readlines()

	ms = ""  # save message_type temporarily
	me = ""  # save message entity temporarily

	tmp_info = "" # save me valid attributes
	flag = False  # used to record a segement of me

	for line in lines:

		n = line.strip().split("=") # split by '=' and remove spaces

		if n[0].strip() == "Msg_type":
			ms = n[1].strip()
			MS.append(ms)
			if re.match("(.*)RESPONSE", ms):
				INFO.append("")
			continue

		if n[0].strip() == "Entity_id":
			me = n[1].strip()
			ME.append(me)
			continue

		if n[0].strip() == "Instance_id":
			ID.append(n[1].strip())
			continue

		if re.match(r'(.*).value = ', line.strip()):
			flag = True
			key_value = line.split("=")
			tmp_info = tmp_info + key_value[0].replace(".value", "", 1).strip() +"="+ key_value[1].strip() + " "


		if not re.match("(.*)RESPONSE", ms) and not len(line.strip()) and flag:
			INFO.append(tmp_info)
			tmp_info = "" 				# reset tmp_info as null
			flag = False  				# reset flag as false


def drawOmciSession():
	dot_object = pydot.Dot(graph_type='digraph', rankdir="LR", labelloc='b',
						   ranksep = 4, nodesep = 0.2, splines = 'true')
	dot_object.set_node_defaults(shape='circle', fixedsize='true',
								 height=.2, width=.2, fontsize=6)

	plate_olt = pydot.Cluster(graph_name='OLT', label='OLT', fontsize=12, color = 'black', lp = 1 )
	plate_onu = pydot.Cluster(graph_name='ONU', label='ONU', fontsize=12, color = 'black')

	j = 1
	while(j < len(MS)*2 + 1):	
		if j % 2 == 1:
			label_seq = str(int((j+1)/2))
			plate_olt.add_node(pydot.Node(name=str(j), color = "black", label = label_seq))
		else:
			plate_onu.add_node(pydot.Node(name=str(j), color = "black",label = ""))
		j = j + 1

	k = 1
	while(k < len(MS)*2 + 1):
		index = int(k/2)
		try:
			label_text = MS[index] + "   " + ME[index] + "     " + ID[index] + "   " + INFO[index]
		except IndexError:
			print("Index out of range...")
			break
		xdir = "forword"
		if "RESPONSE" in MS[index]:
			xdir = "back"

		dot_object.add_edge(pydot.Edge(pydot.Node(name=str(k)), pydot.Node(name=str(k+1)),
									   label = label_text, dir = xdir, fontsize = 6))

		k = k + 2

	dot_object.add_subgraph(plate_olt)
	dot_object.add_subgraph(plate_onu)
	dot_object.write('graph.dotfile', format='raw', prog='dot')
	dot_object.write_pdf('omci_session.pdf', prog='dot')

def removeExistFile():
	for filename in os.listdir(os.getcwd()):
		os.remove(filename) if filename == "omci_session.pdf" else ''

if __name__ == "__main__":
	log_file = input("Please input log file path:")
	getData(log_file)
	removeExistFile()
	drawOmciSession()
	print("A omci_session.pdf file was created in current dir...")
	time.sleep(5)