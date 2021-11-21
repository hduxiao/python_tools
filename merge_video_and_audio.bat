call ffmpeg -i %1 -vn -codec copy out_tmp.m4a
call ffmpeg -i %2 -i out_tmp.m4a -vcodec copy -acodec copy %3
del /f /s /q out_tmp.m4a
