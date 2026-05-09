import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
BASE_MASTER_PATH = ROOT / 'pluginmaster.json'
SOURCES_PATH = ROOT / 'personalpluginmaster.sources.json'
OUTPUT_PATH = ROOT / 'personalpluginmaster.json'


def load_json(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.write('\n')


def load_manifest(source):
    repository_url = source['repository_url']
    if repository_url.startswith('http://') or repository_url.startswith('https://'):
        request = Request(repository_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(request) as response:
            return json.load(response)

    resolved_path = Path(repository_url)
    if not resolved_path.is_absolute():
        resolved_path = ROOT / resolved_path
    return load_json(resolved_path)


def matches_requested_plugin(plugin, requested_names):
    return plugin.get('Name') in requested_names or plugin.get('InternalName') in requested_names


def merge_external_plugins(base_master, sources):
    merged = list(base_master)
    seen_keys = {plugin.get('InternalName') or plugin.get('Name') for plugin in merged}

    for source in sources:
        manifest = load_manifest(source)
        requested_names = set(source['plugin_names'])

        for plugin in manifest:
            if not matches_requested_plugin(plugin, requested_names):
                continue

            plugin_key = plugin.get('InternalName') or plugin.get('Name')
            if plugin_key in seen_keys:
                continue

            merged.append(plugin)
            seen_keys.add(plugin_key)

    return merged


def main():
    base_master = load_json(BASE_MASTER_PATH)
    sources_config = load_json(SOURCES_PATH)
    merged_master = merge_external_plugins(base_master, sources_config['sources'])
    save_json(OUTPUT_PATH, merged_master)


if __name__ == '__main__':
    main()