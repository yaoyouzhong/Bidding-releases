"""Distribution-only GitHub assembly job: verify bytes, never execute installer."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

REPO='yaoyouzhong/Bidding-releases'

def validate(manifest, expected):
    if manifest.get('format')!=1 or manifest.get('sha256')!=expected:
        raise ValueError('Manifest identity mismatch')
    if not re.fullmatch(r'Biaoshu_\d+\.\d+\.\d+_x64-setup\.exe',manifest.get('name','')):
        raise ValueError('Invalid installer name')
    parts=manifest.get('parts',[])
    if not 1<=len(parts)<=512:raise ValueError('Invalid chunk count')
    for i,p in enumerate(parts,1):
        if p['name']!=f'upload-{expected}.part{i:04d}' or not 0<p['size_bytes']<=8*1024*1024 or not re.fullmatch('[0-9a-f]{64}',p['sha256']):
            raise ValueError('Invalid chunk identity/size/order')
    if sum(p['size_bytes'] for p in parts)!=manifest['size_bytes'] or not manifest['size_bytes']<=2*1024**3:
        raise ValueError('Invalid total size')
    return parts

def merge(manifest, expected, directory, output):
    parts=validate(manifest,expected);total=hashlib.sha256()
    with Path(output).open('xb') as out:
        for part in parts:
            data=(Path(directory)/part['name']).read_bytes()
            if len(data)!=part['size_bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
                raise ValueError('Chunk hash mismatch')
            total.update(data);out.write(data)
    if total.hexdigest()!=expected:raise ValueError('Installer hash mismatch')

def api(endpoint, *args, target=None):
    command=['gh','api',f'repos/{REPO}/'+endpoint,*args]
    for attempt in range(3):
        try:
            if target:
                with Path(target).open('wb') as stream:
                    subprocess.run(command,stdout=stream,stderr=subprocess.DEVNULL,check=True,timeout=240)
                return
            return json.loads(subprocess.check_output(command,stderr=subprocess.DEVNULL,timeout=240) or 'null')
        except (subprocess.SubprocessError,ValueError):
            if attempt==2:raise RuntimeError('Bounded GitHub API attempts exhausted') from None
            time.sleep(3)

def main():
    if os.environ.get('GITHUB_REPOSITORY')!=REPO:raise ValueError('Distribution repository required')
    rid=os.environ['RELEASE_ID'];expected=os.environ['INSTALLER_SHA256'];mh=os.environ['MANIFEST_SHA256']
    if not rid.isdecimal() or not all(re.fullmatch('[0-9a-f]{64}',x) for x in [expected,mh]):raise ValueError('Invalid inputs')
    release=api('releases/'+rid)
    if not release['draft'] or release['prerelease']:raise ValueError('Assembly only allowed for draft release')
    assets=api('releases/'+rid+'/assets?per_page=100')
    # At most 512 chunks: enumerate all pages, never assume first page is complete.
    page=2
    while len(assets)%100==0 and assets:
        batch=api(f'releases/{rid}/assets?per_page=100&page={page}')
        if not batch:break
        assets+=batch;page+=1
        if page>8:raise ValueError('Unexpected attachment count')
    names={}
    for asset in assets:
        if asset['name'] in names:raise ValueError('Duplicate attachment name')
        names[asset['name']]=asset
    manifest_name='upload-'+expected+'.json';asset=names[manifest_name]
    if asset.get('digest')!='sha256:'+mh:raise ValueError('Manifest server digest mismatch')
    folder=Path('assembly');folder.mkdir(exist_ok=False)
    mf=folder/'manifest.json';api('releases/assets/'+str(asset['id']),'-H','Accept: application/octet-stream',target=mf)
    if hashlib.sha256(mf.read_bytes()).hexdigest()!=mh:raise ValueError('Manifest bytes mismatch')
    manifest=json.loads(mf.read_text());parts=validate(manifest,expected)
    if release['tag_name']!='v'+manifest['name'].split('_')[1]:raise ValueError('Release version mismatch')
    prior=names.get(manifest['name'])
    if prior:
        if prior.get('state')=='uploaded' and prior.get('size')==manifest['size_bytes'] and prior.get('digest')=='sha256:'+expected:
            print('EXISTING_FULL_INSTALLER_VERIFIED');return
        raise ValueError('Existing full installer conflicts; explicit cleanup required')
    for p in parts:
        a=names[p['name']]
        if a['state']!='uploaded' or a['size']!=p['size_bytes'] or a.get('digest')!='sha256:'+p['sha256']:
            raise ValueError('Chunk server identity mismatch')
        api('releases/assets/'+str(a['id']),'-H','Accept: application/octet-stream',target=folder/p['name'])
    output=folder/manifest['name'];merge(manifest,expected,folder,output)
    # Upload one verified full EXE from GitHub's network. No feed or latest changes.
    subprocess.run(['gh','release','upload',release['tag_name'],str(output),'--repo',REPO],check=True,timeout=600)
    final=api('releases/'+rid+'/assets?per_page=100')
    a=next(a for a in final if a['name']==manifest['name'])
    if a.get('digest')!='sha256:'+expected or a['size']!=manifest['size_bytes']:raise ValueError('Final server digest mismatch')
    print('ASSEMBLED_FULL_INSTALLER_SHA256_VERIFIED',expected)

if __name__=='__main__':main()
