import sys,os

d=os.path.dirname(os.path.realpath(__file__))
pkdoc_all=os.path.join(d,"tools","pkdoc_all.py")
configs=os.path.join(d,"configs")
cmd="python %s %s"%(pkdoc_all,configs)
print cmd
os.system(cmd)

