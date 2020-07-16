import jinja2
import yaml
import os
import sys

'''
 CURRENTDIR is the directory where <jinja2-file>.j2 is located
 output file <jinja2-file>
 data.yml includes vars to be replaced
'''

if __name__=="__main__":
    if len(sys.argv) < 2 :
        print('Usage: %s /path/to/file.j2 [/path/to/data.yml]'%(sys.argv[0]))
        sys.exit(0)
    template_f = sys.argv[1] # e.g. /path/to/Dockerfile.j2
    data_yml = sys.argv[2] if len(sys.argv) > 2 else None # /path/to/vars.yml
    config = {}

    workdir = os.path.abspath(os.path.dirname(template_f))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(workdir))
    filename = os.path.basename(template_f)
    template = env.get_template(filename)

    if data_yml is not None:
        with open(data_yml, 'r') as f:
            config = yaml.load(f)
    config['CURRENTDIR'] = workdir
    print config

    content = template.render(config) #, env=os.environ)
    outfile = filename.strip('.j2')
    content_path = os.path.join(workdir, outfile)
    with open(content_path, 'w') as f:
        f.write(content)
        print('%s/%s created.'%(workdir,outfile))

