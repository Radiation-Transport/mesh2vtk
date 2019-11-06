'''
########################################################################################################
# Copyright 2019 F4E | European Joint Undertaking for ITER and the Development                         #
# of Fusion Energy (‘Fusion for Energy’). Licensed under the EUPL, Version 1.1                         #
# or - as soon they will be approved by the European Commission - subsequent versions                  #
# of the EUPL (the “Licence”). You may not use this work except in compliance                          #
# with the Licence. You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl.html       #
# Unless required by applicable law or agreed to in writing, software distributed                      #
# under the Licence is distributed on an “AS IS” basis, WITHOUT WARRANTIES                             #
# OR CONDITIONS OF ANY KIND, either express or implied. See the Licence permissions                    #
# and limitations under the Licence.                                                                   #
########################################################################################################
'''

dep_path='./' # adjust this path to the location of the meshtal_mod.py module 
import os
import re
from sys import path
path.append(dep_path)  
from  meshtal_mod import *


principal_menu="""
 ***********************************************
   Process meshtally to VTK
 ***********************************************

 * Append meshtally file    (open)
 * Display mesh information (info)
 * Write VTK file           (write)
 * Mesh operation           (operate) 
 * Exit                     (end)
"""

info_menu="""
 * Mesh information         (meshinfo)
 * Tally information        (tallyinfo)
 * Exit                     (end)
"""

operate_menu="""
 * Mesh scale               (scale)
 * Mesh sum                 (sum)
 * Mesh difference          (diff)
 * Energy bin sum           (binsum)
 * Check identical mesh     (identical)
 * Change correlation       (corr)"""

def answer_loop(menu):
  pkeys = ['open','info','write','operate','end']
  ikeys = ['meshinfo','tallyinfo','end']
  okeys = ['scale','sum','diff','binsum','identical','corr']
  menulist = {'principal':pkeys, 'info':ikeys, 'operate':okeys}  
  while True:
    ans = input(" enter action :")
    ans = ans.split()
    ans0 = None
    ans1 = None
    if len(ans) > 0:
      ans0 = ans[0]
      if len(ans) > 1 :
        ans1 = ans[1]

    if menu == 'operate' and (ans1 == None and ans0 not in ['identical','corr']):
       if ans0 not in okeys:
         print(' bad operation keyword')
       else:
         print(' name of the result mesh is missing')
    elif ans0 in menulist[menu] : 
       break
    else:
      print(' not expected keyword')
  return ans0,ans1

def display_meshlist(opmesh=True):
    # display mesh list
    if opmesh : 
      nfiles = len(meshfiles) + len(newmesh)
    else:
      nfiles = len(meshfiles) 

    if nfiles > 1 :
      onefile = False
      for i,f in enumerate(meshfiles):
        print(" - {}".format(f))
        #tallylist = meshtally[i].mesh.keys()
        tallylist = list(meshtally[i].mesh.keys())
        tallylist.sort()
        for tally in tallylist:
          print("     - {}".format(tally))
    else:
      onefile = True
      tallylist = list(meshtally[0].mesh.keys())
      tallylist.sort()
      for tally in tallylist:
        print("     - {}".format(tally))

    if opmesh and len(newmesh) > 0 :
      print(" - Result mesh (result)")
      for rmesh in newmesh.keys(): 
         print("     - {}".format(rmesh))

    return onefile

def answer_meshlist(menu,answer,onefile=True):

    label_00 = ' select mesh, finish "end":'
    label_01 = ' tally and scaling factor "tally factor":'
    label_02 = ' mesh and scaling factor "tally factor", finish "end":'
    label_03 = ' first mesh  "tally":'
    label_04 = ' second mesh "tally":'
    label_05 = ' select mesh :'
    label_10 = ' select mesh "file tally", finish "end":'
    label_11 = ' meshtally file, tally and scaling factor "file tally factor":'
    label_12 = ' meshtally file, tally and scaling factor "file tally factor", finish "end":'
    label_13 = ' first mesh  "file tally":'
    label_14 = ' second mesh "file tally":'
    label_15 = ' select mesh "file tally":'

    label_one = [label_00,label_01,label_02,label_03,label_04,label_05]
    label     = [label_10,label_11,label_12,label_13,label_14,label_05]

    if menu == '3' :
      labelindex =  0 
      nans       =  2
      nvalues    = -1
    elif menu == '4' :
      if answer == 'scale' :
        labelindex =  1 
        nans       =  3
        nvalues    =  1
      elif answer == 'sum' :
        labelindex =  2 
        nans       =  3
        nvalues    = -1
      elif answer == 'diff' :
        labelindex =  3 
        nans       =  2
        nvalues    =  2
      elif answer == 'binsum' :
        labelindex =  5 
        nans       =  2
        nvalues    =  1
      else:
        labelindex =  3 
        nans       =  2
        nvalues    =  2

    finish = False
    mlist = []
    f1 = 1. 

    if onefile :
      nans = nans - 1

    # select mesh 
    ishft = 0
    tallylist = meshtally[0].mesh.keys()
    while not finish:
      while True:
        error = False 
        if onefile :
          sfile = input(label_one[labelindex + ishft])
          sfile = sfile.split()
          if len(sfile) == 1  and sfile[0] == 'end': 
            finish = True
            break
          if len(sfile) == nans :
            m1 = 0
            if len(sfile) == 1  and sfile[0] == 'all': 
              for tally in tallylist:
                mlist.append([m1,tally,f1])
              finish = True
              break
            try :
              tally = int(sfile[0])
            except :   
              tally = -1
            if tally  in tallylist :
              if nans == 2 :
                try : 
                  f1 = float(sfile[1])
                except:
                  error = True
                  print(' factor value should be float')
            else:
              error = True
              print(' bad tally values')
          else :
            error = True
            print(' {} values are entered,{} are expected'.format(len(sfile),nans))
        else :
          sfile = input(label[labelindex + ishft])
          sfile = sfile.split()
          if len(sfile) == 1 and sfile[0] == 'end': 
            finish = True
            break
          if len(sfile) == nans :
            if ( sfile[0] in meshfiles or sfile[0] == 'result'):
              if (sfile[0] == 'result'):
                tallylist = newmesh.keys()
                m1 = -1
                if len(sfile) == 2  and sfile[1] == 'all': 
                  for tally in tallylist:
                     tl = [m1,tally,f1]
                     if tl not in mlist:
                       mlist.append([m1,tally,f1])
                  break
                tally = sfile[1]
              else:
                m1 = meshfiles.index(sfile[0])
                tallylist = meshtally[m1].mesh.keys()
                if len(sfile) == 2  and sfile[1] == 'all': 
                  for tally in tallylist:
                     tl = [m1,tally,f1]
                     if tl not in mlist:
                       mlist.append([m1,tally,f1])
                  break
                try:
                  tally = int(sfile[1])
                except:
                  tally = -1

              if tally in tallylist :
                if nans == 3 :
                  try :
                    f1 = float(sfile[2])
                  except:
                    error = True
                    print(' factor value should be float')
              else:
                error = True
                print(' bad tally values')
            else:
              error = True
              print(' {} meshtally not found'.format(sfile[0]))
          else:
            error = True
            print(' {} values are entered,{} are expected'.format(len(sfile),nans))

        if not error :
          mlist.append([m1,tally,f1])
          if (menu == '4' and answer in ['diff','identical'] ) : ishft = 1
          if nvalues == len(mlist) : finish = True  
          break
    return mlist

def enterfilename(name):
    if name is None:
      fname = input(' enter Meshtally file name:')
    else:
      fname = name
    if fname != '' and fname not in meshfiles :
      if os.path.isfile(fname):
        meshfiles.append(fname)
      else:
        print (' {} not found'.format(fname))
      print('\n Input files :')
      for f in meshfiles:
         print(" - {}".format(f))

def mltf_option(meshtal):
    normopt=['none','vtot','celf','']
    #keys = meshtal.mesh.keys()
    keys = list(meshtal.mesh.keys())
    keys.sort()
    for k in keys: 
      m =  meshtal.mesh[k]
      if m.__format__ == 'mltf' :
        print (' Tally mesh {} is multiflux, set normalization.'.format(k))
        while True:
          ans=input(' {lab[0]}(default), {lab[1]}, {lab[2]}:'.format(lab=normopt))
          if ans in normopt: 
            if ans == '':
              m.__mltopt__ = normopt[0]
            else:
              m.__mltopt__ = ans
            print(' Normalization set to {}'.format(m.__mltopt__))
            break
          else:
            print ('bad normalization option')

def meshinfo():
    im  = 0
    print(info_menu)
    ans0,ans1 = answer_loop('info')
    
    if len(meshfiles) > 1 :
      print(' Input files :')
      for f in meshfiles:
         print(" - {}".format(f))
      while True:
        sfile = input(' Select file #:')
        if sfile in meshfiles:
          im = meshfiles.index(sfile)
          break
        else:
          print (' bad filename')

    #tallylist = meshtally[im].mesh.keys()
    tallylist = list(meshtally[im].mesh.keys())
    tallylist.sort()

    # print tally list
    if   ans0 == 'meshinfo' :
      meshtally[im].print_info()

    # print tally information
    elif ans0 == 'tallyinfo' :
      try:
        tally = int(ans1)
      except:
        tally = 0
      if tally not in tallylist:
        if ans1 is not None :
          print(' bad tally value')
        print(' Tallies :')
        for f in tallylist:
          print(" - tally {}".format(f))
        while True:
          tally = input(' Select tally #:')
          if tally.isdigit():
            tally = int(tally)
          if tally in tallylist: 
            break 
          else:
            print (' bad tally number')

      print(' Meshtally file : {}'.format(meshfiles[im]))
      meshtally[im].mesh[tally].print_info()
       
def vtkwrite():

    print(' select mesh to write to VTK :')
    # display mesh list
    onefile = display_meshlist(True)

    finish = False
    wlist  = []

    mlist = answer_meshlist('3',None,onefile)
    print ('')

    for  mid in mlist: 
      m1    = mid[0]
      tally = mid[1]
      tallyname = tally

      if (m1 != -1) :
        if ( not meshtally[m1].mesh[tally].filled ) :
           meshtally[m1].readMesh([tally])
        meshname  = meshfiles[m1]
        meshobj   = meshtally[m1].mesh[tally]
      else:
        if len(meshtally) == 1 :
          meshname  = meshfiles[m1]
        else:
          meshname  = 'result'
        meshobj   = newmesh[tally]


      # write mesh into VTK
      if meshobj.cart:
        name = '{}_{}.vtr'.format(meshname,tallyname)
      else:
        name = '{}_{}.vts'.format(meshname,tallyname)
      print ( ' Write mesh {}'.format(name))
      meshobj.writeVTK(name)

         
def operate():
    global idadd,corr

    print(operate_menu)
    print('   correlation : {}'.format(corr))
    ans,meshname = answer_loop('operate')

    if ans != 'corr':
      # display mesh list
      onefile = display_meshlist(False)

    if ans == 'scale' : 
      mlist = answer_meshlist('4',ans,onefile)
      if len(mlist) > 0 :
        m1    =  mlist[0][0] 
        tally =  mlist[0][1] 
        sfact =  mlist[0][2]
        if not meshtally[m1].mesh[tally].filled :
           meshtally[m1].readMesh([tally])
        smesh = scalemesh(meshtally[m1].mesh[tally],sfact)
        newmesh[meshname]=smesh

    elif ans == 'sum' : 
      idadd += 1
      mlist = answer_meshlist('4',ans,onefile)
      if len(mlist) > 1 :
        smesh = AddMesh(mlist)
        if smesh is not None: newmesh[meshname]=smesh

    elif ans == 'diff' : 
      mlist = answer_meshlist('4',ans,onefile)
      if len(mlist) == 2 :
        smesh = DiffMesh(mlist[0],mlist[1])
        if smesh is not None: newmesh[meshname]=smesh

    if ans == 'binsum' : 
      mlist = answer_meshlist('4',ans,onefile)
      if len(mlist) > 0 :
        m1    =  mlist[0][0] 
        tally =  mlist[0][1] 
        if not meshtally[m1].mesh[tally].filled :
           meshtally[m1].readMesh([tally])
        meshtally[m1].mesh[tally].print_EbinRange()

        while True:
          ans=input(' Enter bin index list:' ) 
          if ans == 'all':
             binlist = range(len(meshtally[m1].mesh[tally].ener))
             break
          elif re.search(r'[^\d +-]',ans) is None:
             binlist=ans.split()
             # binlist = map(int,binlist)
             # binlist.sort()
             binlist = sorted(map(int,binlist))
             if binlist[0] >= 0 and binlist[-1] < len(meshtally[m1].mesh[tally].ener) : break
          print (' bad bin list values')

        bmesh = addbin(meshtally[m1].mesh[tally],binlist,corr=corr)
        newmesh[meshname]=bmesh

    elif ans == 'identical' : 
      mlist = answer_meshlist('4',ans,onefile)
      if len(mlist) == 2 :
        m1 = meshtally[mlist[0][0]].mesh[mlist[0][1]]
        m2 = meshtally[mlist[1][0]].mesh[mlist[1][1]]
        print_identical(m1,m2)

    elif ans == 'corr' : 
      corr = not corr
      print(' Correlation set to {}'.format(corr))


def print_identical(m1,m2):

   part, mesh, mtyp = identical_mesh(m1,m2)

   if False not in [part,mesh,mtyp]: 
     print (' Meshes are identical')
   else:
     if not mesh : print (' Meshes are different')
     if not part : print (' Particles are different')
     if not mtyp : print (' Mesh types are different')

def AddMesh(mlist):
   noread = {}   
   for m in mlist:
     if not meshtally[m[0]].mesh[m[1]].filled:
        if m[0] in noread.keys():
          noread[m[0]].append(m[1])
        else:
          noread[m[0]] = [m[1]]
   for k in noread.keys() :
      meshtally[k].readMesh(noread[k])

   m1 = meshtally[mlist[0][0]].mesh[mlist[0][1]]
   m2 = meshtally[mlist[1][0]].mesh[mlist[1][1]]
   f1 = mlist[0][2]
   f2 = mlist[1][2]
   msum = addmesh(m1,m2,f1,f2,corr=corr)
   if msum is None: return
   for m in mlist[2:]:
     mi = meshtally[m[0]].mesh[m[1]]  
     fi = m[2]  
     msum  = addmesh(msum,mi,1.,fi,corr=corr)
     if msum is None: return
   return msum

def DiffMesh(mlst1,mlst2):
   if not meshtally[mlst1[0]].mesh[mlst1[1]].filled:
      meshtally[mlst1[0]].readMesh([mlst1[1]])
   if not meshtally[mlst2[0]].mesh[mlst2[1]].filled:
      meshtally[mlst2[0]].readMesh([mlst2[1]])

   m1 = meshtally[mlst1[0]].mesh[mlst1[1]]
   m2 = meshtally[mlst2[0]].mesh[mlst2[1]]

   return diffmesh(m1,m2)

def clear_screen():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')

meshfiles = []    # list stroing filename
meshtally = []    # list storing meshtal objects
newmesh   = {}    # mesh produced after operation
idadd     = 0
corr      = False

clear_screen()
print(principal_menu)
ans,optname=answer_loop('principal')
while True:

  # enter meshtally filename
  if ans[0:4] == 'open' :
    enterfilename(optname)
    if len(meshfiles) > len(meshtally):
      filetype='MCNP'

      meshtally.append(Meshtal(meshfiles[-1],filetype))
      mltf_option(meshtally[-1])

  # Print meshtally information
  elif ans == 'info' :
    if len(meshfiles) == 0:
      print(' No meshtally file')
    else:
      meshinfo()

  # Write mesh to VTK
  elif ans == 'write':
    if len(meshfiles) == 0:
      print(' No meshtally file')
    else:
      vtkwrite()

  # operate on mesh
  elif ans == 'operate':
    if len(meshfiles) == 0:
      print(' No meshtally file')
    else:
      operate()
  else:
    break

  ans,optname=answer_loop('principal')
  clear_screen()
  print(principal_menu)
