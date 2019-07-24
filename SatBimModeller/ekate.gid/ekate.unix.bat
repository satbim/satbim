#!/bin/sh -f
#   OutputFile: $2/$1.info
#   ErrorFile: $2/$1.err
#   delete previous result file
#   Naming convention:
#       $1: name of the current project
#       $2: path of the current project
#       $3: path of the problem type
rm -f $2/*.post.res 
rm -f $2/*.post.msh
rm -f $2/*.post.bin
# clean the empty fields in mdpa
python $3/clean_mdpa.py $2/$1.dat $2/$1.bak
rm $2/$1.dat
mv $2/$1.bak $2/$1.dat
# renaming Kratos input files
mv $2/$1.dat $2/$1.mdpa
mv $2/$1-1.dat $2/${1}.inp
mv $2/$1-2.dat $2/${1}.py
mv $2/$1-3.dat $2/${1}_include.py
mv $2/$1-4.dat $2/${1}_layers.py
touch $2/$1.ess
#touch $2/set_material_data.py
cat $2/$1.ess >> $2/$1.py
sed s/rEpLaCeMeNtStRiNg/$1/g < $2/$1.py > $2/$1.py_changed
mv $2/$1.py_changed $2/$1.py
cd $2
cd ..
