import re


class Patterns(object):
    def regex_ip(self, data):
        pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        try:
            return [0 <= int(x) < 256 for x in re.split('\.', pattern.match(data).group())].count(True) == 4
        except:
            return False