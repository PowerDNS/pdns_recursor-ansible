import yaml

instances = {'a': 5301, 'b': 5302}


def test_instance_configuration(host, config_dir):
    for name, port in instances.items():
        f = host.file('{}/recursor-{}.conf'.format(config_dir, name))
        assert f.exists
        # The template renders numeric strings as integers.
        assert yaml.safe_load(f.content_string)['incoming']['port'] == port


def test_instance_service(host):
    for name in instances:
        s = host.service('pdns-recursor@{}'.format(name))
        assert s.is_running
        assert s.is_enabled


def test_instance_listens(host):
    for port in instances.values():
        assert host.socket('udp://127.0.0.1:{}'.format(port)).is_listening
