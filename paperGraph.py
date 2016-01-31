#(C)2015: Graeham Douglas, Liam Atkinson, Kyata Chibalabala
import requests
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, session, g, _app_ctx_stack, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import urllib
from time import sleep
from xml.etree import ElementTree as ET
import csv

app = Flask(__name__)
app.config.from_pyfile('paperGraph.cfg')
db = SQLAlchemy(app)


class Papers(db.Model):
	__tablename__ = 'papers'
	id = db.Column('paper_id', db.Integer, primary_key=True)
	pm_id = db.Column(db.String, unique=True) #PubMed ID
	doi_id = db.Column(db.String)#unique ID from DOI
	title = db.Column(db.String)
	journal = db.Column(db.String)
	is_local = db.Column(db.Integer)
	
	def __init__(self,pm_id,doi_id,title,journal,is_local):
		self.pm_id = pm_id
		self.doi_id = doi_id
		self.title = title
		self.journal = journal
		self.is_local = is_local
		
class Cited(db.Model):
	__tablename__ = 'cited'
	id = db.Column('cite_id', db.Integer, primary_key = True)
	cited_in = db.Column(db.Integer)
	cited_by = db.Column(db.Integer)
	
	def __init__(self,cited_in,cited_by):
		self.cited_in = cited_in
		self.cited_by = cited_by
		

@app.route('/')
def hello_world():
	#paper_lists = ['23609894', '9805198', '15165869', '1604319']
	paper_lists = []
	with open ("temp_pmids.csv", "rb") as listfile:
		papers_in = csv.reader(listfile, delimiter=',')
		for row in papers_in:
			paper_lists.append(row)	
	#import pdb; pdb.set_trace()
	#paper_list = Papers.query.all()
	for paper_idx in range(108,len(paper_lists[0])):#change to include articles we want to scrape citations of/from
		print paper_idx
		start_id=paper_lists[0][paper_idx]	
		#start_id=paper_lists[paper_idx].pm_id	
		#start_id = "21876726"
		start_title = "a title"
		if Papers.query.filter_by(pm_id=start_id).first() is None:
			add_paper = Papers(start_id,'doi',start_title,'a journal',1)
			db.session.add(add_paper)
			db.session.commit()
		paper_id = Papers.query.filter_by(pm_id=start_id).first().id
		get_cited_in(start_id)
		get_cited_by(start_id)
		sleep(1) #to slow down request numbers to pubmed
	paper_nodes()
	paper_links()
	return 'Hello World!'
	


	
def get_cited_in(pm_id):
	cited_in = Papers.query.filter_by(pm_id=pm_id).first().id
	cited_in_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pmc_refs&id=%s&tool=paperGraph&email=graeham.douglas@gmail.com" %pm_id 
	root = ET.parse(urllib.urlopen(cited_in_url)).getroot()
	#print root
	linkset = root.find('LinkSet/LinkSetDb')
	if linkset is not None:
		links = linkset.findall('Link')
		for Link in links:
			new_id = Link.find('Id').text
			if Papers.query.filter_by(pm_id=new_id).first() is None:
				add_paper = Papers(new_id,'doi','a title','a journal',0)
				db.session.add(add_paper)
				db.session.commit()
			cited_by = Papers.query.filter_by(pm_id=new_id).first().id
			add_ref = Cited(cited_in,cited_by)
			db.session.add(add_ref)
			db.session.commit()
			
	return "That worked, thanks :)", 200
		
def get_cited_by(pm_id):
	cited_by = Papers.query.filter_by(pm_id=pm_id).first().id
	cited_by_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pmc&linkname=pmc_refs_pubmed&id=%s&tool=paperGraph&email=graeham.douglas@gmail.com" %pm_id 
	root = ET.parse(urllib.urlopen(cited_by_url)).getroot()
	#print root
	#import pdb; pdb.set_trace()
	linkset = root.find('LinkSet/LinkSetDb')
	if linkset is not None:
		links = linkset.findall('Link')
		for Link in links:
			new_id = Link.find('Id').text
			if Papers.query.filter_by(pm_id=new_id).first() is None:
				add_paper = Papers(new_id,'doi','a title','a journal',0)
				db.session.add(add_paper)
				db.session.commit()
			cited_in = Papers.query.filter_by(pm_id=new_id).first().id
			add_ref = Cited(cited_in,cited_by)
			db.session.add(add_ref)
			db.session.commit()
	
	return "That worked, thanks :)", 200
	
def get_article_metadata(pm_id):
	article_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=%s&tool=paperGraph&email=graeham.douglas@gmail.com&retmode=json" %pm_id
	article_metadata = requests.get(article_url)
	art_meta = article_metadata.json()
	title = art_meta['result'][pm_id]['title']
	authors = art_meta['result'][pm_id]['authors']
	journal = art_meta['result'][pm_id]['fulljournalname']
	doi_long = art_meta['result'][pm_id]['elocationid']
	#import pdb; pdb.set_trace()
	return "That worked, thanks :)", 200
	
def paper_nodes():
	paper_list = Papers.query.all()
	#node is pm_id, group is is_local
	#write file
	nodes = open('nodes.dat','w')
	for i in range(len(paper_list)):
		name = paper_list[i].pm_id
		group = paper_list[i].is_local
		nodes.write('%s %i \n' %(name,group))
	return "file written", 200
	

def paper_links():
	cites_list = Cited.query.all()
	#source is cited_in, target is cited by. value??
	#write file
	cite = open('links.dat','w')
	for i in range(len(cites_list)):
		#print i
		#source = cites_list[i].cited_in
		#target = cites_list[i].cited_by
		source = Papers.query.filter_by(id=cites_list[i].cited_in).first().pm_id
		target = Papers.query.filter_by(id=cites_list[i].cited_by).first().pm_id
		value = 1.0
		cite.write('%s %s %f \n' %(source,target,value))
	return "file written", 200
	

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=int(port),debug=True)
