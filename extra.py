#!/usr/bin/python
import json
import math
for dataset in ["89"]:
  infile="CH"+dataset+".JSON"
  outfile="NW"+dataset+".JSON" 
  with open(infile) as jsonfile:
    dataset = json.load(jsonfile)
  dodrop=set()
  dataset["desc"]["X001"]="Animal-protein as percentage of total protein."
  dataset["desc"]["X002"]="Added animal fat as percentage of total added fat."
  dataset["desc"]["X003"]="N6/n3 ratio"
  dataset["desc"]["X004"]="Nonhdl/hdl ratio"
  dataset["desc"]["X005"]="Apo-b/Apo-a1 ratio"
  dataset["desc"]["X006"]="Aop-a/Nonhdl"
  dataset["desc"]["X007"]="Red meat as percentage of animal-based food"
  dataset["desc"]["X008"]="Eggs as percentage of animal-based food"
  dataset["desc"]["X009"]="Dairy as percentage of animal-based food"
  dataset["desc"]["X010"]="Added fat as percentage of animal-based food"
  dataset["desc"]["M200"]="mortality Probability of living upto the age of 80 years old."
  dataset["desc"]["M201"]="isch/cereb mortality ratio (35..69)." 
  for num in range(1,148):
    snum = str(num).zfill(3)
    val = dataset["desc"]["D"+snum]
    if "g/day" in val or "kcal/day" in val:
       dataset["desc"]["W"+snum] = val.replace("g/day","g/day/kg").replace("kcal/day","kcal/day/kg").replace("diet survey","per body mass")
  for num in range(1,184):
    snum = str(num).zfill(3)
    val = dataset["desc"]["Q"+snum]
    if "g/day" in val or "g per person" in val:
       dataset["desc"]["Y"+snum] = val.replace("g/day","g/day/kg").replace("g per person","g per kg body weight").replace("questionnaire","per body mass")
  for index in range(0,len(dataset["data"])):
    xiang=dataset["data"][index]["dt"]
    for gender in ["M","F","T"]:
      if gender in xiang:
        xiangsubset=xiang[gender]
        if ("D003" in  xiangsubset) and ("D034" in   xiangsubset):
          t1=1.0 * xiangsubset["D003"]
          a1=1.0 * xiangsubset["D034"]
          if t1 > 0:
            p1 = 100.0 * a1 / t1
            xiangsubset["X001"]=round(p1,4)
        if ("D055" in  xiangsubset) and ("D053" in   xiangsubset):
          t2=1.0 * xiangsubset["D055"]
          a2=1.0 * xiangsubset["D053"]
          if t2 > 0:
            p2 = 100.0 * a2 / t2
            xiangsubset["X002"]=round(p2,4)
        if ("D093" in  xiangsubset) and ("D092" in   xiangsubset):
          n6=1.0 * xiangsubset["D093"]
          n3=1.0 * xiangsubset["D092"]
          if n3 > 0:
            p3 = n6 / n3
            xiangsubset["X003"]=round(p3,4)
        if ("P002" in xiangsubset) and ("P003" in xiangsubset):
          hdl = 1.0 * xiangsubset["P002"]
          nonhdl = 1.0 * xiangsubset["P003"]
          if hdl > 0:
            p6 = nonhdl / hdl
            xiangsubset["X004"]=round(p6,6)
        if ("P004" in xiangsubset) and ("P005" in xiangsubset):
          apoa = xiangsubset["P004"]
          apob = xiangsubset["P005"]
          if apoa > 0:
            p7 = apob / apoa
            xiangsubset["X005"] = round(p7,6)
        if ("P004" in xiangsubset) and ("P003" in xiangsubset):
          apoa = xiangsubset["P004"]
          nonhdl = xiangsubset["P003"]
          xiangsubset["X006"] = round(math.sqrt(apoa * nonhdl),6)
        if (("M063" in xiangsubset) and ("M065" in xiangsubset)):
          isch = xiangsubset["M063"]
          cereb = xiangsubset["M065"]
          if cereb > 0:
            xiangsubset["M201"] = 1.0*isch/cereb;
        if (("D029" in xiangsubset) and ("D050" in xiangsubset)):
          meat = xiangsubset["D050"]
          animal = xiangsubset["D029"]
          if animal > 0:
            xiangsubset["X007"] = 100.0*meat/animal;
        if (("D029" in xiangsubset) and ("D050" in xiangsubset)):
          eggs = xiangsubset["D048"]
          animal = xiangsubset["D029"]
          if animal > 0:
            xiangsubset["X008"] = 100.0*eggs/animal;
        if (("D029" in xiangsubset) and ("D050" in xiangsubset)):
          dairy = xiangsubset["D047"]
          animal = xiangsubset["D029"]
          if animal > 0:
            xiangsubset["X009"] = 100.0*dairy/animal;
        if (("D029" in xiangsubset) and ("D050" in xiangsubset)):
          fat = xiangsubset["D053"]
          animal = xiangsubset["D029"]
          if animal > 0:
            xiangsubset["X010"] = 100.0*fat/animal;
        if ("M001" in xiangsubset) and ("M002" in xiangsubset) and ("M003" in xiangsubset) and ("M005" in xiangsubset) and ("M006" in xiangsubset) :
          m1 = math.pow(1.0 - (1.0 * xiangsubset["M001"] / 1000),5)
          m2 = math.pow(1.0 - (1.0 * xiangsubset["M002"] / 100000),10)
          m3 = math.pow(1.0 - (1.0 * xiangsubset["M003"] / 100000),20)
          m5 = math.pow(1.0 - (1.0 * xiangsubset["M005"] / 1000),35)
          m6 = math.pow(1.0 - (1.0 * xiangsubset["M006"] / 1000),10)
          survival = 100.0 * m1 * m2 * m3 * m5 * m6 
          xiangsubset["M200"]=round(survival,6)
        if "Q091" in xiangsubset and xiangsubset["Q091"] > 0:
          weight = xiangsubset["Q091"]
          for num in range(1,148):
            snum = "W" + str(num).zfill(3)
            onum = "D" + str(num).zfill(3)
            if snum in dataset["desc"] and onum in xiangsubset: 
              xiangsubset[snum] = 1.0 * xiangsubset[onum] / weight
          for num in range(1,184):
            snum = "Y" + str(num).zfill(3)
            onum = "Q" + str(num).zfill(3)
            if snum in dataset["desc"] and onum in xiangsubset:
              xiangsubset[snum] = 1.0 * xiangsubset[onum] / weight
         
  f = open(outfile, 'w')
  f.write(json.dumps(dataset,sort_keys=True,indent=4, separators=(',', ': ')))
  f.close()
