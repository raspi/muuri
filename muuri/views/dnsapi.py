import logging

log = logging.getLogger(__name__)

from pyramid.view import view_config

from ..models import DnsApiModel
from . import SecureView


class DnsApiViews(SecureView):
    __parent__ = None

    @view_config(route_name='dnsapi.home', renderer='dnsapi/home.pt')
    def home(self):
        m = DnsApiModel()
        apilist = m.list_all()

        l = []

        for i in apilist:
            l.append({
                'id': i.id,
                'link': self.request.route_path('dnsapi.zones', id=i.id),
            })

        return {
            'out': '',
            'apilist': l,
        }

    @view_config(route_name='dnsapi.add', renderer='dnsapi/add.pt')
    def add(self):
        """
        Add new DNS API
        """
        import pyramid.httpexceptions as exc

        m = DnsApiModel()
        types = m.get_api_types()

        api_types = []

        for i in types:
            api_types.append({'id': i, 'name': types[i]['name']})

        if self.request.method.lower() == 'post':
            form_apitype = self.request.POST.get('apitype')
            form_address = self.request.POST.get('address')
            form_port = self.request.POST.get('port')
            form_apikey = self.request.POST.get('apikey')
            form_apipass = self.request.POST.get('apipass')

            m.add_api(apikey=form_apikey, apitype=int(form_apitype), host=form_address, port=int(form_port),
                      password=form_apipass)

            return exc.HTTPFound(location=self.request.route_path('dnsapi.home'), comment="DNS API: Add")

        return {'apitypes': api_types}

    @view_config(route_name='dnsapi.zones', renderer='dnsapi/zones.pt')
    def zones(self):
        m = DnsApiModel()
        api = m.get_api_id(self.request.matchdict['id'])

        zones = []

        return {
            'zonelist': zones
        }

    @view_config(route_name='dnsapi.zone', renderer='dnsapi/zone.pt')
    def zone(self):
        pass
