import json
import os
import shutil
import subprocess
import sys
import webbrowser

docker_image = 'alphamj/os-contest:v6.3'


def clean_project(submit_dir):
    file_list = ['initrd.img', 'kernel-qemu', 'os_serial_out.txt', 'sbi-qemu', 'sdcard.img']
    for file in file_list:
        path = os.path.join(submit_dir, file)
        if os.path.exists(path):
            os.unlink(path)


def main():
    submit = sys.argv[1]

    if submit.startswith('http') or submit.startswith('git@'):
        subprocess.call(f"git clone {submit} submit")
        submit = os.path.join(os.getcwd(), 'submit')

    testdata = os.path.join(os.getcwd(), 'testdata')
    kernel = os.path.join(os.getcwd(), 'kernel.zip')

    clean_project(submit)

    cmd = f"docker run --rm "
    cmd += f" -v {testdata}:/coursegrader/testdata -v {submit}:/coursegrader/submit -v {kernel}:/cg/kernel.zip "
    cmd += f" --entrypoint python3 "
    cmd += f" {docker_image} /cg/kernel.zip"
    print(cmd)
    output = subprocess.check_output(cmd)

    result = json.loads(output)
    print(f"score: {result['score']}")
    with open("detail.html", "w", encoding='utf-8') as f:
        f.write(f"<div>{result['comment']}</div>")
        f.write(f"<div>{result['detail']}</div>")

    clean_project(submit)
    webbrowser.open(os.path.join(os.getcwd(), "detail.html"))


if __name__ == '__main__':
    main()
