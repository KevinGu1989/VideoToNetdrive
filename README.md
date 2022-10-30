# VideoToNetdrive
A python script to help converting all videos within a local directory and upload them to net drive by WebDav


#Prerequisite
##1. Ffmpeg
Download and Install ffmpeg command line tool from http://ffmpeg.org/download.html

Make sure your ffmpeg command line is working fine.

##2. Converter your net drive to WebDav protocol 
I'm using Alist which can consolidate my net drives as well as providing WebDav protocol access to them

Alist install guide:
https://alist.nn.ci/guide/

##3. Install required python libs
`pip install -r ./requirements.txt`


#How to run
Before running the main.py, you should config your own config.yaml

```
#local paths
#Your input directory for your videos
input_local_path: L:/DCIM/100MEDIA

#Your output directory for your videos
output_local_path: Z:/famlily/20221031

#for args please don't miss the place holder {input_name} and {output_name}
ffmpeg_cmd_template: 'ffmpeg -hwaccel cuvid  -c:v h264_cuvid -i {input_name}  -c:v h264_nvenc -b:v 12800k -bufsize 12800k -y  {output_name}'

webdav:
  copy_to_webdav: True
  web_dav_path: /baidu/famlily/20221031
  options:
    #web dav host
    'webdav_hostname': "http://192.168.1.2:1234/dav"
    'webdav_login': "user"
    'webdav_password': "1111111"
    'disable_check': True
```

Once you complete your config.yaml you can run the .py script to execute the job.

`python ./main.py`