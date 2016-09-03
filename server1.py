#!/usr/bin/python
import cherrypy
from cherrypy.lib import file_generator
import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy 
import json
from cherrypy.process.plugins import Daemonizer
from threading import Thread, Lock

def fetchdoubleornot(var,path,var2,path2,datapoint,datapoint2):
  if path[0] in datapoint and path2[0] in datapoint2:
    if len(path) > 1 and len(path2) > 1:
      return fetchdoubleornot(var,path[1:],var2,path2[1:],datapoint[path[0]],datapoint2[path2[0]])
    else:
      if var in datapoint[path[0]] and  var2 in datapoint2[path2[0]]:
        return (datapoint[path[0]][var],datapoint2[path2[0]][var2])
      else:
        return None
  else:
    return None

def fetchdouble(var1,path1,var2,path2,datapoints):
  for datapoint in datapoints:
    rv=fetchdoubleornot(var1,path1,var2,path2,datapoint["dt"],datapoint["dt"])
    if rv != None:
      yield rv



class DataSetBrowser(object):
  def __init__(self,dataset):
    self.dataset = dataset
    self.mutex = Lock()
  def varsasarray(self,var1,path1,var2,path2):
    rv1=[]
    rv2=[]
    for v in fetchdouble(var1,path1,var2,path2,self.dataset["data"]):
      rv1.append(v[0])
      rv2.append(v[1])
    return (rv1,rv2)
  def hasgender(self,f,gender):
    for datapoint in self.dataset["data"]:
      if gender in datapoint["dt"]:
        if f in datapoint["dt"][gender]:
          return True
    return False
  def fullname(self,f):
    return self.dataset["desc"][f]
  def getgenders(self,f):
    genders = set()
    for gender in ["T","M","F"]:
      if self.hasgender(f,gender):
        genders.add(gender)
    return genders
  @cherrypy.expose
  def index(self):
    return "<H3>China Study II uni-var browser</H3><FORM action=\"/choose2\" method=\"GET\"><SELECT name=\"t1\"><OPTION value=\"D\">Dietary survey (original)</OPTION><OPTION value=\"W\">Dietary survey (per body mass)</OPTION><OPTION value=\"Q\">Questionnaire (original)</OPTION><OPTION value=\"Y\">Questionnaire (per body mass)</OPTION><OPTION value=\"X\">Composite variables</OPTION><OPTION value=\"G\">General features</OPTION><OPTION value=\"U\">Urine</OPTION><OPTION value=\"P\">Blood (plasma)</OPTION><OPTION value=\"R\">Blood (red)</OPTION><OPTION value=\"M\">Mortality</OPTION></SELECT><br><SELECT name=\"t2\"><OPTION value=\"D\">Dietary survey (original)</OPTION><OPTION value=\"W\">Dietary survey (per body mass)</OPTION><OPTION value=\"Q\">Questionnaire (original)</OPTION><OPTION value=\"Y\">Questionnaire (per body mass)</OPTION><OPTION value=\"X\">Composite variables</OPTION><OPTION value=\"G\">General features</OPTION><OPTION value=\"U\">Urine</OPTION><OPTION value=\"P\">Blood (plasma)</OPTION><OPTION value=\"R\">Blood (red)</OPTION><OPTION value=\"M\">Mortality</OPTION></SELECT><br><BUTTON type=\"submit\">Continue</BUTTON></FORM>"
  @cherrypy.expose
  def choose2(self,t1="D",t2="M"):
    desc = self.dataset["desc"]
    r1 = "<H3>China Study II uni-var browser</H3><FORM action=\"/choose3\" method=\"GET\"><SELECT name=\"f1\">"
    r2= ""
    for key in sorted(desc):
      if key[0] == t1:
        r2 = r2 + "<OPTION value=\"" + key + "\">" + desc[key] + "</OPTION>" 
    r3 = "</SELECT><br><SELECT name=\"f2\">"
    r4 = ""
    for key in sorted(desc):
      if key[0] == t2:
        r4 = r4 + "<OPTION value=\"" + key + "\">" + desc[key] + "</OPTION>"
    r5 = "</SELECT><br><SELECT name=\"deg\"><OPTION value=\"2\">polyfit (deg=2)</OPTION><OPTION value=\"3\">polyfit (deg=3)</OPTION><OPTION value=\"4\">polyfit (deg=4)</SELECT><br><BUTTON type=\"submit\">Continue</BUTTON></FORM>"
    return r1 + r2 + r3 + r4 + r5
  @cherrypy.expose
  def choose3(self,f1,f2,deg):
    genders1 = self.getgenders(f1)
    genders2 = self.getgenders(f2)
    print "genders:",genders1,genders2
    i = genders1.intersection(genders2)
    rval = ""
    if len(i) == 0:
       if len(genders1) == 1 and len(genders2) == 1:
         g1=genders1.pop()
         g2=genders2.pop()
         return self.primary(f1,f2,g1,g2,deg)
       for g1 in genders1:
         for g2 in genders2:
           rval = rval + "<A HREF=\"primary?f1=" + f1 + "&g1=" + g1 + "&f2=" + f2 + "&g2=" + g2 + "\">" + g1 + "=&gt;" + g2 + "&deg=" + deg +"</A><br>"
       return rval
    else:
      if len(i) == 1:
        g=i.pop()
        return self.primary(f1,f2,g,g,deg)
      for g in i:
        rval = rval + "<IMG SRC=\"primary?f1=" + f1 + "&g1=" + g + "&f2=" + f2 + "&g2=" + g +"&deg=" + deg + "\"><br>"   
      return rval
  @cherrypy.expose
  def primary(self,f1="D001",f2="X007",g1="T",g2="T",deg="3"):
    n=int(deg)
    (a1,a2) = self.varsasarray(f1,g1,f2,g2)
    xp =  numpy.linspace(numpy.amin(a1), numpy.amax(a1), 100)
    cherrypy.response.headers['Content-Type'] = "image/png"
    buffer = StringIO.StringIO()
    fit,C_p = numpy.polyfit(a1, a2, n, cov=True) 
    p = numpy.poly1d(fit)
    p1 = numpy.poly1d(numpy.polyfit(a1, a2, 1))
    self.mutex.acquire()
    try:
        plt.xlabel(self.fullname(f1) + " G=" + g1)
        plt.ylabel(self.fullname(f2) + " G=" + g2)
        plt.suptitle("Fit for Polynomial (degree {})".format(n))
        plt.scatter(a1,a2)
        plt.plot(xp, p(xp), '-',xp, p1(xp), '-')
        fig = plt.gcf()
        fig.savefig(buffer, format='png')
        plt.clf()
    finally:
        self.mutex.release()
    buffer.seek(0)
    return file_generator(buffer)
  @cherrypy.expose
  def ll0(self):
    return "<H3>China Study II longlivety explorer</H3><FORM action=\"ll1\" method=\"GET\"><SELECT name=\"t1\"><OPTION value=\"D\">Dietary survey</OPTION><OPTION value=\"Q\">Questionnaire</OPTION><OPTION value=\"U\">Urine</OPTION><OPTION value=\"R\">Blood (red)</OPTION><OPTION value=\"P\">Blood (plasma)</OPTION></SELECT><BUTTON type=\"submit\">Continue</BUTTON></FORM>"

if __name__ == '__main__':
    datapath = "./NW89.JSON"
    dataset = None
    with open(datapath) as jsonfile:
      dataset = json.load(jsonfile)
    d = Daemonizer(cherrypy.engine)
    d.subscribe()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'}) 
    cherrypy.quickstart(DataSetBrowser(dataset))
