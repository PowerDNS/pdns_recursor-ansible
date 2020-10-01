def test_systemd_override(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/pdns-recursor.service.d/override.conf'
        f = host.file(fname)

        assert not f.exists
