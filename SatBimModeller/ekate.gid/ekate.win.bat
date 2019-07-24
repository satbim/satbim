REM    OutputFile: $2/$1.info
REM    ErrorFile: $2/$1.err
REM    delete previous result file 
DEL "%2\*.post.res" 
DEL "%2\*.post.msh"
DEL "%2\*.post.bin"
COPY "C:\Program Files\GiD\GiD 12.0.10\problemtypes\ekate.gid\sed.exe" "%2"
COPY "C:\Program Files\GiD\GiD 12.0.10\problemtypes\ekate.gid\regex2.dll" "%2"
COPY "C:\Program Files\GiD\GiD 12.0.10\problemtypes\ekate.gid\libintl3.dll" "%2"
COPY "C:\Program Files\GiD\GiD 12.0.10\problemtypes\ekate.gid\libiconv2.dll" "%2"
REM renaming Kratos input files
REN "%2\%1.dat" "%2\%1.mdpa"
REN "%2\%1-1.dat" "%2\%1.py"
REN "%2\%1-2.dat" "%2\%1_include.py"
REN "%2\%1-3.dat" "%2\%1_layers.py"
ECHO >> "%2\%1.ess"
TYPE "%2\%1.ess" >> "%2\%1.py"
SED "s\rEpLaCeMeNtStRiNg\%1\g" < "%2\%1.py" > "%2\%1.py_changed"
REN "%2\%1.py_changed" "%2\%1.py"
CD "%2"
CD ..

