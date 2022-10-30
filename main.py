import subprocess
import os
import os.path
from webdav3.client import Client
import yaml


def load_yaml(yaml_path):
    fs = open(os.path.join(yaml_path), encoding="UTF-8")
    settings = yaml.load(fs, Loader=yaml.FullLoader)
    return settings


setting = load_yaml('./config.yaml')

print('Yaml loaded: ', setting)
print(os.listdir(setting['input_local_path']))
ffmpeg_cmd_template = setting['ffmpeg_cmd_template']


def compress_vedio(input_path, nas_path):
    for v in os.listdir(input_path):
        abs_in_path = os.path.abspath((os.path.join(input_path, v)))
        abs_out_path = os.path.abspath((os.path.join(nas_path, v)))
        ffmpeg_cmd = ffmpeg_cmd_template.format(input_name=abs_in_path, output_name=abs_out_path)
        print(ffmpeg_cmd)
        # subprocess.run(ffmpeg_cmd, encoding="utf-8", shell=True)
        p = subprocess.Popen(ffmpeg_cmd, encoding="utf-8", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        counter = 0
        # Trigger ffmpeg
        while p.poll() == None:
            out = p.stdout.readline().strip()
            counter = counter + 1
            if out and counter % 20 == 0:
                print(out)

    print('Video converted！！！')


def upload(options, local_path, web_dav_path):
    print(options, local_path, web_dav_path)
    client = Client(options)
    print(client.list())
    print(web_dav_path, local_path)
    try:
        client.upload(web_dav_path, local_path)
        print('Video uploaded: ' + web_dav_path)
    except Exception as e:
        print(e.__traceback__)


def upload_async(options, local_path, web_dav_path):
    # Unload resource
    client = Client(options)

    kwargs = {
        'remote_path': web_dav_path,
        'local_path': local_path,
        'callback': lambda: print('Video uploaded:', web_dav_path)
    }

    try:
        client.upload_async(**kwargs)
    except Exception as e:
        print(e.__traceback__)


def upload_file(input_path):
    if setting['webdav']['copy_to_webdav']:
        for v in os.listdir(input_path):
            abs_in_path = os.path.abspath((os.path.join(input_path, v)))
            web_dav_file_path = setting['webdav']['web_dav_path'] + '/' + v
            upload(setting['webdav']['options'], abs_in_path, web_dav_file_path)


compress_vedio(setting['input_local_path'], setting['output_local_path'])
upload_file(setting['output_local_path'])
