import netifaces


class NetworkInformation(object):
    def get_net_add(self):
        get_netifc = netifaces.interfaces()
        list_net_detail = []
        try:
            for line in get_netifc:
                inf = netifaces.ifaddresses(line)
                if 2 in inf.keys() and 'lo' != line:
                    dicts = []
                    dicts.extend(inf[2])
                    dicts[0]['eth'] = line
                    list_net_detail.extend(inf[2])

            return list_net_detail
        except Exception, e:
            self.write_log(e, '/var/log/openvpn-errors.log')
            pass

    def get_broadcast(self, host):
        broad = ''
        i = 0
        for line in host.split('.'):

            if i < 3:
                broad += line + '.'
            i += 1
        broad += '255'
        return broad