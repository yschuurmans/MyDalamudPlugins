import json
import os
from itertools import zip_longest
from time import time
from sys import argv
from os.path import getmtime
from zipfile import ZipFile, ZIP_DEFLATED

BRANCH = os.environ['GITHUB_REF'].split('refs/heads/')[-1]
DOWNLOAD_URL = 'https://github.com/yschuurmans/MyDalamudPlugins/raw/{branch}/plugins/{plugin_name}/latest.zip'

DEFAULTS = {
    'IsHide': False,
    'IsTestingExclusive': False,
    'ApplicableVersion': 'any',
}

DUPLICATES = {
    'DownloadLinkInstall': ['DownloadLinkTesting', 'DownloadLinkUpdate'],
}

TRIMMED_KEYS = [
    'Author',
    'Name',
    'Punchline',
    'Description',
    'Changelog',
    'InternalName',
    'AssemblyVersion',
    'RepoUrl',
    'ApplicableVersion',
    'Tags',
    'DalamudApiLevel',
    'LoadPriority',
    'IconUrl',
    'ImageUrls',
]


def parse_version(version):
    if version is None:
        return ()

    parts = []
    for part in str(version).split('.'):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(part)
    return tuple(parts)


def is_newer_plugin(candidate, existing):
    candidate_version = parse_version(candidate.get('AssemblyVersion'))
    existing_version = parse_version(existing.get('AssemblyVersion'))

    for candidate_part, existing_part in zip_longest(candidate_version, existing_version, fillvalue=0):
        if candidate_part == existing_part:
            continue
        return candidate_part > existing_part

    return False

def main():
    # extract the manifests from inside the zip files
    master = extract_manifests()

    # trim the manifests
    master = [trim_manifest(manifest) for manifest in master]

    # convert the list of manifests into a master list
    add_extra_fields(master)

    # write the master
    write_master(master)

    # update the LastUpdated field in master
    last_updated()

def extract_manifests():
    manifests = {}

    for dirpath, dirnames, filenames in os.walk('./plugins'):
        if len(filenames) == 0 or 'latest.zip' not in filenames:
            continue
        plugin_name = os.path.basename(os.path.normpath(dirpath))
        latest_zip = os.path.join(dirpath, 'latest.zip')
        with ZipFile(latest_zip) as z:
            manifest = json.loads(z.read(f'{plugin_name}.json').decode('utf-8'))
            manifest_key = manifest.get('InternalName') or manifest.get('Name')
            existing_manifest = manifests.get(manifest_key)
            if existing_manifest is None or is_newer_plugin(manifest, existing_manifest):
                manifests[manifest_key] = manifest

    return list(manifests.values())

def add_extra_fields(manifests):
    for manifest in manifests:
        # generate the download link from the internal assembly name
        manifest['DownloadLinkInstall'] = DOWNLOAD_URL.format(branch=BRANCH, plugin_name=manifest["InternalName"])
        # add default values if missing
        for k, v in DEFAULTS.items():
            if k not in manifest:
                manifest[k] = v
        # duplicate keys as specified in DUPLICATES
        for source, keys in DUPLICATES.items():
            for k in keys:
                if k not in manifest:
                    manifest[k] = manifest[source]
        manifest['DownloadCount'] = 0

def write_master(master):
    # write as pretty json
    with open('pluginmaster.json', 'w') as f:
        json.dump(master, f, indent=4)

def trim_manifest(plugin):
    return {k: plugin[k] for k in TRIMMED_KEYS if k in plugin}

def last_updated():
    with open('pluginmaster.json') as f:
        master = json.load(f)

    for plugin in master:
        latest = f'plugins/{plugin["InternalName"]}/latest.zip'
        modified = int(getmtime(latest))

        if 'LastUpdate' not in plugin or modified != int(plugin['LastUpdate']):
            plugin['LastUpdate'] = str(modified)

    with open('pluginmaster.json', 'w') as f:
        json.dump(master, f, indent=4)

if __name__ == '__main__':
    main()
