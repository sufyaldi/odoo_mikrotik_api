from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

try:
    from librouteros import connect
    LIBROUTEROS_AVAILABLE = True
except ImportError:
    _logger.error("librouteros is not available. Please install the library.")
    LIBROUTEROS_AVAILABLE = False

class MikrotikConfig(models.Model):
    _name = 'mikrotik.config'
    _description = 'Mikrotik Configuration'

    name = fields.Char(string='Name', required=True)
    ip_address = fields.Char(string='IP Address', required=True)
    port = fields.Char(string='Port', required=True, default='8728')  # Default Mikrotik API port as string
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)

    def _clean_port(self, port_str):
        return int(port_str.replace(',', ''))

    def get_interface_traffic(self):
        if not LIBROUTEROS_AVAILABLE:
            _logger.error("librouteros is not available. Skipping get_interface_traffic.")
            return []

        try:
            port = self._clean_port(self.port)  # Clean port string to integer
            _logger.info(f"Connecting to Mikrotik at {self.ip_address}:{port} with user {self.username}")
            api = connect(username=self.username, password=self.password, host=self.ip_address, port=port)
            _logger.info("Connected to Mikrotik API")
            interfaces = api.path('interface')
            traffic_data = []
            for interface in interfaces:
                _logger.info(f"Interface data: {interface}")
                if 'name' in interface and 'rx-byte' in interface and 'tx-byte' in interface:
                    traffic_data.append({
                        'name': interface['name'],
                        'rx': interface['rx-byte'],
                        'tx': interface['tx-byte']
                    })
                else:
                    _logger.warning(f"Skipping interface due to missing data: {interface}")
            return traffic_data
        except Exception as e:
            _logger.error(f"Failed to get interface traffic: {str(e)}")
            return []

    def action_monitor_mikrotik(self):
        _logger.info("Action Monitor Mikrotik Called")
        traffic_data = self.get_interface_traffic()
        _logger.info(f"Traffic Data: {traffic_data}")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Mikrotik Monitor',
                'message': f'Traffic Data: {traffic_data}',
                'sticky': False,
            }
        }
